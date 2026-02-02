#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入TCMID处方数据
==================
功能: 将清洗后的TCMID处方数据导入数据库
输入:
  - cleaned_prescriptions.json
  - cleaned_prescription_herbs.json
  - matched_herbs.json (药材匹配结果)
输出:
  - 导入prescriptions表
  - 导入prescription_resources表
  - 生成导入报告
"""

import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from collections import defaultdict

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': os.environ.get('DB_USER', 'yfguo'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'host': 'localhost',
    'port': 5432
}

# 文件路径
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
CLEANED_PRESCRIPTIONS_FILE = os.path.join(OUTPUT_DIR, 'cleaned_prescriptions.json')
CLEANED_HERBS_FILE = os.path.join(OUTPUT_DIR, 'cleaned_prescription_herbs.json')
MATCHED_HERBS_FILE = os.path.join(OUTPUT_DIR, 'matched_herbs.json')
REPORT_OUTPUT = os.path.join(OUTPUT_DIR, 'tcmid_import_report.txt')


def connect_db():
    """连接数据库"""
    return psycopg2.connect(**DB_CONFIG)


def load_matched_herbs():
    """加载药材匹配结果"""
    print("加载药材匹配结果...")
    with open(MATCHED_HERBS_FILE, 'r', encoding='utf-8') as f:
        matched_herbs = json.load(f)

    # 创建映射：(prescription_id, component_id) -> bio_resource_id
    herb_mapping = {}
    for herb in matched_herbs:
        key = (herb['prescription_id'], herb['component_id'])
        herb_mapping[key] = herb['bio_resource_id']

    print(f"已加载 {len(herb_mapping)} 条药材匹配记录")
    return herb_mapping


def get_next_prescription_id(conn):
    """获取下一个处方ID"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COALESCE(MAX(CAST(SUBSTRING(prescription_id FROM 5) AS INTEGER)), 0) + 1
            FROM prescriptions
            WHERE prescription_id LIKE 'PRES%'
        """)
        next_id = cur.fetchone()[0]
    return f"PRES{next_id:05d}"


def import_prescriptions(conn, prescriptions_data):
    """导入处方数据"""
    print("\n导入处方数据...")

    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'with_icd11': 0
    }

    # 创建TCMID ID到数据库ID的映射
    tcmid_to_db_id = {}

    with conn.cursor() as cur:
        for idx, prescription in enumerate(prescriptions_data, 1):
            if idx % 100 == 0:
                print(f"进度: {idx}/{len(prescriptions_data)}")

            stats['total'] += 1

            try:
                # 生成新的prescription_id
                prescription_id = get_next_prescription_id(conn)

                # 提取ICD-11编码（取第一个）
                icd11_category = None
                if prescription['icd11_codes']:
                    icd11_category = prescription['icd11_codes'][0]['code']
                    stats['with_icd11'] += 1

                # 插入处方
                cur.execute("""
                    INSERT INTO prescriptions (
                        prescription_id, english_name, chinese_name,
                        pinyin_name, functions, indications,
                        disease_icd11_category, reference, tcmid_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    prescription_id,
                    prescription['english_name'],
                    prescription['chinese_name'],
                    prescription['pinyin_name'],
                    prescription['function_description'],
                    prescription['indications'],
                    icd11_category,
                    prescription['reference'],
                    prescription['prescription_id']  # 保存TCMID原始ID
                ))

                db_id = cur.fetchone()[0]
                tcmid_to_db_id[prescription['prescription_id']] = db_id

                stats['success'] += 1

            except Exception as e:
                stats['failed'] += 1
                print(f"导入处方失败 {prescription['prescription_id']}: {e}")
                conn.rollback()
                continue

        conn.commit()

    print(f"处方导入完成: 成功 {stats['success']}, 失败 {stats['failed']}")
    return tcmid_to_db_id, stats


