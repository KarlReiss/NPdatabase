#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析未匹配TTD靶点并生成创建建议
================================
功能: 分析未匹配的TTD靶点，生成更新现有targets和创建新targets的SQL脚本
"""

import json
import os
from collections import Counter

# 文件路径
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
MATCHED_FILE = os.path.join(OUTPUT_DIR, 'matched_targets.json')
UNMATCHED_FILE = os.path.join(OUTPUT_DIR, 'unmatched_targets.json')
ANALYSIS_OUTPUT = os.path.join(OUTPUT_DIR, 'unmatched_targets_analysis.txt')
UPDATE_SQL_OUTPUT = os.path.join(OUTPUT_DIR, 'update_matched_targets.sql')
CREATE_SQL_OUTPUT = os.path.join(OUTPUT_DIR, 'create_missing_targets.sql')


def analyze_matched():
    """分析已匹配的靶点，生成UPDATE SQL"""
    print("分析已匹配靶点...")

    with open(MATCHED_FILE, 'r', encoding='utf-8') as f:
        matched = json.load(f)

    print(f"已匹配靶点数: {len(matched)}")
    return matched


def analyze_unmatched():
    """分析未匹配靶点"""
    print("分析未匹配靶点...")

    with open(UNMATCHED_FILE, 'r', encoding='utf-8') as f:
        unmatched = json.load(f)

    # 按靶点类型分类
    by_type = Counter(t['target_type'] for t in unmatched)

    # 按是否有UniProt ID分类
    with_uniprot = [t for t in unmatched if t['uniprot_id'].strip()]
    without_uniprot = [t for t in unmatched if not t['uniprot_id'].strip()]

    # 按是否有基因名分类
    with_gene = [t for t in unmatched if t['gene_name'].strip()]
    without_gene = [t for t in unmatched if not t['gene_name'].strip()]

    return unmatched, by_type, with_uniprot, without_uniprot, with_gene, without_gene


def generate_analysis_report(matched, unmatched, by_type, with_uniprot, without_uniprot, with_gene, without_gene):
    """生成分析报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("TTD靶点匹配详细分析")
    lines.append("=" * 80)
    lines.append("")

    # 匹配统计
    lines.append("## 匹配统计")
    lines.append(f"已匹配靶点数: {len(matched)}")
    lines.append(f"未匹配靶点数: {len(unmatched)}")
    lines.append(f"匹配率: {len(matched)/(len(matched)+len(unmatched))*100:.2f}%")
    lines.append("")

    # 未匹配靶点按类型统计
    lines.append("## 未匹配靶点按类型统计")
    lines.append("-" * 80)
    for target_type, count in by_type.most_common():
        lines.append(f"{target_type}: {count}")
    lines.append("")

    # 未匹配靶点按数据完整性统计
    lines.append("## 未匹配靶点数据完整性")
    lines.append("-" * 80)
    lines.append(f"有UniProt ID: {len(with_uniprot)}")
    lines.append(f"无UniProt ID: {len(without_uniprot)}")
    lines.append(f"有基因名: {len(with_gene)}")
    lines.append(f"无基因名: {len(without_gene)}")
    lines.append("")

    # 未匹配靶点示例（前30条）
    lines.append("## 未匹配靶点示例（前30条）")
    lines.append("-" * 80)
    for i, target in enumerate(unmatched[:30], 1):
        lines.append(f"{i}. {target['ttd_id']} - {target['target_name']}")
        lines.append(f"   UniProt: {target['uniprot_id']}")
        lines.append(f"   基因名: {target['gene_name']}")
        lines.append(f"   类型: {target['target_type']}")
        lines.append("")

    lines.append("=" * 80)

    return '\n'.join(lines)


