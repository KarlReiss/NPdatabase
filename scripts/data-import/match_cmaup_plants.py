#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMAUP 植物匹配到生物资源
========================
功能: 将 CMAUP Plants.txt 中的植物匹配到 bio_resources 表
匹配策略:
  1. 优先级1: 拉丁名精确匹配
  2. 优先级2: 属名 + 科名匹配
  3. 优先级3: 仅属名匹配（需要人工确认）
  4. 补充策略: 匹配成功后，补充 taxonomy ID 信息

输出:
  - matched_plants.json: 成功匹配的植物
  - unmatched_plants.json: 未匹配的植物
  - plant_matching_report.txt: 匹配报告
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
    'host': 'localhost',
    'port': 5432
}

# 文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data/CMAUP'
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
CMAUP_FILE = os.path.join(DATA_DIR, 'CMAUPv2.0_download_Plants.txt')
MATCHED_OUTPUT = os.path.join(OUTPUT_DIR, 'matched_plants.json')
UNMATCHED_OUTPUT = os.path.join(OUTPUT_DIR, 'unmatched_plants.json')
REPORT_OUTPUT = os.path.join(OUTPUT_DIR, 'plant_matching_report.txt')

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)


def connect_db():
    """连接数据库"""
    return psycopg2.connect(**DB_CONFIG)


