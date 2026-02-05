#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整合 bio_resources_integrated.txt 与 prescription_herbs.csv

功能:
1. 加载两个数据源
2. 通过拉丁名和中文名进行匹配
3. 生成三个输出文件:
   - bio_resources_with_tcmid.txt: 整合后的生物资源表
   - prescription_resources_data.txt: 处方-生物资源关联数据
   - unmatched_prescription_herbs.csv: 未匹配的药材记录
4. 生成匹配报告

作者: Claude Code
日期: 2026-02-05
"""

import pandas as pd
import os
from collections import defaultdict
from datetime import datetime

# 文件路径配置
BASE_DIR = "/home/yfguo/NPdatabase"
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
TCMID_DIR = os.path.join(DATA_DIR, "TCMID")
OUTPUT_DIR = PROCESSED_DIR
SCRIPT_OUTPUT_DIR = os.path.join(BASE_DIR, "scripts/data-import/output")

# 输入文件
BIO_RESOURCES_FILE = os.path.join(SCRIPT_OUTPUT_DIR, "bio_resources_integrated.txt")
PRESCRIPTION_HERBS_FILE = os.path.join(TCMID_DIR, "prescription_herbs.csv")

# 输出文件
OUTPUT_BIO_RESOURCES = os.path.join(OUTPUT_DIR, "bio_resources_with_tcmid.txt")
OUTPUT_PRESCRIPTION_RESOURCES = os.path.join(OUTPUT_DIR, "prescription_resources_data.txt")
OUTPUT_UNMATCHED = os.path.join(OUTPUT_DIR, "unmatched_prescription_herbs.csv")
OUTPUT_REPORT = os.path.join(OUTPUT_DIR, "tcmid_integration_report.txt")


def normalize_name(name):
    """标准化名称: 转小写、去除多余空格"""
    if pd.isna(name) or name == "":
        return ""
    return str(name).strip().lower()


def load_bio_resources(file_path):
    """加载 bio_resources_integrated.txt"""
    print(f"正在加载 {file_path}...")
    df = pd.read_csv(file_path, sep='\t', encoding='utf-8', low_memory=False)
    print(f"  加载完成: {len(df)} 条记录")
    print(f"  字段数: {len(df.columns)}")
    return df


def load_prescription_herbs(file_path):
    """加载 prescription_herbs.csv"""
    print(f"正在加载 {file_path}...")
    # 处理 BOM
    df = pd.read_csv(file_path, encoding='utf-8-sig', low_memory=False)
    print(f"  加载完成: {len(df)} 条记录")
    print(f"  字段数: {len(df.columns)}")
    return df


def build_matching_index(bio_resources_df):
    """构建匹配索引（仅拉丁名）

    返回:
        dict: {normalized_name: [org_id1, org_id2, ...]}
    """
    print("正在构建匹配索引（仅拉丁名）...")

    # 拉丁名索引 (species_name)
    species_index = defaultdict(list)
    # 拉丁名索引 (org_name)
    org_name_index = defaultdict(list)

    for idx, row in bio_resources_df.iterrows():
        org_id = row['org_id']

        # 索引 species_name
        if pd.notna(row.get('species_name')):
            normalized = normalize_name(row['species_name'])
            if normalized:
                species_index[normalized].append(org_id)

        # 索引 org_name (拉丁名)
        if pd.notna(row.get('org_name')):
            normalized = normalize_name(row['org_name'])
            if normalized:
                org_name_index[normalized].append(org_id)

    print(f"  species_name 索引: {len(species_index)} 个唯一名称")
    print(f"  org_name 索引: {len(org_name_index)} 个唯一名称")

    return {
        'species': species_index,
        'org_name': org_name_index
    }


def match_prescription_herbs(prescription_herbs_df, bio_resources_df, indexes):
    """匹配 prescription_herbs 与 bio_resources（仅使用拉丁名）

    返回:
        tuple: (matched_records, unmatched_records, match_stats)
    """
    print("正在匹配 prescription_herbs 与 bio_resources（仅使用拉丁名）...")

    matched_records = []
    unmatched_records = []
    match_stats = {
        'total': len(prescription_herbs_df),
        'matched': 0,
        'unmatched': 0,
        'by_species_name': 0,
        'by_org_name': 0
    }

    for idx, row in prescription_herbs_df.iterrows():
        prescription_id = row['PrescriptionID']
        component_id = row['ComponentID']
        latin_name = row['LatinName']
        chinese_name = row['ChineseName']
        barcode = row.get('Barcode', '')

        matched_org_ids = []
        match_method = None

        # 优先级1: 拉丁名匹配 (species_name)
        if pd.notna(latin_name):
            normalized_latin = normalize_name(latin_name)
            if normalized_latin in indexes['species']:
                matched_org_ids = indexes['species'][normalized_latin]
                match_method = 'species_name'
                match_stats['by_species_name'] += 1

        # 优先级2: 拉丁名匹配 (org_name)
        if not matched_org_ids and pd.notna(latin_name):
            normalized_latin = normalize_name(latin_name)
            if normalized_latin in indexes['org_name']:
                matched_org_ids = indexes['org_name'][normalized_latin]
                match_method = 'org_name'
                match_stats['by_org_name'] += 1

        # 记录匹配结果
        if matched_org_ids:
            match_stats['matched'] += 1
            for org_id in matched_org_ids:
                matched_records.append({
                    'prescription_id': prescription_id,
                    'component_id': component_id,
                    'bio_resource_id': org_id,
                    'barcode': barcode,
                    'match_method': match_method,
                    'latin_name': latin_name,
                    'chinese_name': chinese_name
                })
        else:
            match_stats['unmatched'] += 1
            unmatched_records.append(row.to_dict())

    print(f"  匹配完成:")
    print(f"    总记录数: {match_stats['total']}")
    print(f"    匹配成功: {match_stats['matched']} ({match_stats['matched']/match_stats['total']*100:.2f}%)")
    print(f"    未匹配: {match_stats['unmatched']} ({match_stats['unmatched']/match_stats['total']*100:.2f}%)")
    print(f"    按 species_name 匹配: {match_stats['by_species_name']}")
    print(f"    按 org_name 匹配: {match_stats['by_org_name']}")

    return matched_records, unmatched_records, match_stats


def generate_bio_resources_with_tcmid(bio_resources_df, matched_records):
    """生成 bio_resources_with_tcmid.txt

    为每个 bio_resource 添加 tcmid_component_id 和 tcmid_chinese_name 字段
    """
    print("正在生成 bio_resources_with_tcmid.txt...")

    # 构建 org_id -> component_ids 映射
    org_to_components = defaultdict(set)
    # 构建 org_id -> chinese_names 映射
    org_to_chinese_names = defaultdict(set)

    for record in matched_records:
        org_id = record['bio_resource_id']
        component_id = record['component_id']
        chinese_name = record.get('chinese_name', '')

        org_to_components[org_id].add(component_id)
        if chinese_name and pd.notna(chinese_name):
            org_to_chinese_names[org_id].add(chinese_name)

    # 添加 tcmid_component_id 和 tcmid_chinese_name 列
    tcmid_component_ids = []
    tcmid_chinese_names = []

    for idx, row in bio_resources_df.iterrows():
        org_id = row['org_id']

        # 添加 component_id
        if org_id in org_to_components:
            # 多个 component_id 用逗号分隔
            component_ids = sorted(org_to_components[org_id])
            tcmid_component_ids.append(','.join(component_ids))
        else:
            tcmid_component_ids.append('')

        # 添加 chinese_name
        if org_id in org_to_chinese_names:
            # 多个中文名用逗号分隔
            chinese_names = sorted(org_to_chinese_names[org_id])
            tcmid_chinese_names.append(','.join(chinese_names))
        else:
            tcmid_chinese_names.append('')

    # 添加新列
    result_df = bio_resources_df.copy()
    result_df['tcmid_component_id'] = tcmid_component_ids
    result_df['tcmid_chinese_name'] = tcmid_chinese_names

    print(f"  生成完成: {len(result_df)} 条记录")
    print(f"  其中 {sum(1 for x in tcmid_component_ids if x)} 条有 TCMID Component ID")
    print(f"  其中 {sum(1 for x in tcmid_chinese_names if x)} 条有 TCMID 中文名")

    return result_df


def generate_prescription_resources_data(matched_records):
    """生成 prescription_resources_data.txt"""
    print("正在生成 prescription_resources_data.txt...")

    # 转换为 DataFrame
    df = pd.DataFrame(matched_records)

    # 选择需要的列
    result_df = df[['prescription_id', 'component_id', 'bio_resource_id', 'barcode']].copy()

    # 去重 (可能有重复的关联)
    result_df = result_df.drop_duplicates()

    print(f"  生成完成: {len(result_df)} 条记录")

    return result_df


def generate_unmatched_herbs(unmatched_records):
    """生成 unmatched_prescription_herbs.csv"""
    print("正在生成 unmatched_prescription_herbs.csv...")

    df = pd.DataFrame(unmatched_records)

    print(f"  生成完成: {len(df)} 条记录")

    return df


def generate_report(match_stats, bio_resources_df, matched_records, unmatched_records):
    """生成整合报告"""
    print("正在生成整合报告...")

    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("TCMID 与 Bio Resources 整合报告")
    report_lines.append("=" * 80)
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # 数据源统计
    report_lines.append("## 数据源统计")
    report_lines.append("-" * 80)
    report_lines.append(f"bio_resources_integrated.txt: {len(bio_resources_df)} 条记录")
    report_lines.append(f"prescription_herbs.csv: {match_stats['total']} 条记录")
    report_lines.append("")

    # 匹配统计
    report_lines.append("## 匹配统计")
    report_lines.append("-" * 80)
    report_lines.append(f"总记录数: {match_stats['total']}")
    report_lines.append(f"匹配成功: {match_stats['matched']} ({match_stats['matched']/match_stats['total']*100:.2f}%)")
    report_lines.append(f"未匹配: {match_stats['unmatched']} ({match_stats['unmatched']/match_stats['total']*100:.2f}%)")
    report_lines.append("")

    # 匹配方法分布
    report_lines.append("## 匹配方法分布")
    report_lines.append("-" * 80)
    report_lines.append(f"按 species_name 匹配: {match_stats['by_species_name']} ({match_stats['by_species_name']/match_stats['matched']*100:.2f}%)")
    report_lines.append(f"按 org_name 匹配: {match_stats['by_org_name']} ({match_stats['by_org_name']/match_stats['matched']*100:.2f}%)")
    report_lines.append("")

    # 输出文件统计
    report_lines.append("## 输出文件统计")
    report_lines.append("-" * 80)
    report_lines.append(f"bio_resources_with_tcmid.txt: {len(bio_resources_df)} 条记录 (27 个字段)")
    report_lines.append(f"prescription_resources_data.txt: {len(matched_records)} 条记录 (4 个字段)")
    report_lines.append(f"unmatched_prescription_herbs.csv: {len(unmatched_records)} 条记录")
    report_lines.append("")

    # 数据质量分析
    report_lines.append("## 数据质量分析")
    report_lines.append("-" * 80)

    # 统计有 TCMID Component ID 的 bio_resources
    matched_org_ids = set(r['bio_resource_id'] for r in matched_records)
    report_lines.append(f"有 TCMID Component ID 的 bio_resources: {len(matched_org_ids)} ({len(matched_org_ids)/len(bio_resources_df)*100:.2f}%)")

    # 统计每个 bio_resource 对应的 component 数量
    org_to_components = defaultdict(set)
    for record in matched_records:
        org_to_components[record['bio_resource_id']].add(record['component_id'])

    component_counts = [len(components) for components in org_to_components.values()]
    if component_counts:
        report_lines.append(f"每个 bio_resource 平均对应 {sum(component_counts)/len(component_counts):.2f} 个 TCMID Component")
        report_lines.append(f"最多对应 {max(component_counts)} 个 TCMID Component")

    report_lines.append("")

    # 未匹配记录分析
    if unmatched_records:
        report_lines.append("## 未匹配记录分析")
        report_lines.append("-" * 80)

        # 统计未匹配的拉丁名
        unmatched_latin_names = set()
        unmatched_chinese_names = set()
        for record in unmatched_records:
            if pd.notna(record.get('LatinName')):
                unmatched_latin_names.add(record['LatinName'])
            if pd.notna(record.get('ChineseName')):
                unmatched_chinese_names.add(record['ChineseName'])

        report_lines.append(f"未匹配的唯一拉丁名: {len(unmatched_latin_names)}")
        report_lines.append(f"未匹配的唯一中文名: {len(unmatched_chinese_names)}")

        # 显示前10个未匹配的拉丁名
        if unmatched_latin_names:
            report_lines.append("")
            report_lines.append("前10个未匹配的拉丁名:")
            for name in sorted(unmatched_latin_names)[:10]:
                report_lines.append(f"  - {name}")

    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append("报告结束")
    report_lines.append("=" * 80)

    report_text = "\n".join(report_lines)

    print("  报告生成完成")

    return report_text


def main():
    """主函数"""
    print("=" * 80)
    print("TCMID 与 Bio Resources 整合脚本")
    print("=" * 80)
    print()

    # 1. 加载数据
    bio_resources_df = load_bio_resources(BIO_RESOURCES_FILE)
    prescription_herbs_df = load_prescription_herbs(PRESCRIPTION_HERBS_FILE)
    print()

    # 2. 构建匹配索引
    indexes = build_matching_index(bio_resources_df)
    print()

    # 3. 匹配
    matched_records, unmatched_records, match_stats = match_prescription_herbs(
        prescription_herbs_df, bio_resources_df, indexes
    )
    print()

    # 4. 生成输出文件
    # 4.1 bio_resources_with_tcmid.txt
    bio_resources_with_tcmid = generate_bio_resources_with_tcmid(bio_resources_df, matched_records)
    bio_resources_with_tcmid.to_csv(OUTPUT_BIO_RESOURCES, sep='\t', index=False, encoding='utf-8')
    print(f"  已保存到: {OUTPUT_BIO_RESOURCES}")
    print()

    # 4.2 prescription_resources_data.txt
    prescription_resources_data = generate_prescription_resources_data(matched_records)
    prescription_resources_data.to_csv(OUTPUT_PRESCRIPTION_RESOURCES, sep='\t', index=False, encoding='utf-8')
    print(f"  已保存到: {OUTPUT_PRESCRIPTION_RESOURCES}")
    print()

    # 4.3 unmatched_prescription_herbs.csv
    unmatched_herbs = generate_unmatched_herbs(unmatched_records)
    unmatched_herbs.to_csv(OUTPUT_UNMATCHED, index=False, encoding='utf-8')
    print(f"  已保存到: {OUTPUT_UNMATCHED}")
    print()

    # 5. 生成报告
    report_text = generate_report(match_stats, bio_resources_df, matched_records, unmatched_records)
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"  已保存到: {OUTPUT_REPORT}")
    print()

    print("=" * 80)
    print("整合完成!")
    print("=" * 80)
    print()
    print("输出文件:")
    print(f"  1. {OUTPUT_BIO_RESOURCES}")
    print(f"  2. {OUTPUT_PRESCRIPTION_RESOURCES}")
    print(f"  3. {OUTPUT_UNMATCHED}")
    print(f"  4. {OUTPUT_REPORT}")
    print()


if __name__ == "__main__":
    main()