def generate_update_sql(matched):
    """生成更新已匹配靶点的SQL脚本"""
    lines = []
    lines.append("-- ============================================================================")
    lines.append("-- 更新已匹配靶点的TTD补充信息")
    lines.append("-- ============================================================================")
    lines.append("-- 注意: 此脚本更新已匹配到的靶点，补充TTD的详细信息")
    lines.append("-- ============================================================================")
    lines.append("")

    lines.append("BEGIN;")
    lines.append("")

    for target in matched:
        target_id = target['target_id']

        # 转义所有单引号并截断过长字段
        gene_name = target['gene_name'].replace("'", "''") if target['gene_name'] else ''
        synonyms = target['synonyms'].replace("'", "''") if target['synonyms'] else ''
        function = target['function'].replace("'", "''") if target['function'] else ''
        pdb_structure = target['pdb_structure'].replace("'", "''") if target['pdb_structure'] else ''
        bioclass = target['bioclass'].replace("'", "''") if target['bioclass'] else ''
        ec_number = target['ec_number'].replace("'", "''") if target['ec_number'] else ''
        sequence = target['sequence'].replace("'", "''") if target['sequence'] else ''
        ttd_id = target['ttd_id'].replace("'", "''") if target['ttd_id'] else ''

        # 截断过长字段（根据数据库schema限制）
        gene_name = gene_name[:100] if gene_name else ''
        ec_number = ec_number[:50] if ec_number else ''
        ttd_id = ttd_id[:50] if ttd_id else ''
        bioclass = bioclass[:200] if bioclass else ''
        pdb_structure = pdb_structure[:500] if pdb_structure else ''

        lines.append(f"-- {target['ttd_id']}: {target['target_name']}")
        lines.append("UPDATE targets SET")

        update_fields = []
        if gene_name:
            update_fields.append(f"    gene_name = '{gene_name}'")
        if synonyms:
            update_fields.append(f"    synonyms = '{synonyms}'")
        if function:
            update_fields.append(f"    function = '{function}'")
        if pdb_structure:
            update_fields.append(f"    pdb_structure = '{pdb_structure}'")
        if bioclass:
            update_fields.append(f"    bioclass = '{bioclass}'")
        if ec_number:
            update_fields.append(f"    ec_number = '{ec_number}'")
        if sequence:
            update_fields.append(f"    sequence = '{sequence}'")
        if ttd_id:
            update_fields.append(f"    ttd_id = '{ttd_id}'")

        lines.append(",\n".join(update_fields))
        lines.append(f"WHERE id = {target_id};")
        lines.append("")

    lines.append("COMMIT;")
    lines.append("")
    lines.append(f"-- 总计更新: {len(matched)} 条记录")

    return '\n'.join(lines)


