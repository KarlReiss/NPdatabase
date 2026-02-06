#!/usr/bin/env python3
"""
测试植物-疾病关联数据映射情况
检查 Plant_ID 和 ICD-11 Code 的映射覆盖率
"""

import pandas as pd
import psycopg2
from collections import Counter

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': 'yfguo',
    'host': 'localhost',
    'port': 5432
}

# 数据文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data'
CMAUP_ASSOCIATIONS = f'{DATA_DIR}/CMAUP/CMAUPv2.0_download_Plant_Human_Disease_Associations.txt'


def clean_value(val):
    """清理数据值"""
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in ('n.a.', 'n.a', 'na', '', '-'):
            return None
    return val


def main():
    print("=" * 80)
    print("植物-疾病关联数据映射测试")
    print("=" * 80)

    # 连接数据库
    print("\n1. 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 加载生物资源映射
    print("\n2. 加载生物资源映射...")
    cursor.execute("SELECT resource_id FROM bio_resources WHERE resource_id IS NOT NULL")
    bio_resource_ids = {row[0] for row in cursor.fetchall()}
    print(f"   数据库中的生物资源数: {len(bio_resource_ids)}")

    # 加载疾病映射
    print("\n3. 加载疾病映射...")
    cursor.execute("SELECT icd11_code FROM diseases WHERE icd11_code IS NOT NULL")
    disease_codes = {row[0] for row in cursor.fetchall()}
    print(f"   数据库中的疾病数: {len(disease_codes)}")

    # 加载关联数据
    print("\n4. 加载关联数据...")
    df = pd.read_csv(CMAUP_ASSOCIATIONS, sep='\t', dtype=str)
    print(f"   关联记录总数: {len(df)}")

    # 分析 Plant_ID 映射
    print("\n5. 分析 Plant_ID 映射...")
    plant_ids = [clean_value(x) for x in df['Plant_ID'].unique() if clean_value(x)]
    plant_id_counter = Counter(df['Plant_ID'].apply(clean_value))

    matched_plants = [pid for pid in plant_ids if pid in bio_resource_ids]
    unmatched_plants = [pid for pid in plant_ids if pid not in bio_resource_ids]

    print(f"   唯一植物ID数: {len(plant_ids)}")
    print(f"   可映射植物数: {len(matched_plants)} ({len(matched_plants)/len(plant_ids)*100:.2f}%)")
    print(f"   无法映射植物数: {len(unmatched_plants)} ({len(unmatched_plants)/len(plant_ids)*100:.2f}%)")

    if unmatched_plants:
        print(f"\n   前10个无法映射的植物ID及其记录数:")
        for pid in unmatched_plants[:10]:
            count = plant_id_counter[pid]
            print(f"     - {pid}: {count} 条记录")

    # 分析 ICD-11 Code 映射
    print("\n6. 分析 ICD-11 Code 映射...")
    icd_codes = [clean_value(x) for x in df['ICD-11 Code'].unique() if clean_value(x)]
    icd_code_counter = Counter(df['ICD-11 Code'].apply(clean_value))

    matched_diseases = [code for code in icd_codes if code in disease_codes]
    unmatched_diseases = [code for code in icd_codes if code not in disease_codes]

    print(f"   唯一疾病编码数: {len(icd_codes)}")
    print(f"   可映射疾病数: {len(matched_diseases)} ({len(matched_diseases)/len(icd_codes)*100:.2f}%)")
    print(f"   无法映射疾病数: {len(unmatched_diseases)} ({len(unmatched_diseases)/len(icd_codes)*100:.2f}%)")

    if unmatched_diseases:
        print(f"\n   前10个无法映射的疾病编码及其记录数:")
        for code in unmatched_diseases[:10]:
            count = icd_code_counter[code]
            disease_name = df[df['ICD-11 Code'] == code]['Disease'].iloc[0]
            print(f"     - {code} ({disease_name}): {count} 条记录")

    # 计算可成功导入的记录数
    print("\n7. 预估导入成功率...")
    success_count = 0
    for _, row in df.iterrows():
        plant_id = clean_value(row['Plant_ID'])
        icd_code = clean_value(row['ICD-11 Code'])
        if plant_id in bio_resource_ids and icd_code in disease_codes:
            success_count += 1

    print(f"   可成功导入记录数: {success_count}/{len(df)} ({success_count/len(df)*100:.2f}%)")

    # 分析证据类型分布
    print("\n8. 分析证据类型分布...")
    evidence_stats = {
        'therapeutic_target': 0,
        'transcriptome': 0,
        'clinical_trial_plant': 0,
        'clinical_trial_ingredient': 0
    }

    for _, row in df.iterrows():
        if clean_value(row.get('Association_by_Therapeutic_Target')):
            evidence_stats['therapeutic_target'] += 1
        if clean_value(row.get('Association_by_Disease_Transcriptiome_Reversion')):
            evidence_stats['transcriptome'] += 1
        if clean_value(row.get('Association_by_Clinical_Trials_of_Plant')):
            evidence_stats['clinical_trial_plant'] += 1
        if clean_value(row.get('Association_by_Clinical_Trials_of_Plant_Ingredients')):
            evidence_stats['clinical_trial_ingredient'] += 1

    for evidence_type, count in evidence_stats.items():
        percentage = count / len(df) * 100
        print(f"   {evidence_type}: {count} ({percentage:.2f}%)")

    # 关闭连接
    cursor.close()
    conn.close()

    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)


if __name__ == '__main__':
    main()
