#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMAUP 与 NPASS 物种数据整合
============================
功能: 将 CMAUP Plants.txt 和 NPASS species_info.txt 整合为统一的生物资源数据

匹配策略:
  1. 优先级1: ID精确匹配 (Plant_ID = org_id)
  2. 优先级2: 拉丁名匹配 (Species_Name = species_name)
  3. 优先级3: 种ID匹配 (Species_Tax_ID = species_tax_id)
  4. 优先级4: 属科组合匹配 (Genus_Name + Family_Name = genus_name + family_name)
  5. 优先级5: 属ID匹配 (Genus_Tax_ID = genus_tax_id)

数据合并策略:
  - 匹配成功: 合并两个来源的数据,优先保留NPASS字段,CMAUP作为补充,标记为BOTH
  - NPASS独有: 保留,标记为NPASS
  - CMAUP独有: 保留,标记为CMAUP

输出:
  - bio_resources_integrated.txt: 整合后的TSV文件
  - integration_report.txt: 匹配报告
  - unmatched_cmaup.txt: CMAUP中未匹配的记录
"""

import csv
import os
import re
from collections import defaultdict
from datetime import datetime

# 文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data'
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
CMAUP_FILE = os.path.join(DATA_DIR, 'CMAUP', 'CMAUPv2.0_download_Plants.txt')
NPASS_FILE = os.path.join(DATA_DIR, 'NPASS', 'NPASS3.0_species_info.txt')
INTEGRATED_OUTPUT = os.path.join(OUTPUT_DIR, 'bio_resources_integrated.txt')
REPORT_OUTPUT = os.path.join(OUTPUT_DIR, 'integration_report.txt')
UNMATCHED_OUTPUT = os.path.join(OUTPUT_DIR, 'unmatched_cmaup.txt')

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)


def normalize_value(value):
    """标准化值: 处理NA/n.a./空值"""
    if not value or value in ['NA', 'n.a.', 'N/A', '']:
        return None
    return value.strip()


def normalize_latin_name(name):
    """标准化拉丁名（转小写，去除多余空格）"""
    if not name or name in ['NA', 'n.a.']:
        return ""
    return ' '.join(name.lower().strip().split())


def normalize_id(id_str):
    """标准化ID: 去除变种后缀 (如 NPO5649.1 -> NPO5649)"""
    if not id_str or id_str in ['NA', 'n.a.']:
        return ""
    # 去除 .1, .2 等变种后缀
    return re.sub(r'\.\d+$', '', id_str.strip())


def load_cmaup_data():
    """加载CMAUP植物数据"""
    print(f"加载CMAUP数据: {CMAUP_FILE}")
    cmaup_data = []
    with open(CMAUP_FILE, 'r', encoding='utf-8') as f:
        # 处理可能的\r\n换行符
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            # 清理字段值
            cleaned_row = {k: v.strip() if v else v for k, v in row.items()}
            cmaup_data.append(cleaned_row)

    print(f"已加载 {len(cmaup_data)} 条CMAUP记录")
    return cmaup_data


def load_npass_data():
    """加载NPASS物种数据"""
    print(f"加载NPASS数据: {NPASS_FILE}")
    npass_data = []
    with open(NPASS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            npass_data.append(row)

    print(f"已加载 {len(npass_data)} 条NPASS记录")
    return npass_data


def build_npass_indexes(npass_data):
    """构建NPASS数据的多个索引以加速匹配"""
    print("构建NPASS索引...")

    indexes = {
        'by_org_id': {},           # org_id -> record
        'by_latin_name': {},       # normalized latin name -> record
        'by_species_tax_id': {},   # species_tax_id -> record
        'by_genus_family': {},     # (genus, family) -> record
        'by_genus_tax_id': {}      # genus_tax_id -> record
    }

    for record in npass_data:
        # 索引1: org_id
        org_id = normalize_id(record.get('org_id', ''))
        if org_id:
            indexes['by_org_id'][org_id] = record

        # 索引2: 拉丁名
        latin_name = normalize_latin_name(record.get('species_name', ''))
        if latin_name:
            if latin_name not in indexes['by_latin_name']:
                indexes['by_latin_name'][latin_name] = []
            indexes['by_latin_name'][latin_name].append(record)

        # 索引3: species_tax_id
        species_tax_id = normalize_value(record.get('species_tax_id', ''))
        if species_tax_id:
            if species_tax_id not in indexes['by_species_tax_id']:
                indexes['by_species_tax_id'][species_tax_id] = []
            indexes['by_species_tax_id'][species_tax_id].append(record)

        # 索引4: genus + family
        genus = normalize_latin_name(record.get('genus_name', ''))
        family = normalize_latin_name(record.get('family_name', ''))
        if genus and family:
            key = (genus, family)
            if key not in indexes['by_genus_family']:
                indexes['by_genus_family'][key] = []
            indexes['by_genus_family'][key].append(record)

        # 索引5: genus_tax_id
        genus_tax_id = normalize_value(record.get('genus_tax_id', ''))
        if genus_tax_id:
            if genus_tax_id not in indexes['by_genus_tax_id']:
                indexes['by_genus_tax_id'][genus_tax_id] = []
            indexes['by_genus_tax_id'][genus_tax_id].append(record)

    print(f"索引构建完成:")
    print(f"  - org_id索引: {len(indexes['by_org_id'])} 条")
    print(f"  - 拉丁名索引: {len(indexes['by_latin_name'])} 条")
    print(f"  - species_tax_id索引: {len(indexes['by_species_tax_id'])} 条")
    print(f"  - genus+family索引: {len(indexes['by_genus_family'])} 条")
    print(f"  - genus_tax_id索引: {len(indexes['by_genus_tax_id'])} 条")

    return indexes


def match_cmaup_to_npass(cmaup_record, indexes):
    """
    将CMAUP记录匹配到NPASS记录
    返回: (matched_npass_record, match_method, confidence)
    """
    # 优先级1: ID精确匹配
    plant_id = normalize_id(cmaup_record.get('Plant_ID', ''))
    if plant_id and plant_id in indexes['by_org_id']:
        return indexes['by_org_id'][plant_id], 'id_exact', 'high'

    # 优先级2: 拉丁名匹配
    species_name = normalize_latin_name(cmaup_record.get('Species_Name', ''))
    if species_name and species_name in indexes['by_latin_name']:
        matches = indexes['by_latin_name'][species_name]
        if len(matches) == 1:
            return matches[0], 'latin_name', 'high'
        elif len(matches) > 1:
            # 多个匹配,返回第一个
            return matches[0], 'latin_name_multiple', 'medium'

    # 优先级3: 种ID匹配
    species_tax_id = normalize_value(cmaup_record.get('Species_Tax_ID', ''))
    if species_tax_id and species_tax_id in indexes['by_species_tax_id']:
        matches = indexes['by_species_tax_id'][species_tax_id]
        if len(matches) == 1:
            return matches[0], 'species_tax_id', 'high'
        elif len(matches) > 1:
            return matches[0], 'species_tax_id_multiple', 'medium'

    # 优先级4: 属科组合匹配
    genus = normalize_latin_name(cmaup_record.get('Genus_Name', ''))
    family = normalize_latin_name(cmaup_record.get('Family_Name', ''))
    if genus and family:
        key = (genus, family)
        if key in indexes['by_genus_family']:
            matches = indexes['by_genus_family'][key]
            if len(matches) == 1:
                return matches[0], 'genus_family', 'medium'
            elif len(matches) > 1:
                return matches[0], 'genus_family_multiple', 'low'

    # 优先级5: 属ID匹配
    genus_tax_id = normalize_value(cmaup_record.get('Genus_Tax_ID', ''))
    if genus_tax_id and genus_tax_id in indexes['by_genus_tax_id']:
        matches = indexes['by_genus_tax_id'][genus_tax_id]
        if len(matches) == 1:
            return matches[0], 'genus_tax_id', 'medium'
        elif len(matches) > 1:
            return matches[0], 'genus_tax_id_multiple', 'low'

    return None, 'no_match', 'none'


def merge_records(npass_record, cmaup_record, match_method, confidence):
    """
    合并NPASS和CMAUP记录
    优先保留NPASS字段,CMAUP作为补充
    """
    merged = {}

    # 从NPASS复制所有字段
    for key, value in npass_record.items():
        merged[key] = normalize_value(value)

    # 添加CMAUP补充字段
    merged['cmaup_id'] = normalize_value(cmaup_record.get('Plant_ID', ''))
    merged['cmaup_plant_name'] = normalize_value(cmaup_record.get('Plant_Name', ''))

    # 添加元数据
    merged['data_source'] = 'BOTH'
    merged['match_method'] = match_method
    merged['match_confidence'] = confidence

    return merged


def create_npass_only_record(npass_record):
    """创建NPASS独有记录"""
    merged = {}

    # 从NPASS复制所有字段
    for key, value in npass_record.items():
        merged[key] = normalize_value(value)

    # CMAUP字段为空
    merged['cmaup_id'] = None
    merged['cmaup_plant_name'] = None

    # 元数据
    merged['data_source'] = 'NPASS'
    merged['match_method'] = 'npass_only'
    merged['match_confidence'] = 'high'

    return merged


def create_cmaup_only_record(cmaup_record):
    """创建CMAUP独有记录"""
    merged = {
        # NPASS字段 (从CMAUP映射)
        'org_id': normalize_value(cmaup_record.get('Plant_ID', '')),
        'org_name': normalize_value(cmaup_record.get('Plant_Name', '')),
        'org_tax_level': 'Species',  # 假设都是种级别
        'org_tax_id': normalize_value(cmaup_record.get('Species_Tax_ID', '')),
        'subspecies_tax_id': None,
        'subspecies_name': None,
        'species_tax_id': normalize_value(cmaup_record.get('Species_Tax_ID', '')),
        'species_name': normalize_value(cmaup_record.get('Species_Name', '')),
        'genus_tax_id': normalize_value(cmaup_record.get('Genus_Tax_ID', '')),
        'genus_name': normalize_value(cmaup_record.get('Genus_Name', '')),
        'family_tax_id': normalize_value(cmaup_record.get('Family_Tax_ID', '')),
        'family_name': normalize_value(cmaup_record.get('Family_Name', '')),
        'kingdom_tax_id': None,
        'kingdom_name': None,
        'superkingdom_tax_id': None,
        'superkingdom_name': None,
        'org_name_initial': None,
        'num_of_np_act': None,
        'num_of_np_no_act': None,
        'num_of_np_quantity': None,
        'if_org_coculture': None,
        'if_org_engineered': None,
        'if_org_symbiont': None,

        # CMAUP字段
        'cmaup_id': normalize_value(cmaup_record.get('Plant_ID', '')),
        'cmaup_plant_name': normalize_value(cmaup_record.get('Plant_Name', '')),

        # 元数据
        'data_source': 'CMAUP',
        'match_method': 'cmaup_only',
        'match_confidence': 'high'
    }

    return merged


def integrate_data(cmaup_data, npass_data):
    """
    整合CMAUP和NPASS数据
    """
    print("\n开始数据整合...")

    # 构建NPASS索引
    indexes = build_npass_indexes(npass_data)

    # 统计信息
    stats = {
        'total_cmaup': len(cmaup_data),
        'total_npass': len(npass_data),
        'matched': 0,
        'unmatched_cmaup': 0,
        'npass_only': 0,
        'match_methods': defaultdict(int),
        'confidence_levels': defaultdict(int)
    }

    # 存储结果
    integrated_records = []
    unmatched_cmaup_records = []
    matched_npass_ids = set()

    # 匹配CMAUP到NPASS
    print(f"\n匹配CMAUP记录到NPASS...")
    for idx, cmaup_record in enumerate(cmaup_data, 1):
        if idx % 100 == 0:
            print(f"  进度: {idx}/{len(cmaup_data)}")

        npass_match, match_method, confidence = match_cmaup_to_npass(cmaup_record, indexes)

        if npass_match:
            # 匹配成功
            merged = merge_records(npass_match, cmaup_record, match_method, confidence)
            integrated_records.append(merged)
            matched_npass_ids.add(npass_match['org_id'])
            stats['matched'] += 1
            stats['match_methods'][match_method] += 1
            stats['confidence_levels'][confidence] += 1
        else:
            # 未匹配
            merged = create_cmaup_only_record(cmaup_record)
            integrated_records.append(merged)
            unmatched_cmaup_records.append(cmaup_record)
            stats['unmatched_cmaup'] += 1

    # 添加NPASS独有记录
    print(f"\n添加NPASS独有记录...")
    for npass_record in npass_data:
        if npass_record['org_id'] not in matched_npass_ids:
            merged = create_npass_only_record(npass_record)
            integrated_records.append(merged)
            stats['npass_only'] += 1

    stats['total_integrated'] = len(integrated_records)

    print(f"\n整合完成:")
    print(f"  - 总记录数: {stats['total_integrated']}")
    print(f"  - 匹配成功: {stats['matched']}")
    print(f"  - CMAUP独有: {stats['unmatched_cmaup']}")
    print(f"  - NPASS独有: {stats['npass_only']}")

    return integrated_records, unmatched_cmaup_records, stats


def write_integrated_file(records, output_file):
    """写入整合后的TSV文件"""
    print(f"\n写入整合文件: {output_file}")

    # 定义字段顺序 (移除 data_source, match_method, match_confidence)
    fieldnames = [
        'org_id', 'cmaup_id', 'org_name', 'cmaup_plant_name',
        'org_tax_level', 'org_tax_id',
        'subspecies_tax_id', 'subspecies_name',
        'species_tax_id', 'species_name',
        'genus_tax_id', 'genus_name',
        'family_tax_id', 'family_name',
        'kingdom_tax_id', 'kingdom_name',
        'superkingdom_tax_id', 'superkingdom_name',
        'org_name_initial',
        'num_of_np_act', 'num_of_np_no_act', 'num_of_np_quantity',
        'if_org_coculture', 'if_org_engineered', 'if_org_symbiont'
    ]

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t', extrasaction='ignore')
        writer.writeheader()

        for record in records:
            # 将None转换为空字符串以便输出
            output_record = {k: (v if v is not None else '') for k, v in record.items()}
            writer.writerow(output_record)

    print(f"已写入 {len(records)} 条记录")


def write_unmatched_file(records, output_file):
    """写入未匹配的CMAUP记录"""
    if not records:
        print(f"\n没有未匹配的CMAUP记录")
        return

    print(f"\n写入未匹配CMAUP记录: {output_file}")

    fieldnames = ['Plant_ID', 'Plant_Name', 'Species_Tax_ID', 'Species_Name',
                  'Genus_Tax_ID', 'Genus_Name', 'Family_Tax_ID', 'Family_Name']

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(records)

    print(f"已写入 {len(records)} 条未匹配记录")


def generate_report(stats, unmatched_cmaup_records):
    """生成整合报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("CMAUP 与 NPASS 物种数据整合报告")
    lines.append("=" * 80)
    lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # 总体统计
    lines.append("## 总体统计")
    lines.append(f"CMAUP总记录数: {stats['total_cmaup']}")
    lines.append(f"NPASS总记录数: {stats['total_npass']}")
    lines.append(f"整合后总记录数: {stats['total_integrated']}")
    lines.append("")

    # 数据来源分布
    lines.append("## 数据来源分布")
    lines.append(f"匹配成功 (BOTH): {stats['matched']} ({stats['matched']/stats['total_integrated']*100:.2f}%)")
    lines.append(f"CMAUP独有: {stats['unmatched_cmaup']} ({stats['unmatched_cmaup']/stats['total_integrated']*100:.2f}%)")
    lines.append(f"NPASS独有: {stats['npass_only']} ({stats['npass_only']/stats['total_integrated']*100:.2f}%)")
    lines.append("")

    # 匹配率
    lines.append("## 匹配率")
    match_rate = stats['matched'] / stats['total_cmaup'] * 100 if stats['total_cmaup'] > 0 else 0
    lines.append(f"CMAUP匹配率: {match_rate:.2f}% ({stats['matched']}/{stats['total_cmaup']})")
    lines.append("")

    # 匹配方法统计
    lines.append("## 匹配方法统计")
    for method, count in sorted(stats['match_methods'].items(), key=lambda x: x[1], reverse=True):
        percentage = count / stats['matched'] * 100 if stats['matched'] > 0 else 0
        lines.append(f"{method}: {count} ({percentage:.2f}%)")
    lines.append("")

    # 匹配置信度统计
    lines.append("## 匹配置信度统计")
    for confidence, count in sorted(stats['confidence_levels'].items(), key=lambda x: x[1], reverse=True):
        percentage = count / stats['matched'] * 100 if stats['matched'] > 0 else 0
        lines.append(f"{confidence}: {count} ({percentage:.2f}%)")
    lines.append("")

    # 未匹配CMAUP记录示例
    if unmatched_cmaup_records:
        lines.append("## 未匹配CMAUP记录示例 (前20条)")
        lines.append("-" * 80)
        for record in unmatched_cmaup_records[:20]:
            lines.append(f"Plant_ID: {record.get('Plant_ID', 'N/A')}")
            lines.append(f"  Plant_Name: {record.get('Plant_Name', 'N/A')}")
            lines.append(f"  Species_Name: {record.get('Species_Name', 'N/A')}")
            lines.append(f"  Genus_Name: {record.get('Genus_Name', 'N/A')}")
            lines.append(f"  Family_Name: {record.get('Family_Name', 'N/A')}")
            lines.append("")

    lines.append("=" * 80)
    lines.append("")
    lines.append("## 输出文件")
    lines.append(f"- 整合数据: {INTEGRATED_OUTPUT}")
    lines.append(f"- 未匹配CMAUP: {UNMATCHED_OUTPUT}")
    lines.append(f"- 本报告: {REPORT_OUTPUT}")
    lines.append("")
    lines.append("=" * 80)

    return '\n'.join(lines)


def main():
    print("=" * 80)
    print("CMAUP 与 NPASS 物种数据整合程序")
    print("=" * 80)

    # 加载数据
    cmaup_data = load_cmaup_data()
    npass_data = load_npass_data()

    # 整合数据
    integrated_records, unmatched_cmaup_records, stats = integrate_data(cmaup_data, npass_data)

    # 写入整合文件
    write_integrated_file(integrated_records, INTEGRATED_OUTPUT)

    # 写入未匹配文件
    write_unmatched_file(unmatched_cmaup_records, UNMATCHED_OUTPUT)

    # 生成报告
    report = generate_report(stats, unmatched_cmaup_records)
    with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n已保存整合报告: {REPORT_OUTPUT}")

    # 打印报告
    print("\n" + report)

    print("\n整合完成！")
    print(f"\n请检查以下文件:")
    print(f"  1. {INTEGRATED_OUTPUT}")
    print(f"  2. {REPORT_OUTPUT}")
    print(f"  3. {UNMATCHED_OUTPUT}")


if __name__ == '__main__':
    main()

