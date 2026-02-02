#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMAUP 疾病数据导入脚本
========================
功能:
  1. 导入 diseases 表数据
  2. 导入 bio_resource_disease_associations 表数据
"""

import json
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import re

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': 'yfguo',
    'password': '',
    'host': 'localhost',
    'port': 5432
}

# 文件路径
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
DISEASES_FILE = os.path.join(OUTPUT_DIR, 'cleaned_diseases.json')
ASSOCIATIONS_FILE = os.path.join(OUTPUT_DIR, 'cleaned_plant_disease_associations.json')


def connect_db():
    """连接数据库"""
    return psycopg2.connect(**DB_CONFIG)


def generate_disease_id(conn):
    """生成下一个疾病ID"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT MAX(SUBSTRING(disease_id FROM 4)::INT) as max_num
            FROM diseases
            WHERE disease_id ~ '^DIS[0-9]+$'
        """)
        result = cur.fetchone()
        max_num = result[0] if result[0] else 0
        return f"DIS{max_num + 1:04d}"


def import_diseases(conn, diseases_data):
    """
    导入疾病数据到 diseases 表
    """
    print(f"\n导入疾病数据...")
    print(f"待导入疾病数量: {len(diseases_data)}")

    # 检查已存在的疾病
    with conn.cursor() as cur:
        cur.execute("SELECT icd11_code FROM diseases")
        existing_codes = set(row[0] for row in cur.fetchall())

    imported_count = 0
    skipped_count = 0

    for disease in diseases_data:
        icd11_code = disease['icd11_code']

        # 检查是否已存在
        if icd11_code in existing_codes:
            skipped_count += 1
            continue

        # 生成疾病ID
        disease_id = generate_disease_id(conn)

        # 插入数据
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO diseases (
                    disease_id, icd11_code, disease_name, disease_category
                ) VALUES (%s, %s, %s, %s)
            """, (
                disease_id,
                icd11_code,
                disease['disease_name'],
                disease.get('disease_category')
            ))

        imported_count += 1

        if imported_count % 100 == 0:
            conn.commit()
            print(f"已导入: {imported_count}/{len(diseases_data)}")

    conn.commit()

    print(f"导入完成!")
    print(f"  - 新导入: {imported_count}")
    print(f"  - 跳过已存在: {skipped_count}")

    return imported_count, skipped_count


def get_bio_resource_id_by_cmaup_id(conn, cmaup_id):
    """
    通过 CMAUP ID 获取 bio_resource_id
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM bio_resources
            WHERE cmaup_id = %s
        """, (cmaup_id,))
        result = cur.fetchone()
        return result[0] if result else None


def get_disease_id_by_icd11(conn, icd11_code):
    """
    通过 ICD-11 编码获取 disease_id
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM diseases
            WHERE icd11_code = %s
        """, (icd11_code,))
        result = cur.fetchone()
        return result[0] if result else None


def import_associations(conn, associations_data):
    """
    导入植物-疾病关联数据到 bio_resource_disease_associations 表
    """
    print(f"\n导入植物-疾病关联数据...")
    print(f"待导入关联数量: {len(associations_data)}")

    # 统计
    imported_count = 0
    skipped_count = 0
    not_found_plant = 0
    not_found_disease = 0

    # 创建索引映射以提高查询速度
    with conn.cursor() as cur:
        # 加载所有 CMAUP ID 到 bio_resource_id 的映射
        cur.execute("SELECT cmaup_id, id FROM bio_resources WHERE cmaup_id IS NOT NULL")
        plant_mapping = {row[0]: row[1] for row in cur.fetchall()}

        # 加载所有 ICD-11 编码到 disease_id 的映射
        cur.execute("SELECT icd11_code, id FROM diseases")
        disease_mapping = {row[0]: row[1] for row in cur.fetchall()}

        # 检查已存在的关联
        cur.execute("""
            SELECT bio_resource_id, disease_id
            FROM bio_resource_disease_associations
        """)
        existing_associations = set((row[0], row[1]) for row in cur.fetchall())

    for assoc in associations_data:
        plant_id = assoc['plant_id']
        icd11_code = assoc['icd11_code']

        # 查找 bio_resource_id
        bio_resource_id = plant_mapping.get(plant_id)
        if not bio_resource_id:
            not_found_plant += 1
            continue

        # 查找 disease_id
        disease_id = disease_mapping.get(icd11_code)
        if not disease_id:
            not_found_disease += 1
            continue

        # 检查是否已存在
        if (bio_resource_id, disease_id) in existing_associations:
            skipped_count += 1
            continue

        # 插入数据
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO bio_resource_disease_associations (
                    bio_resource_id, disease_id,
                    evidence_therapeutic_target, evidence_transcriptome,
                    evidence_clinical_trial_plant, evidence_clinical_trial_ingredient,
                    confidence_score, source, source_version
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                bio_resource_id,
                disease_id,
                assoc.get('evidence_therapeutic_target'),
                assoc.get('evidence_transcriptome', False),
                assoc.get('evidence_clinical_trial_plant'),
                assoc.get('evidence_clinical_trial_ingredient'),
                assoc.get('confidence_score'),
                'CMAUP',
                '2.0'
            ))

        imported_count += 1
        existing_associations.add((bio_resource_id, disease_id))

        if imported_count % 1000 == 0:
            conn.commit()
            print(f"已导入: {imported_count}/{len(associations_data)}")

    conn.commit()

    print(f"导入完成!")
    print(f"  - 新导入: {imported_count}")
    print(f"  - 跳过已存在: {skipped_count}")
    print(f"  - 未找到植物: {not_found_plant}")
    print(f"  - 未找到疾病: {not_found_disease}")

    return imported_count, skipped_count, not_found_plant, not_found_disease


