#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析未匹配药材并生成创建建议
============================
功能: 分析未匹配的TCMID药材，生成创建新bio_resources记录的SQL脚本
"""

import json
import os
from collections import Counter

# 文件路径
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
UNMATCHED_FILE = os.path.join(OUTPUT_DIR, 'unmatched_herbs.json')
ANALYSIS_OUTPUT = os.path.join(OUTPUT_DIR, 'unmatched_herbs_analysis.txt')
SQL_OUTPUT = os.path.join(OUTPUT_DIR, 'create_missing_bio_resources.sql')


def analyze_unmatched():
    """分析未匹配药材"""
    print("分析未匹配药材...")

    with open(UNMATCHED_FILE, 'r', encoding='utf-8') as f:
        unmatched = json.load(f)

    # 按唯一药材分组
    unique_herbs = {}
    for herb in unmatched:
        key = (herb['component_id'], herb['latin_name'], herb['chinese_name'])
        if key not in unique_herbs:
            unique_herbs[key] = {
                'component_id': herb['component_id'],
                'latin_name': herb['latin_name'],
                'chinese_name': herb['chinese_name'],
                'match_method': herb['match_method'],
                'count': 0,
                'prescriptions': []
            }
        unique_herbs[key]['count'] += 1
        unique_herbs[key]['prescriptions'].append(herb['prescription_id'])

    # 按匹配方法分类
    by_method = {
        'no_match': [],
        'fuzzy_multiple': []
    }

    for herb_data in unique_herbs.values():
        method = herb_data['match_method']
        if method == 'no_match':
            by_method['no_match'].append(herb_data)
        elif method == 'fuzzy_latin_multiple':
            by_method['fuzzy_multiple'].append(herb_data)

    # 按使用频率排序
    by_method['no_match'].sort(key=lambda x: x['count'], reverse=True)
    by_method['fuzzy_multiple'].sort(key=lambda x: x['count'], reverse=True)

    return by_method, unique_herbs


def identify_resource_type(latin_name, chinese_name):
    """根据拉丁名和中文名识别资源类型"""
    # 动物相关关键词
    animal_keywords = ['gallus', 'cervus', 'crassostrea', 'bos', 'equus', 'sus']
    # 矿物相关关键词
    mineral_keywords = ['succinus', 'gypsum', 'magnetitum', 'haematitum']
    # 微生物相关关键词
    microbe_keywords = ['wolfiporia', 'poria', 'fungus']

    latin_lower = latin_name.lower()

    for keyword in animal_keywords:
        if keyword in latin_lower:
            return 'Animal'

    for keyword in mineral_keywords:
        if keyword in latin_lower:
            return 'Mineral'

    for keyword in microbe_keywords:
        if keyword in latin_lower:
            return 'Microbe'

    # 默认为植物
    return 'Plant'


def generate_analysis_report(by_method, unique_herbs):
    """生成分析报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("未匹配药材详细分析")
    lines.append("=" * 80)
    lines.append("")

    # 统计
    lines.append("## 统计概览")
    lines.append(f"完全未匹配药材数: {len(by_method['no_match'])}")
    lines.append(f"模糊匹配（多个候选）: {len(by_method['fuzzy_multiple'])}")
    lines.append(f"总计: {len(unique_herbs)}")
    lines.append("")

    # 完全未匹配药材（按使用频率排序）
    lines.append("## 完全未匹配药材（按使用频率排序，前50）")
    lines.append("-" * 80)
    for i, herb in enumerate(by_method['no_match'][:50], 1):
        lines.append(f"{i}. {herb['component_id']} - {herb['chinese_name']} ({herb['latin_name']})")
        lines.append(f"   使用次数: {herb['count']}")
        lines.append(f"   资源类型建议: {identify_resource_type(herb['latin_name'], herb['chinese_name'])}")
        lines.append("")

    # 模糊匹配（多个候选）
    lines.append("## 模糊匹配药材（多个候选，需人工确认）")
    lines.append("-" * 80)
    for i, herb in enumerate(by_method['fuzzy_multiple'][:20], 1):
        lines.append(f"{i}. {herb['component_id']} - {herb['chinese_name']} ({herb['latin_name']})")
        lines.append(f"   使用次数: {herb['count']}")
        lines.append("")

    # 按资源类型统计
    lines.append("## 按资源类型统计（完全未匹配）")
    lines.append("-" * 80)
    type_counter = Counter()
    for herb in by_method['no_match']:
        resource_type = identify_resource_type(herb['latin_name'], herb['chinese_name'])
        type_counter[resource_type] += 1

    for resource_type, count in type_counter.most_common():
        lines.append(f"{resource_type}: {count}")
    lines.append("")

    lines.append("=" * 80)

    return '\n'.join(lines)


