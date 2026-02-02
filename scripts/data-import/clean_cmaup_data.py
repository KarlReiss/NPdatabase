#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMAUP疾病数据清洗
==================
功能: 清洗CMAUP植物-疾病关联数据，生成中间JSON文件
输入:
  - CMAUPv2.0_download_Plant_Human_Disease_Associations.txt
输出:
  - cleaned_diseases.json (去重后的疾病列表)
  - cleaned_plant_disease_associations.json (植物-疾病关联)
  - cmaup_cleaning_report.txt
"""

import csv
import json
import os
from collections import defaultdict

# 文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data/CMAUP'
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
ASSOCIATIONS_FILE = os.path.join(DATA_DIR, 'CMAUPv2.0_download_Plant_Human_Disease_Associations.txt')
CLEANED_DISEASES_OUTPUT = os.path.join(OUTPUT_DIR, 'cleaned_diseases.json')
CLEANED_ASSOCIATIONS_OUTPUT = os.path.join(OUTPUT_DIR, 'cleaned_plant_disease_associations.json')
REPORT_OUTPUT = os.path.join(OUTPUT_DIR, 'cmaup_cleaning_report.txt')

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_associations(associations_file):
    """清洗植物-疾病关联数据"""
    print("清洗植物-疾病关联数据...")

    associations = []
    diseases_dict = {}  # 用于去重疾病
    stats = {
        'total': 0,
        'with_therapeutic_target': 0,
        'with_transcriptome': 0,
        'with_clinical_trial_plant': 0,
        'with_clinical_trial_ingredient': 0,
        'unique_plants': set(),
        'unique_diseases': set(),
        'disease_categories': defaultdict(int)
    }

    with open(associations_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for idx, row in enumerate(reader, 1):
            if idx % 10000 == 0:
                print(f"进度: {idx} 条记录")

            stats['total'] += 1

            # 清洗关联数据
            plant_id = row['Plant_ID'].strip()
            icd11_code = row['ICD-11 Code'].strip()
            disease_category = row['Disease_Category'].strip()
            disease_name = row['Disease'].strip()

            # 证据字段
            therapeutic_target = row['Association_by_Therapeutic_Target'].strip()
            transcriptome = row['Association_by_Disease_Transcriptiome_Reversion'].strip()
            clinical_trial_plant = row['Association_by_Clinical_Trials_of_Plant'].strip()
            clinical_trial_ingredient = row['Association_by_Clinical_Trials_of_Plant_Ingredients'].strip()

            # 处理n.a.值
            therapeutic_target = None if therapeutic_target == 'n.a.' else therapeutic_target
            transcriptome = False if transcriptome == 'n.a.' else True
            clinical_trial_plant = None if clinical_trial_plant == 'n.a.' else clinical_trial_plant
            clinical_trial_ingredient = None if clinical_trial_ingredient == 'n.a.' else clinical_trial_ingredient

            # 统计
            if therapeutic_target:
                stats['with_therapeutic_target'] += 1
            if transcriptome:
                stats['with_transcriptome'] += 1
            if clinical_trial_plant:
                stats['with_clinical_trial_plant'] += 1
            if clinical_trial_ingredient:
                stats['with_clinical_trial_ingredient'] += 1

            stats['unique_plants'].add(plant_id)
            stats['unique_diseases'].add(icd11_code)
            stats['disease_categories'][disease_category] += 1

            # 保存关联
            association = {
                'plant_id': plant_id,
                'icd11_code': icd11_code,
                'evidence_therapeutic_target': therapeutic_target,
                'evidence_transcriptome': transcriptome,
                'evidence_clinical_trial_plant': clinical_trial_plant,
                'evidence_clinical_trial_ingredient': clinical_trial_ingredient
            }
            associations.append(association)

            # 保存疾病信息（去重）
            if icd11_code not in diseases_dict:
                diseases_dict[icd11_code] = {
                    'icd11_code': icd11_code,
                    'disease_category': disease_category,
                    'disease_name': disease_name
                }

    print(f"已清洗 {len(associations)} 条关联记录")
    print(f"去重后疾病数: {len(diseases_dict)}")

    # 转换为列表
    diseases = list(diseases_dict.values())

    return associations, diseases, stats


def calculate_confidence_score(association):
    """
    计算置信度评分（0-1）
    基于证据类型数量
    """
    score = 0.0
    evidence_count = 0

    if association['evidence_therapeutic_target']:
        evidence_count += 1
        score += 0.3  # 治疗靶点证据权重最高

    if association['evidence_transcriptome']:
        evidence_count += 1
        score += 0.2  # 转录组证据

    if association['evidence_clinical_trial_plant']:
        evidence_count += 1
        score += 0.25  # 植物临床试验

    if association['evidence_clinical_trial_ingredient']:
        evidence_count += 1
        score += 0.25  # 成分临床试验

    # 归一化到0-1
    if evidence_count > 0:
        return min(score, 1.0)
    else:
        return 0.0


def add_confidence_scores(associations):
    """为所有关联添加置信度评分"""
    print("计算置信度评分...")
    for assoc in associations:
        assoc['confidence_score'] = calculate_confidence_score(assoc)
    return associations


def generate_report(stats, diseases_count):
    """生成清洗报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("CMAUP疾病数据清洗报告")
    lines.append("=" * 80)
    lines.append("")

    # 总体统计
    lines.append("## 总体统计")
    lines.append(f"总关联记录数: {stats['total']:,}")
    lines.append(f"唯一植物数: {len(stats['unique_plants']):,}")
    lines.append(f"唯一疾病数: {len(stats['unique_diseases']):,}")
    lines.append(f"去重后疾病数: {diseases_count:,}")
    lines.append("")

    # 证据类型统计
    lines.append("## 证据类型统计")
    lines.append(f"有治疗靶点证据: {stats['with_therapeutic_target']:,} ({stats['with_therapeutic_target']/stats['total']*100:.2f}%)")
    lines.append(f"有转录组证据: {stats['with_transcriptome']:,} ({stats['with_transcriptome']/stats['total']*100:.2f}%)")
    lines.append(f"有植物临床试验: {stats['with_clinical_trial_plant']:,} ({stats['with_clinical_trial_plant']/stats['total']*100:.2f}%)")
    lines.append(f"有成分临床试验: {stats['with_clinical_trial_ingredient']:,} ({stats['with_clinical_trial_ingredient']/stats['total']*100:.2f}%)")
    lines.append("")

    # 疾病分类统计（Top 10）
    lines.append("## 疾病分类统计（Top 10）")
    sorted_categories = sorted(stats['disease_categories'].items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories[:10]:
        lines.append(f"  {category}: {count:,} ({count/stats['total']*100:.2f}%)")
    lines.append("")

    lines.append("=" * 80)

    return '\n'.join(lines)


def main():
    print("CMAUP疾病数据清洗程序")
    print("=" * 80)

    # 清洗关联数据
    associations, diseases, stats = clean_associations(ASSOCIATIONS_FILE)

    # 添加置信度评分
    associations = add_confidence_scores(associations)

    # 保存清洗后的数据
    print("\n保存清洗后的数据...")
    with open(CLEANED_DISEASES_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(diseases, f, ensure_ascii=False, indent=2)
    print(f"已保存疾病数据: {CLEANED_DISEASES_OUTPUT}")

    with open(CLEANED_ASSOCIATIONS_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(associations, f, ensure_ascii=False, indent=2)
    print(f"已保存关联数据: {CLEANED_ASSOCIATIONS_OUTPUT}")

    # 生成报告
    report = generate_report(stats, len(diseases))
    with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"已保存清洗报告: {REPORT_OUTPUT}")

    # 打印报告
    print("\n" + report)

    print("\n清洗完成！")


if __name__ == '__main__':
    main()