def update_disease_stats(conn):
    """
    更新 diseases 表的统计字段
    """
    print(f"\n更新疾病统计信息...")

    with conn.cursor() as cur:
        # 更新关联植物数
        cur.execute("""
            UPDATE diseases d
            SET num_of_related_plants = (
                SELECT COUNT(DISTINCT brda.bio_resource_id)
                FROM bio_resource_disease_associations brda
                WHERE brda.disease_id = d.id
            )
        """)

        # 更新关联靶点数（通过治疗靶点证据）
        cur.execute("""
            UPDATE diseases d
            SET num_of_related_targets = (
                SELECT COUNT(DISTINCT unnest(string_to_array(regexp_replace(
                    brda.evidence_therapeutic_target, '\s+', '', 'g'), ',')))
                FROM bio_resource_disease_associations brda
                WHERE brda.disease_id = d.id
                AND brda.evidence_therapeutic_target IS NOT NULL
                AND brda.evidence_therapeutic_target != ''
            )
        """)

    conn.commit()

    print("统计信息更新完成!")


def main():
    """主函数"""
    print("=" * 80)
    print("CMAUP 疾病数据导入")
    print("=" * 80)

    # 读取清洗后的数据
    print(f"\n读取清洗后的数据...")

    with open(DISEASES_FILE, 'r', encoding='utf-8') as f:
        diseases_data = json.load(f)

    with open(ASSOCIATIONS_FILE, 'r', encoding='utf-8') as f:
        associations_data = json.load(f)

    print(f"疾病记录数: {len(diseases_data)}")
    print(f"植物-疾病关联记录数: {len(associations_data)}")

    # 连接数据库并导入
    conn = connect_db()
    try:
        # 1. 导入疾病数据
        print("\n" + "=" * 80)
        print("步骤 1: 导入疾病数据")
        print("=" * 80)
        disease_imported, disease_skipped = import_diseases(conn, diseases_data)

        # 2. 导入植物-疾病关联数据
        print("\n" + "=" * 80)
        print("步骤 2: 导入植物-疾病关联数据")
        print("=" * 80)
        assoc_imported, assoc_skipped, not_found_plant, not_found_disease = \
            import_associations(conn, associations_data)

        # 3. 更新疾病统计信息
        print("\n" + "=" * 80)
        print("步骤 3: 更新疾病统计信息")
        print("=" * 80)
        update_disease_stats(conn)

        # 生成导入报告
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("CMAUP 疾病数据导入报告")
        report_lines.append("=" * 80)
        report_lines.append("")
        report_lines.append("## 疾病数据导入")
        report_lines.append(f"总记录数: {len(diseases_data)}")
        report_lines.append(f"新导入: {disease_imported}")
        report_lines.append(f"跳过已存在: {disease_skipped}")
        report_lines.append("")
        report_lines.append("## 植物-疾病关联数据导入")
        report_lines.append(f"总记录数: {len(associations_data)}")
        report_lines.append(f"新导入: {assoc_imported}")
        report_lines.append(f"跳过已存在: {assoc_skipped}")
        report_lines.append(f"未找到植物 (CMAUP ID): {not_found_plant}")
        report_lines.append(f"未找到疾病 (ICD-11): {not_found_disease}")
        report_lines.append("")
        report_lines.append("=" * 80)

        report = '\n'.join(report_lines)

        # 保存报告
        report_file = os.path.join(OUTPUT_DIR, 'cmaup_disease_import_report.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        # 打印报告
        print("\n" + report)
        print(f"\n报告已保存到: {report_file}")

    finally:
        conn.close()

    print("\n导入完成!")


if __name__ == '__main__':
    main()