def generate_create_sql(by_method):
    """生成创建新bio_resources的SQL脚本"""
    lines = []
    lines.append("-- ============================================================================")
    lines.append("-- 创建缺失的生物资源记录（基于TCMID未匹配药材）")
    lines.append("-- ============================================================================")
    lines.append("-- 注意: 此脚本仅包含完全未匹配的药材")
    lines.append("-- 模糊匹配（多个候选）的药材需要人工确认后再处理")
    lines.append("-- ============================================================================")
    lines.append("")

    # 生成resource_id的起始值
    lines.append("-- 获取当前最大resource_id编号")
    lines.append("-- SELECT MAX(CAST(SUBSTRING(resource_id FROM 4) AS INTEGER)) FROM bio_resources WHERE resource_id LIKE 'RES%';")
    lines.append("")

    # 为每个未匹配药材生成INSERT语句
    lines.append("-- 插入新的生物资源记录")
    lines.append("BEGIN;")
    lines.append("")

    resource_id_counter = 50000  # 从RES50000开始

    for herb in by_method['no_match']:
        if not herb['latin_name'].strip():
            # 跳过没有拉丁名的
            continue

        resource_type = identify_resource_type(herb['latin_name'], herb['chinese_name'])
        resource_id = f"RES{resource_id_counter:05d}"
        resource_id_counter += 1

        # 从拉丁名提取属名和种名
        latin_parts = herb['latin_name'].strip().split()
        genus = latin_parts[0] if len(latin_parts) > 0 else ''
        species = ' '.join(latin_parts[:2]) if len(latin_parts) >= 2 else latin_parts[0] if latin_parts else ''

        # 转义所有单引号
        chinese_name_escaped = herb['chinese_name'].replace("'", "''")
        latin_name_escaped = herb['latin_name'].replace("'", "''")
        genus_escaped = genus.replace("'", "''")
        species_escaped = species.replace("'", "''")

        lines.append(f"-- {herb['component_id']}: {herb['chinese_name']} ({herb['latin_name']})")
        lines.append("INSERT INTO bio_resources (")
        lines.append("    resource_id, resource_type, chinese_name, latin_name,")
        lines.append("    taxonomy_genus, taxonomy_species, tcmid_id")
        lines.append(") VALUES (")
        lines.append(f"    '{resource_id}',")
        lines.append(f"    '{resource_type}',")
        lines.append(f"    '{chinese_name_escaped}',")
        lines.append(f"    '{latin_name_escaped}',")
        lines.append(f"    '{genus_escaped}',")
        lines.append(f"    '{species_escaped}',")
        lines.append(f"    '{herb['component_id']}'")
        lines.append(") ON CONFLICT (resource_id) DO NOTHING;")
        lines.append("")

    lines.append("COMMIT;")
    lines.append("")
    lines.append(f"-- 总计: {len([h for h in by_method['no_match'] if h['latin_name'].strip()])} 条新记录")

    return '\n'.join(lines)


def main():
    print("未匹配药材分析程序")
    print("=" * 80)

    # 分析未匹配药材
    by_method, unique_herbs = analyze_unmatched()

    # 生成分析报告
    print("\n生成分析报告...")
    report = generate_analysis_report(by_method, unique_herbs)
    with open(ANALYSIS_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"已保存分析报告: {ANALYSIS_OUTPUT}")

    # 生成SQL脚本
    print("\n生成SQL脚本...")
    sql = generate_create_sql(by_method)
    with open(SQL_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(sql)
    print(f"已保存SQL脚本: {SQL_OUTPUT}")

    # 打印报告
    print("\n" + report)

    print("\n分析完成！")


if __name__ == '__main__':
    main()