def import_prescription_herbs(conn, herbs_data, herb_mapping, tcmid_to_db_id):
    """导入处方-药材关联"""
    print("\n导入处方-药材关联...")

    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'no_match': 0,
        'no_prescription': 0
    }

    with conn.cursor() as cur:
        for idx, herb in enumerate(herbs_data, 1):
            if idx % 1000 == 0:
                print(f"进度: {idx}/{len(herbs_data)}")

            stats['total'] += 1

            # 获取处方数据库ID
            prescription_db_id = tcmid_to_db_id.get(herb['prescription_id'])
            if not prescription_db_id:
                stats['no_prescription'] += 1
                continue

            # 获取药材匹配的bio_resource_id
            key = (herb['prescription_id'], herb['component_id'])
            bio_resource_id = herb_mapping.get(key)

            if not bio_resource_id:
                stats['no_match'] += 1
                continue

            try:
                # 插入处方-药材关联
                cur.execute("""
                    INSERT INTO prescription_resources (
                        prescription_id, bio_resource_id, dosage_text,
                        tcmid_component_id, barcode, latin_name, chinese_name
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (prescription_id, bio_resource_id) DO NOTHING
                """, (
                    prescription_db_id,
                    bio_resource_id,
                    herb['quantity'],
                    herb['component_id'],
                    herb['barcode'] if herb['barcode'] else None,
                    herb['latin_name'],
                    herb['chinese_name']
                ))

                stats['success'] += 1

            except Exception as e:
                stats['failed'] += 1
                print(f"导入关联失败 {herb['prescription_id']}-{herb['component_id']}: {e}")
                conn.rollback()
                continue

        conn.commit()

    print(f"关联导入完成: 成功 {stats['success']}, 失败 {stats['failed']}, 无匹配 {stats['no_match']}")
    return stats


def generate_report(prescription_stats, herb_stats):
    """生成导入报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("TCMID处方数据导入报告")
    lines.append("=" * 80)
    lines.append("")

    # 处方导入统计
    lines.append("## 处方导入统计")
    lines.append(f"总处方数: {prescription_stats['total']}")
    lines.append(f"成功导入: {prescription_stats['success']}")
    lines.append(f"导入失败: {prescription_stats['failed']}")
    lines.append(f"有ICD-11编码: {prescription_stats['with_icd11']} ({prescription_stats['with_icd11']/prescription_stats['total']*100:.2f}%)")
    lines.append("")

    # 药材关联导入统计
    lines.append("## 药材关联导入统计")
    lines.append(f"总药材记录数: {herb_stats['total']}")
    lines.append(f"成功导入: {herb_stats['success']}")
    lines.append(f"导入失败: {herb_stats['failed']}")
    lines.append(f"无药材匹配: {herb_stats['no_match']}")
    lines.append(f"无处方记录: {herb_stats['no_prescription']}")
    lines.append(f"导入率: {herb_stats['success']/herb_stats['total']*100:.2f}%")
    lines.append("")

    lines.append("=" * 80)

    return '\n'.join(lines)


def main():
    print("TCMID处方数据导入程序")
    print("=" * 80)

    # 加载数据
    print("\n加载清洗后的数据...")
    with open(CLEANED_PRESCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
        prescriptions_data = json.load(f)
    print(f"已加载 {len(prescriptions_data)} 条处方")

    with open(CLEANED_HERBS_FILE, 'r', encoding='utf-8') as f:
        herbs_data = json.load(f)
    print(f"已加载 {len(herbs_data)} 条药材记录")

    # 加载药材匹配结果
    herb_mapping = load_matched_herbs()

    # 连接数据库
    conn = connect_db()

    try:
        # 导入处方
        tcmid_to_db_id, prescription_stats = import_prescriptions(conn, prescriptions_data)

        # 导入处方-药材关联
        herb_stats = import_prescription_herbs(conn, herbs_data, herb_mapping, tcmid_to_db_id)

        # 生成报告
        report = generate_report(prescription_stats, herb_stats)
        with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n已保存导入报告: {REPORT_OUTPUT}")

        # 打印报告
        print("\n" + report)

    finally:
        conn.close()

    print("\n导入完成！")


if __name__ == '__main__':
    main()