def load_bio_resources(conn):
    """加载所有植物类生物资源数据到内存"""
    print("加载生物资源数据...")
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, resource_id, latin_name, chinese_name,
                   taxonomy_genus, taxonomy_family, taxonomy_species
            FROM bio_resources
            WHERE resource_type = 'Plant'
        """)
        resources = cur.fetchall()

    print(f"已加载 {len(resources)} 条植物类生物资源记录")
    return resources


def normalize_latin_name(name):
    """标准化拉丁名（转小写，去除多余空格）"""
    if not name or name == 'NA':
        return ""
    return ' '.join(name.lower().strip().split())


def normalize_genus_name(name):
    """标准化属名（转小写，去除空格）"""
    if not name or name == 'NA':
        return ""
    return name.lower().strip()


def normalize_family_name(name):
    """标准化科名（转小写，去除空格）"""
    if not name or name == 'NA':
        return ""
    return name.lower().strip()


def match_plant_by_latin_name(cmaup_plant, resources):
    """
    优先级1: 拉丁名精确匹配
    """
    cmaup_latin = normalize_latin_name(cmaup_plant['Species_Name'])
    if not cmaup_latin:
        return None, None

    for res in resources:
        res_latin = normalize_latin_name(res['latin_name'])
        if res_latin == cmaup_latin:
            return res['id'], 'exact_latin'

    return None, None


def match_plant_by_genus_family(cmaup_plant, resources):
    """
    优先级2: 属名 + 科名匹配
    """
    cmaup_genus = normalize_genus_name(cmaup_plant['Genus_Name'])
    cmaup_family = normalize_family_name(cmaup_plant['Family_Name'])

    if not cmaup_genus or not cmaup_family:
        return None, None

    matches = []
    for res in resources:
        res_genus = normalize_genus_name(res['taxonomy_genus'])
        res_family = normalize_family_name(res['taxonomy_family'])

        if res_genus == cmaup_genus and res_family == cmaup_family:
            matches.append(res['id'])

    if len(matches) == 1:
        return matches[0], 'genus_family'
    elif len(matches) > 1:
        return matches, 'genus_family_multiple'

    return None, None


def match_plant_by_genus_only(cmaup_plant, resources):
    """
    优先级3: 仅属名匹配（可能有多个结果）
    """
    cmaup_genus = normalize_genus_name(cmaup_plant['Genus_Name'])

    if not cmaup_genus:
        return None, None

    matches = []
    for res in resources:
        res_genus = normalize_genus_name(res['taxonomy_genus'])
        if res_genus == cmaup_genus:
            matches.append(res['id'])

    if len(matches) == 1:
        return matches[0], 'genus_only_single'
    elif len(matches) > 1:
        return matches, 'genus_only_multiple'

    return None, None


def match_plants(cmaup_data, resources):
    """
    匹配所有CMAUP植物
    """
    matched = []
    unmatched = []
    match_stats = defaultdict(int)

    total = len(cmaup_data)
    print(f"\n开始匹配 {total} 条CMAUP植物记录...")

    for idx, plant in enumerate(cmaup_data, 1):
        if idx % 100 == 0:
            print(f"进度: {idx}/{total}")

        result = {
            'cmaup_id': plant['Plant_ID'],
            'plant_name': plant['Plant_Name'],
            'species_name': plant['Species_Name'],
            'species_tax_id': plant['Species_Tax_ID'],
            'genus_name': plant['Genus_Name'],
            'genus_tax_id': plant['Genus_Tax_ID'],
            'family_name': plant['Family_Name'],
            'family_tax_id': plant['Family_Tax_ID']
        }

        # 尝试匹配
        bio_resource_id = None
        match_method = None

        # 优先级1: 拉丁名精确匹配
        bio_resource_id, match_method = match_plant_by_latin_name(plant, resources)

        # 优先级2: 属名 + 科名匹配
        if not bio_resource_id:
            bio_resource_id, match_method = match_plant_by_genus_family(plant, resources)

        # 优先级3: 仅属名匹配
        if not bio_resource_id:
            bio_resource_id, match_method = match_plant_by_genus_only(plant, resources)

        # 记录结果
        if bio_resource_id:
            if isinstance(bio_resource_id, list):
                # 多个匹配
                result['bio_resource_ids'] = bio_resource_id
                result['match_method'] = match_method
                result['confidence'] = 'low'
                unmatched.append(result)
                match_stats['multiple_matches'] += 1
            else:
                # 成功匹配
                result['bio_resource_id'] = bio_resource_id
                result['match_method'] = match_method
                if match_method == 'exact_latin':
                    result['confidence'] = 'high'
                elif match_method == 'genus_family':
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


def generate_report(matched, unmatched, match_stats, total_plants):
    """
    生成匹配报告
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("CMAUP 植物匹配报告")
    report_lines.append("=" * 80)
    report_lines.append("")

    # 总体统计
    report_lines.append("## 总体统计")
    report_lines.append(f"总CMAUP植物记录数: {total_plants}")
    report_lines.append(f"成功匹配数: {len(matched)}")
    report_lines.append(f"未匹配数: {len(unmatched)}")
    report_lines.append(f"匹配率: {len(matched)/total_plants*100:.2f}%")
    report_lines.append("")

    # 匹配方法统计
    report_lines.append("## 匹配方法统计")
    report_lines.append(f"拉丁名精确匹配: {match_stats.get('exact_latin', 0)}")
    report_lines.append(f"属名+科名匹配: {match_stats.get('genus_family', 0)}")
    report_lines.append(f"仅属名匹配（单个）: {match_stats.get('genus_only_single', 0)}")
    report_lines.append(f"多个匹配（需人工确认）: {match_stats.get('multiple_matches', 0)}")
    report_lines.append(f"完全未匹配: {match_stats.get('no_match', 0)}")
    report_lines.append("")

    # 未匹配植物示例
    if unmatched:
        report_lines.append("## 未匹配植物示例（前20条）")
        report_lines.append("-" * 80)
        for plant in unmatched[:20]:
            report_lines.append(f"CMAUP ID: {plant['cmaup_id']}")
            report_lines.append(f"  植物名: {plant['plant_name']}")
            report_lines.append(f"  拉丁名: {plant['species_name']}")
            report_lines.append(f"  属名: {plant['genus_name']}")
            report_lines.append(f"  科名: {plant['family_name']}")
            report_lines.append(f"  匹配方法: {plant['match_method']}")
            if 'bio_resource_ids' in plant:
                report_lines.append(f"  候选资源IDs: {plant['bio_resource_ids'][:10]}...")
            report_lines.append("")

    # 统计唯一植物
    unique_matched = set(p['cmaup_id'] for p in matched)
    unique_unmatched = set(p['cmaup_id'] for p in unmatched)

    report_lines.append("## 唯一植物统计")
    report_lines.append(f"唯一匹配植物数: {len(unique_matched)}")
    report_lines.append(f"唯一未匹配植物数: {len(unique_unmatched)}")
    report_lines.append("")

    report_lines.append("=" * 80)

    return '\n'.join(report_lines)


def main():
    print("CMAUP 植物匹配程序")
    print("=" * 80)

    # 读取CMAUP植物数据
    print(f"\n读取CMAUP植物数据: {CMAUP_FILE}")
    cmaup_data = []
    with open(CMAUP_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        cmaup_data = list(reader)

    print(f"已读取 {len(cmaup_data)} 条CMAUP植物记录")

    # 连接数据库并加载生物资源
    conn = connect_db()
    try:
        resources = load_bio_resources(conn)

        # 执行匹配
        matched, unmatched, match_stats = match_plants(cmaup_data, resources)

        # 保存结果
        print(f"\n保存匹配结果...")
        with open(MATCHED_OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(matched, f, ensure_ascii=False, indent=2)
        print(f"已保存匹配结果: {MATCHED_OUTPUT}")

        with open(UNMATCHED_OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(unmatched, f, ensure_ascii=False, indent=2)
        print(f"已保存未匹配结果: {UNMATCHED_OUTPUT}")

        # 生成报告
        report = generate_report(matched, unmatched, match_stats, len(cmaup_data))
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
