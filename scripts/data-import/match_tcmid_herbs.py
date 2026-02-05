#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCMID 药材匹配到生物资源
======================
功能: 将 TCMID prescription_herbs.csv 中的药材匹配到 bio_resources 表
匹配策略:
  1. 优先级1: 拉丁名精确匹配
  2. 优先级2: 中文名精确匹配
  3. 优先级3: 拉丁名模糊匹配（属名匹配）
  4. 优先级4: 记录为未匹配，需要创建新记录

输出:
  - matched_herbs.json: 成功匹配的药材
  - unmatched_herbs.json: 未匹配的药材
  - matching_report.txt: 匹配报告
"""

import csv
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from collections import defaultdict
import os
import re

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': os.environ.get('DB_USER', 'yfguo'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 5432))
}

# 文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data/TCMID'
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
HERBS_FILE = os.path.join(DATA_DIR, 'prescription_herbs.csv')
MATCHED_OUTPUT = os.path.join(OUTPUT_DIR, 'matched_herbs.json')
UNMATCHED_OUTPUT = os.path.join(OUTPUT_DIR, 'unmatched_herbs.json')
REPORT_OUTPUT = os.path.join(OUTPUT_DIR, 'herb_matching_report.txt')

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)


def connect_db():
    """连接数据库"""
    return psycopg2.connect(**DB_CONFIG)


def load_bio_resources(conn):
    """加载所有生物资源数据到内存"""
    print("加载生物资源数据...")
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, resource_id, latin_name, chinese_name,
                   taxonomy_genus, taxonomy_family
            FROM bio_resources
            WHERE resource_type IN ('Plant', 'Herb', 'plant', 'herb')
        """)
        resources = cur.fetchall()

    print(f"已加载 {len(resources)} 条生物资源记录")
    return resources


def normalize_latin_name(name):
    """标准化拉丁名（转小写，去除多余空格）"""
    if not name:
        return ""
    return ' '.join(name.lower().strip().split())


def extract_genus(latin_name):
    """从拉丁名中提取属名（第一个单词）"""
    if not latin_name:
        return ""
    parts = latin_name.strip().split()
    return parts[0].lower() if parts else ""


def match_herb_exact_latin(herb, resources):
    """
    优先级1: 拉丁名精确匹配
    """
    herb_latin = normalize_latin_name(herb['LatinName'])
    if not herb_latin:
        return None, None

    for res in resources:
        res_latin = normalize_latin_name(res['latin_name'])
        if res_latin == herb_latin:
            return res['id'], 'exact_latin'

    return None, None


def match_herb_exact_chinese(herb, resources):
    """
    优先级2: 中文名精确匹配
    """
    herb_chinese = herb['ChineseName'].strip()
    if not herb_chinese:
        return None, None

    for res in resources:
        if res['chinese_name'] and res['chinese_name'].strip() == herb_chinese:
            return res['id'], 'exact_chinese'

    return None, None


def match_herb_fuzzy_latin(herb, resources):
    """
    优先级3: 拉丁名模糊匹配（属名匹配）
    返回所有匹配的资源（可能有多个）
    """
    herb_genus = extract_genus(herb['LatinName'])
    if not herb_genus:
        return [], None

    matches = []
    for res in resources:
        res_genus = extract_genus(res['latin_name'])
        if res_genus == herb_genus:
            matches.append(res['id'])

    if len(matches) == 1:
        # 只有一个匹配，可以使用
        return matches[0], 'fuzzy_latin_single'
    elif len(matches) > 1:
        # 多个匹配，需要人工确认
        return matches, 'fuzzy_latin_multiple'

    return None, None


def match_herbs(herbs_data, resources):
    """
    匹配所有药材
    """
    matched = []
    unmatched = []
    match_stats = defaultdict(int)

    total = len(herbs_data)
    print(f"\n开始匹配 {total} 条药材记录...")

    for idx, herb in enumerate(herbs_data, 1):
        if idx % 100 == 0:
            print(f"进度: {idx}/{total}")

        result = {
            'prescription_id': herb['PrescriptionID'],
            'component_id': herb['ComponentID'],
            'latin_name': herb['LatinName'],
            'chinese_name': herb['ChineseName'],
            'quantity': herb['ComponentQuantity'],
            'barcode': herb['Barcode']
        }

        # 尝试匹配
        bio_resource_id = None
        match_method = None

        # 优先级1: 拉丁名精确匹配
        bio_resource_id, match_method = match_herb_exact_latin(herb, resources)

        # 优先级2: 中文名精确匹配
        if not bio_resource_id:
            bio_resource_id, match_method = match_herb_exact_chinese(herb, resources)

        # 优先级3: 拉丁名模糊匹配
        if not bio_resource_id:
            bio_resource_id, match_method = match_herb_fuzzy_latin(herb, resources)

        # 记录结果
        if bio_resource_id:
            if isinstance(bio_resource_id, list):
                # 多个模糊匹配
                result['bio_resource_ids'] = bio_resource_id
                result['match_method'] = match_method
                result['confidence'] = 'low'
                unmatched.append(result)
                match_stats['fuzzy_multiple'] += 1
            else:
                # 成功匹配
                result['bio_resource_id'] = bio_resource_id
                result['match_method'] = match_method
                if match_method == 'exact_latin':
                    result['confidence'] = 'high'
                elif match_method == 'exact_chinese':
                    result['confidence'] = 'high'
                else:
                    result['confidence'] = 'medium'
                matched.append(result)
                match_stats[match_method] += 1
        else:
            # 未匹配
            result['match_method'] = 'no_match'
            result['confidence'] = 'none'
            unmatched.append(result)
            match_stats['no_match'] += 1

    return matched, unmatched, match_stats


