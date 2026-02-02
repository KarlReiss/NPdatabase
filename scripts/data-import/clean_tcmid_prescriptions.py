#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCMID处方数据清洗
==================
功能: 清洗TCMID处方数据，生成中间JSON文件
输入:
  - prescription_basic_info.csv
  - prescription_herbs.csv
输出:
  - cleaned_prescriptions.json
  - cleaned_prescription_herbs.json
  - tcmid_cleaning_report.txt
"""

import csv
import json
import os
import re
from collections import defaultdict

# 文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data/TCMID'
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
BASIC_INFO_FILE = os.path.join(DATA_DIR, 'prescription_basic_info.csv')
HERBS_FILE = os.path.join(DATA_DIR, 'prescription_herbs.csv')
CLEANED_PRESCRIPTIONS_OUTPUT = os.path.join(OUTPUT_DIR, 'cleaned_prescriptions.json')
CLEANED_HERBS_OUTPUT = os.path.join(OUTPUT_DIR, 'cleaned_prescription_herbs.json')
REPORT_OUTPUT = os.path.join(OUTPUT_DIR, 'tcmid_cleaning_report.txt')

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)


def parse_icd11_codes(icd11_str):
    """
    解析ICD-11编码字符串
    例如: "CA42 [Acute bronchitis, 急性支气管炎 ];"
    返回: [{'code': 'CA42', 'name_en': 'Acute bronchitis', 'name_zh': '急性支气管炎'}]
    """
    if not icd11_str or icd11_str.strip() == '':
        return []

    codes = []
    # 分割多个ICD-11编码（用分号分隔）
    parts = icd11_str.split(';')

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 匹配格式: CODE [Name_EN, Name_ZH]
        match = re.match(r'([A-Z0-9\.]+)\s*\[([^\]]+)\]', part)
        if match:
            code = match.group(1).strip()
            names = match.group(2).strip()

            # 分割英文名和中文名
            name_parts = names.split(',')
            name_en = name_parts[0].strip() if len(name_parts) > 0 else ''
            name_zh = name_parts[1].strip() if len(name_parts) > 1 else ''

            codes.append({
                'code': code,
                'name_en': name_en,
                'name_zh': name_zh
            })

    return codes


def clean_prescriptions(basic_info_file):
    """清洗处方基本信息"""
    print("清洗处方基本信息...")

    cleaned = []
    stats = {
        'total': 0,
        'with_icd11': 0,
        'with_tissues': 0,
        'with_reference': 0,
        'empty_fields': defaultdict(int)
    }

    with open(basic_info_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stats['total'] += 1

            # 解析ICD-11编码
            icd11_codes = parse_icd11_codes(row['DiseaseICD11Category'])

            # 清洗数据
            prescription = {
                'prescription_id': row['PrescriptionID'].strip(),
                'pinyin_name': row['PinyinName'].strip(),
                'chinese_name': row['ChineseName'].strip(),
                'english_name': row['EnglishName'].strip(),
                'function_description': row['FunctionDescription'].strip(),
                'indications': row['Indications'].strip(),
                'icd11_codes': icd11_codes,
                'icd11_category': row['DiseaseICD11Category'].strip(),
                'human_tissues': row['HumanTissues'].strip(),
                'reference': row['Reference'].strip(),
                'reference_book': row['ReferenceBook'].strip()
            }

            # 统计
            if icd11_codes:
                stats['with_icd11'] += 1
            if prescription['human_tissues']:
                stats['with_tissues'] += 1
            if prescription['reference'] or prescription['reference_book']:
                stats['with_reference'] += 1

            # 统计空字段
            for key, value in prescription.items():
                if key == 'icd11_codes':
                    if not value:
                        stats['empty_fields'][key] += 1
                elif not value:
                    stats['empty_fields'][key] += 1

            cleaned.append(prescription)

    print(f"已清洗 {len(cleaned)} 条处方记录")
    return cleaned, stats


def clean_prescription_herbs(herbs_file):
    """清洗处方药材信息"""
    print("清洗处方药材信息...")

    cleaned = []
    stats = {
        'total': 0,
        'with_latin_name': 0,
        'with_chinese_name': 0,
        'with_quantity': 0,
        'with_barcode': 0,
        'empty_fields': defaultdict(int)
    }

    with open(herbs_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stats['total'] += 1

            # 清洗数据
            herb = {
                'prescription_id': row['PrescriptionID'].strip(),
                'component_id': row['ComponentID'].strip(),
                'latin_name': row['LatinName'].strip(),
                'chinese_name': row['ChineseName'].strip(),
                'quantity': row['ComponentQuantity'].strip(),
                'barcode': row['Barcode'].strip()
            }

            # 统计
            if herb['latin_name']:
                stats['with_latin_name'] += 1
            if herb['chinese_name']:
                stats['with_chinese_name'] += 1
            if herb['quantity']:
                stats['with_quantity'] += 1
            if herb['barcode']:
                stats['with_barcode'] += 1

            # 统计空字段
            for key, value in herb.items():
                if not value:
                    stats['empty_fields'][key] += 1

            cleaned.append(herb)

    print(f"已清洗 {len(cleaned)} 条药材记录")
    return cleaned, stats


def generate_report(prescription_stats, herb_stats):
    """生成清洗报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("TCMID处方数据清洗报告")
    lines.append("=" * 80)
    lines.append("")

    # 处方基本信息统计
    lines.append("## 处方基本信息统计")
    lines.append(f"总处方数: {prescription_stats['total']}")
    lines.append(f"有ICD-11编码: {prescription_stats['with_icd11']} ({prescription_stats['with_icd11']/prescription_stats['total']*100:.2f}%)")
    lines.append(f"有人体组织信息: {prescription_stats['with_tissues']} ({prescription_stats['with_tissues']/prescription_stats['total']*100:.2f}%)")
    lines.append(f"有参考文献: {prescription_stats['with_reference']} ({prescription_stats['with_reference']/prescription_stats['total']*100:.2f}%)")
    lines.append("")

    lines.append("### 空字段统计（处方）")
    for field, count in sorted(prescription_stats['empty_fields'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {field}: {count} ({count/prescription_stats['total']*100:.2f}%)")
    lines.append("")

    # 药材信息统计
    lines.append("## 药材信息统计")
    lines.append(f"总药材记录数: {herb_stats['total']}")
    lines.append(f"有拉丁名: {herb_stats['with_latin_name']} ({herb_stats['with_latin_name']/herb_stats['total']*100:.2f}%)")
    lines.append(f"有中文名: {herb_stats['with_chinese_name']} ({herb_stats['with_chinese_name']/herb_stats['total']*100:.2f}%)")
    lines.append(f"有用量: {herb_stats['with_quantity']} ({herb_stats['with_quantity']/herb_stats['total']*100:.2f}%)")
    lines.append(f"有条形码: {herb_stats['with_barcode']} ({herb_stats['with_barcode']/herb_stats['total']*100:.2f}%)")
    lines.append("")

    lines.append("### 空字段统计（药材）")
    for field, count in sorted(herb_stats['empty_fields'].items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {field}: {count} ({count/herb_stats['total']*100:.2f}%)")
    lines.append("")

    lines.append("=" * 80)

    return '\n'.join(lines)


def main():
    print("TCMID处方数据清洗程序")
    print("=" * 80)

    # 清洗处方基本信息
    cleaned_prescriptions, prescription_stats = clean_prescriptions(BASIC_INFO_FILE)

    # 清洗药材信息
    cleaned_herbs, herb_stats = clean_prescription_herbs(HERBS_FILE)

    # 保存清洗后的数据
    print("\n保存清洗后的数据...")
    with open(CLEANED_PRESCRIPTIONS_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(cleaned_prescriptions, f, ensure_ascii=False, indent=2)
    print(f"已保存处方数据: {CLEANED_PRESCRIPTIONS_OUTPUT}")

    with open(CLEANED_HERBS_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(cleaned_herbs, f, ensure_ascii=False, indent=2)
    print(f"已保存药材数据: {CLEANED_HERBS_OUTPUT}")

    # 生成报告
    report = generate_report(prescription_stats, herb_stats)
    with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"已保存清洗报告: {REPORT_OUTPUT}")

    # 打印报告
    print("\n" + report)

    print("\n清洗完成！")


if __name__ == '__main__':
    main()