def generate_create_sql(unmatched):
    """生成创建新靶点的SQL脚本"""
    lines = []
    lines.append("-- ============================================================================")
    lines.append("-- 创建未匹配的TTD靶点记录")
    lines.append("-- ============================================================================")
    lines.append("-- 注意: 此脚本创建完全未匹配的TTD靶点")
    lines.append("-- 建议: 执行前人工审核，确认这些靶点确实不存在于数据库中")
    lines.append("-- ============================================================================")
    lines.append("")

    # 获取当前最大target_id编号
    lines.append("-- 获取当前最大target_id编号")
    lines.append("-- SELECT MAX(CAST(SUBSTRING(target_id FROM 4) AS INTEGER)) FROM targets WHERE target_id LIKE 'TAR%';")
    lines.append("")

    lines.append("BEGIN;")
    lines.append("")

    target_id_counter = 10000  # 从TAR10000开始

    for target in unmatched:
        target_id = f"TAR{target_id_counter:05d}"
        target_id_counter += 1

        # 转义所有单引号并截断过长字段
        target_name = target['target_name'].replace("'", "''") if target['target_name'] else ''
        gene_name = target['gene_name'].replace("'", "''") if target['gene_name'] else ''
        synonyms = target['synonyms'].replace("'", "''") if target['synonyms'] else ''
        function = target['function'].replace("'", "''") if target['function'] else ''
        pdb_structure = target['pdb_structure'].replace("'", "''") if target['pdb_structure'] else ''
        bioclass = target['bioclass'].replace("'", "''") if target['bioclass'] else ''
        ec_number = target['ec_number'].replace("'", "''") if target['ec_number'] else ''
        sequence = target['sequence'].replace("'", "''") if target['sequence'] else ''
        ttd_id = target['ttd_id'].replace("'", "''") if target['ttd_id'] else ''
        uniprot_id = target['uniprot_id'].replace("'", "''") if target['uniprot_id'] else ''

        # 截断过长字段（根据数据库schema限制）
        gene_name = gene_name[:100] if gene_name else ''
        ec_number = ec_number[:50] if ec_number else ''
        ttd_id = ttd_id[:50] if ttd_id else ''
        bioclass = bioclass[:200] if bioclass else ''
        pdb_structure = pdb_structure[:500] if pdb_structure else ''

        # 确定target_type
        target_type = 'Protein'  # 默认为Protein

        lines.append(f"-- {target['ttd_id']}: {target['target_name']}")
        lines.append("INSERT INTO targets (")
        lines.append("    target_id, target_type, target_name, uniprot_id, gene_name,")
        lines.append("    synonyms, function, pdb_structure, bioclass, ec_number, sequence, ttd_id")
        lines.append(") VALUES (")
        lines.append(f"    '{target_id}',")
        lines.append(f"    '{target_type}',")
        lines.append(f"    '{target_name}',")

        # Handle NULL values properly
        uniprot_val = f"'{uniprot_id}'" if uniprot_id else 'NULL'
        gene_val = f"'{gene_name}'" if gene_name else 'NULL'
        synonyms_val = f"'{synonyms}'" if synonyms else 'NULL'
        function_val = f"'{function}'" if function else 'NULL'
        pdb_val = f"'{pdb_structure}'" if pdb_structure else 'NULL'
        bioclass_val = f"'{bioclass}'" if bioclass else 'NULL'
        ec_val = f"'{ec_number}'" if ec_number else 'NULL'
        sequence_val = f"'{sequence}'" if sequence else 'NULL'

        lines.append(f"    {uniprot_val},")
        lines.append(f"    {gene_val},")
        lines.append(f"    {synonyms_val},")
        lines.append(f"    {function_val},")
        lines.append(f"    {pdb_val},")
        lines.append(f"    {bioclass_val},")
        lines.append(f"    {ec_val},")
        lines.append(f"    {sequence_val},")
        lines.append(f"    '{ttd_id}'")
        lines.append(") ON CONFLICT (target_id) DO NOTHING;")
        lines.append("")

    lines.append("COMMIT;")
    lines.append("")
    lines.append(f"-- 总计创建: {len(unmatched)} 条新记录")

    return '\n'.join(lines)


def main():
    print("TTD靶点匹配分析程序")
    print("=" * 80)

    # 分析已匹配靶点
    matched = analyze_matched()

    # 分析未匹配靶点
    unmatched, by_type, with_uniprot, without_uniprot, with_gene, without_gene = analyze_unmatched()

    # 生成分析报告
    print("\n生成分析报告...")
    report = generate_analysis_report(matched, unmatched, by_type, with_uniprot, without_uniprot, with_gene, without_gene)
    with open(ANALYSIS_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"已保存分析报告: {ANALYSIS_OUTPUT}")

    # 生成UPDATE SQL脚本
    print("\n生成UPDATE SQL脚本...")
    update_sql = generate_update_sql(matched)
    with open(UPDATE_SQL_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(update_sql)
    print(f"已保存UPDATE SQL脚本: {UPDATE_SQL_OUTPUT}")

    # 生成CREATE SQL脚本
    print("\n生成CREATE SQL脚本...")
    create_sql = generate_create_sql(unmatched)
    with open(CREATE_SQL_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(create_sql)
    print(f"已保存CREATE SQL脚本: {CREATE_SQL_OUTPUT}")

    # 打印报告
    print("\n" + report)

    print("\n分析完成！")
    print("\n下一步:")
    print("1. 执行UPDATE SQL更新已匹配靶点:")
    print(f"   psql -U yfguo -d npdb -f {UPDATE_SQL_OUTPUT}")
    print("2. 执行CREATE SQL创建新靶点:")
    print(f"   psql -U yfguo -d npdb -f {CREATE_SQL_OUTPUT}")


if __name__ == '__main__':
    main()