def generate_report(matched, unmatched, match_stats, total_herbs):
    """
    生成匹配报告
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("TCMID 药材匹配报告")
    report_lines.append("=" * 80)
    report_lines.append("")

    # 总体统计
    report_lines.append("## 总体统计")
    report_lines.append(f"总药材记录数: {total_herbs}")
    report_lines.append(f"成功匹配数: {len(matched)}")
    report_lines.append(f"未匹配数: {len(unmatched)}")
    report_lines.append(f"匹配率: {len(matched)/total_herbs*100:.2f}%")
    report_lines.append("")

    # 匹配方法统计
    report_lines.append("## 匹配方法统计")
    report_lines.append(f"拉丁名精确匹配: {match_stats.get('exact_latin', 0)}")
    report_lines.append(f"中文名精确匹配: {match_stats.get('exact_chinese', 0)}")
    report_lines.append(f"拉丁名模糊匹配（单个）: {match_stats.get('fuzzy_latin_single', 0)}")
    report_lines.append(f"拉丁名模糊匹配（多个）: {match_stats.get('fuzzy_multiple', 0)}")
    report_lines.append(f"完全未匹配: {match_stats.get('no_match', 0)}")
    report_lines.append("")

    # 未匹配药材示例
    if unmatched:
        report_lines.append("## 未匹配药材示例（前20条）")
        report_lines.append("-" * 80)
        for herb in unmatched[:20]:
            report_lines.append(f"ComponentID: {herb['component_id']}")
            report_lines.append(f"  拉丁名: {herb['latin_name']}")
            report_lines.append(f"  中文名: {herb['chinese_name']}")
            report_lines.append(f"  匹配方法: {herb['match_method']}")
            if 'bio_resource_ids' in herb:
                report_lines.append(f"  候选资源IDs: {herb['bio_resource_ids']}")
            report_lines.append("")

    # 统计唯一药材
    unique_matched = set((h['component_id'], h['latin_name'], h['chinese_name'])
                         for h in matched)
    unique_unmatched = set((h['component_id'], h['latin_name'], h['chinese_name'])
                           for h in unmatched)

    report_lines.append("## 唯一药材统计")
    report_lines.append(f"唯一匹配药材数: {len(unique_matched)}")
    report_lines.append(f"唯一未匹配药材数: {len(unique_unmatched)}")
    report_lines.append("")

    report_lines.append("=" * 80)

    return '\n'.join(report_lines)


def main():
    print("TCMID 药材匹配程序")
    print("=" * 80)

    # 读取TCMID药材数据
    print(f"\n读取TCMID药材数据: {HERBS_FILE}")
    herbs_data = []
    with open(HERBS_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        herbs_data = list(reader)

    print(f"已读取 {len(herbs_data)} 条药材记录")

    # 连接数据库并加载生物资源
    conn = connect_db()
    try:
        resources = load_bio_resources(conn)

        # 执行匹配
        matched, unmatched, match_stats = match_herbs(herbs_data, resources)

        # 保存结果
        print(f"\n保存匹配结果...")
        with open(MATCHED_OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(matched, f, ensure_ascii=False, indent=2)
        print(f"已保存匹配结果: {MATCHED_OUTPUT}")

        with open(UNMATCHED_OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(unmatched, f, ensure_ascii=False, indent=2)
        print(f"已保存未匹配结果: {UNMATCHED_OUTPUT}")

        # 生成报告
        report = generate_report(matched, unmatched, match_stats, len(herbs_data))
        with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"已保存匹配报告: {REPORT_OUTPUT}")

        # 打印报告
        print("\n" + report)

    finally:
        conn.close()

    print("\n匹配完成！")


if __name__ == '__main__':
    main()
