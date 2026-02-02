#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析CMAUP植物匹配结果并生成UPDATE SQL
====================================
功能: 为已匹配的植物生成UPDATE SQL，补充taxonomy ID信息
"""

import json
import os

# 文件路径
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
MATCHED_FILE = os.path.join(OUTPUT_DIR, 'matched_plants.json')
UNMATCHED_FILE = os.path.join(OUTPUT_DIR, 'unmatched_plants.json')
ANALYSIS_OUTPUT = os.path.join(OUTPUT_DIR, 'matched_plants_analysis.txt')
UPDATE_SQL_OUTPUT = os.path.join(OUTPUT_DIR, 'update_bio_resources_taxonomy.sql')


def analyze_matched():
    """分析已匹配的植物"""
    print("分析已匹配植物...")

    with open(MATCHED_FILE, 'r', encoding='utf-8') as f:
        matched = json.load(f)

    print(f"已匹配植物数: {len(matched)}")

    # 按匹配方法分类
    by_method = {}
    for plant in matched:
        method = plant['match_method']
        if method not in by_method:
            by_method[method] = []
        by_method[method].append(plant)

    return matched, by_method


def analyze_unmatched():
    """分析未匹配植物"""
    print("分析未匹配植物...")

    with open(UNMATCHED_FILE, 'r', encoding='utf-8') as f:
        unmatched = json.load(f)

    # 按匹配方法分类
    multiple_matches = [p for p in unmatched if p['match_method'] in ['genus_family_multiple', 'genus_only_multiple']]
    no_match = [p for p in unmatched if p['match_method'] == 'no_match']

    return unmatched, multiple_matches, no_match


def generate_analysis_report(matched, by_method, unmatched, multiple_matches, no_match):
    """生成分析报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("CMAUP植物匹配详细分析")
    lines.append("=" * 80)
    lines.append("")

    # 匹配统计
    lines.append("## 匹配统计")
    lines.append(f"已匹配植物数: {len(matched)}")
    lines.append(f"未匹配植物数: {len(unmatched)}")
    lines.append(f"匹配率: {len(matched)/(len(matched)+len(unmatched))*100:.2f}%")
    lines.append("")

    # 按匹配方法统计
    lines.append("## 按匹配方法统计")
    lines.append("-" * 80)
    for method, plants in by_method.items():
        lines.append(f"{method}: {len(plants)}")
    lines.append("")

    # 未匹配植物统计
    lines.append("## 未匹配植物统计")
    lines.append("-" * 80)
    lines.append(f"多个候选匹配（需人工确认）: {len(multiple_matches)}")
    lines.append(f"完全未匹配: {len(no_match)}")
    lines.append("")

    # 完全未匹配植物列表
    if no_match:
        lines.append("## 完全未匹配植物列表")
        lines.append("-" * 80)
        for plant in no_match:
            lines.append(f"CMAUP ID: {plant['cmaup_id']}")
            lines.append(f"  植物名: {plant['plant_name']}")
            lines.append(f"  拉丁名: {plant['species_name']}")
            lines.append(f"  属名: {plant['genus_name']}")
            lines.append(f"  科名: {plant['family_name']}")
            lines.append("")

    lines.append("=" * 80)

    return '\n'.join(lines)


def generate_update_sql(matched):
    """生成UPDATE SQL脚本"""
    lines = []
    lines.append("-- ============================================================================")
    lines.append("-- 更新bio_resources表的taxonomy ID信息（基于CMAUP匹配结果）")
    lines.append("-- ============================================================================")
    lines.append("-- 注意: 此脚本更新已匹配植物的taxonomy ID字段")
    lines.append("-- ============================================================================")
    lines.append("")

    lines.append("BEGIN;")
    lines.append("")

    update_count = 0
    for plant in matched:
        bio_resource_id = plant['bio_resource_id']

        # 获取taxonomy IDs（处理NA值）
        species_tax_id = plant['species_tax_id'] if plant['species_tax_id'] != 'NA' else None
        genus_tax_id = plant['genus_tax_id'] if plant['genus_tax_id'] != 'NA' else None
        family_tax_id = plant['family_tax_id'] if plant['family_tax_id'] != 'NA' else None
        cmaup_id = plant['cmaup_id']

        # 只有当至少有一个taxonomy ID不为NA时才更新
        if species_tax_id or genus_tax_id or family_tax_id:
            lines.append(f"-- {plant['cmaup_id']}: {plant['plant_name']}")
            lines.append("UPDATE bio_resources SET")

            update_fields = []
            if species_tax_id:
                update_fields.append(f"    species_tax_id = '{species_tax_id}'")
            if genus_tax_id:
                update_fields.append(f"    genus_tax_id = '{genus_tax_id}'")
            if family_tax_id:
                update_fields.append(f"    family_tax_id = '{family_tax_id}'")
            if cmaup_id:
                update_fields.append(f"    cmaup_id = '{cmaup_id}'")

            lines.append(",\n".join(update_fields))
            lines.append(f"WHERE id = {bio_resource_id};")
            lines.append("")
            update_count += 1

    lines.append("COMMIT;")
    lines.append("")
    lines.append(f"-- 总计更新: {update_count} 条记录")

    return '\n'.join(lines)


def main():
    print("CMAUP植物匹配分析程序")
    print("=" * 80)

    # 分析已匹配植物
    matched, by_method = analyze_matched()

    # 分析未匹配植物
    unmatched, multiple_matches, no_match = analyze_unmatched()

    # 生成分析报告
    print("\n生成分析报告...")
    report = generate_analysis_report(matched, by_method, unmatched, multiple_matches, no_match)
    with open(ANALYSIS_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"已保存分析报告: {ANALYSIS_OUTPUT}")

    # 生成UPDATE SQL脚本
    print("\n生成UPDATE SQL脚本...")
    update_sql = generate_update_sql(matched)
    with open(UPDATE_SQL_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(update_sql)
    print(f"已保存UPDATE SQL脚本: {UPDATE_SQL_OUTPUT}")

    # 打印报告
    print("\n" + report)

    print("\n分析完成！")
    print("\n下一步:")
    print("1. 执行UPDATE SQL更新bio_resources:")
    print(f"   psql -U yfguo -d npdb -f {UPDATE_SQL_OUTPUT}")
    print("2. 处理多个候选匹配的植物（需人工确认）")


if __name__ == '__main__':
    main()
