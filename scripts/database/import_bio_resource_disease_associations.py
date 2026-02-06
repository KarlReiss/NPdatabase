#!/usr/bin/env python3
"""
导入植物-疾病关联数据到 bio_resource_disease_associations 表
数据源: CMAUP v2.0 Plant-Human Disease Associations
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from collections import defaultdict

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

# 批量插入大小
BATCH_SIZE = 1000


def clean_value(val):
    """清理数据值，将 n.a. 和空字符串转为 None"""
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in ('n.a.', 'n.a', 'na', '', '-'):
            return None
    return val


def calculate_confidence_score(row):
    """
    根据证据类型计算置信度评分 (0-1)
    - 治疗靶点证据: +0.3
    - 转录组证据: +0.2
    - 植物临床试验: +0.3
    - 成分临床试验: +0.2
    """
    score = 0.0

    # 治疗靶点证据
    if clean_value(row.get('Association_by_Therapeutic_Target')):
        score += 0.3

    # 转录组证据
    if clean_value(row.get('Association_by_Disease_Transcriptiome_Reversion')):
        score += 0.2

    # 植物临床试验
    if clean_value(row.get('Association_by_Clinical_Trials_of_Plant')):
        score += 0.3

    # 成分临床试验
    if clean_value(row.get('Association_by_Clinical_Trials_of_Plant_Ingredients')):
        score += 0.2

    return round(score, 2)


def load_bio_resource_mapping(conn):
    """加载生物资源ID映射 (resource_id -> id)"""
    print(f"[{datetime.now()}] 加载生物资源ID映射...")
    cursor = conn.cursor()
    cursor.execute("SELECT id, resource_id FROM bio_resources WHERE resource_id IS NOT NULL")
    mapping = {resource_id: id for id, resource_id in cursor.fetchall()}
    cursor.close()
    print(f"  - 映射记录数: {len(mapping)}")
    return mapping


def load_disease_mapping(conn):
    """加载疾病ID映射 (icd11_code -> id)"""
    print(f"[{datetime.now()}] 加载疾病ID映射...")
    cursor = conn.cursor()
    cursor.execute("SELECT id, icd11_code FROM diseases WHERE icd11_code IS NOT NULL")
    mapping = {icd11_code: id for id, icd11_code in cursor.fetchall()}
    cursor.close()
    print(f"  - 映射记录数: {len(mapping)}")
    return mapping


def load_associations_data():
    """加载CMAUP植物-疾病关联数据"""
    print(f"[{datetime.now()}] 加载 CMAUP Plant-Human Disease Associations...")
    df = pd.read_csv(CMAUP_ASSOCIATIONS, sep='\t', dtype=str)
    print(f"  - 记录数: {len(df)}")
    print(f"  - 列名: {list(df.columns)}")
    return df


def expand_icd_range(icd_code):
    """
    将范围编码拆分为起始和结束编码
    例如: 2A00-2F9Z -> [2A00, 2F9Z]
    """
    if '-' in icd_code:
        parts = icd_code.split('-')
        if len(parts) == 2:
            return [parts[0].strip(), parts[1].strip()]
    return [icd_code]


def prepare_records(df, bio_resource_mapping, disease_mapping):
    """准备插入数据库的记录"""
    print(f"[{datetime.now()}] 准备数据库记录...")

    # 使用字典来合并重复的 (bio_resource_id, disease_id) 组合
    records_dict = {}
    stats = {
        'total': len(df),
        'success': 0,
        'skipped_no_plant': 0,
        'skipped_no_disease': 0,
        'skipped_range_expanded': 0,
        'duplicates_merged': 0,
        'evidence_counts': defaultdict(int)
    }

    for idx, row in df.iterrows():
        # 映射 Plant_ID 到 bio_resource_id
        plant_id = clean_value(row.get('Plant_ID'))
        if not plant_id or plant_id not in bio_resource_mapping:
            stats['skipped_no_plant'] += 1
            continue
        bio_resource_id = bio_resource_mapping[plant_id]

        # 映射 ICD-11 Code 到 disease_id（支持范围编码拆分）
        icd11_code = clean_value(row.get('ICD-11 Code'))
        if not icd11_code:
            stats['skipped_no_disease'] += 1
            continue

        # 拆分范围编码
        icd_codes = expand_icd_range(icd11_code)

        # 处理证据字段
        evidence_target = clean_value(row.get('Association_by_Therapeutic_Target'))
        evidence_transcriptome_raw = clean_value(row.get('Association_by_Disease_Transcriptiome_Reversion'))
        evidence_trial_plant = clean_value(row.get('Association_by_Clinical_Trials_of_Plant'))
        evidence_trial_ingredient = clean_value(row.get('Association_by_Clinical_Trials_of_Plant_Ingredients'))

        # 转录组证据转为布尔值
        evidence_transcriptome = evidence_transcriptome_raw is not None

        # 计算置信度
        confidence_score = calculate_confidence_score(row)

        # 处理每个ICD编码（可能是拆分后的多个）
        for icd_code in icd_codes:
            if icd_code not in disease_mapping:
                stats['skipped_no_disease'] += 1
                if len(icd_codes) > 1:
                    stats['skipped_range_expanded'] += 1
                continue

            disease_id = disease_mapping[icd_code]
            key = (bio_resource_id, disease_id)

            # 如果已存在，合并证据
            if key in records_dict:
                stats['duplicates_merged'] += 1
                existing = records_dict[key]

                # 合并证据字段（保留非空值）
                merged_target = existing[2] or evidence_target
                merged_transcriptome = existing[3] or evidence_transcriptome
                merged_trial_plant = existing[4] or evidence_trial_plant
                merged_trial_ingredient = existing[5] or evidence_trial_ingredient

                # 重新计算置信度
                merged_confidence = 0.0
                if merged_target: merged_confidence += 0.3
                if merged_transcriptome: merged_confidence += 0.2
                if merged_trial_plant: merged_confidence += 0.3
                if merged_trial_ingredient: merged_confidence += 0.2

                records_dict[key] = (
                    bio_resource_id,
                    disease_id,
                    merged_target,
                    merged_transcriptome,
                    merged_trial_plant,
                    merged_trial_ingredient,
                    round(merged_confidence, 2),
                    'CMAUP',
                    'v2.0'
                )
            else:
                # 新记录
                records_dict[key] = (
                    bio_resource_id,
                    disease_id,
                    evidence_target,
                    evidence_transcriptome,
                    evidence_trial_plant,
                    evidence_trial_ingredient,
                    confidence_score,
                    'CMAUP',
                    'v2.0'
                )
                stats['success'] += 1

        if (idx + 1) % 10000 == 0:
            print(f"  - 已处理 {idx + 1}/{len(df)} 条记录...")

    # 统计证据类型（基于最终的去重记录）
    for record in records_dict.values():
        if record[2]:  # evidence_therapeutic_target
            stats['evidence_counts']['therapeutic_target'] += 1
        if record[3]:  # evidence_transcriptome
            stats['evidence_counts']['transcriptome'] += 1
        if record[4]:  # evidence_clinical_trial_plant
            stats['evidence_counts']['clinical_trial_plant'] += 1
        if record[5]:  # evidence_clinical_trial_ingredient
            stats['evidence_counts']['clinical_trial_ingredient'] += 1

    # 转换为列表
    records = list(records_dict.values())

    print(f"[{datetime.now()}] 数据准备完成:")
    print(f"  - 总记录数: {stats['total']}")
    print(f"  - 唯一关联数: {len(records)}")
    print(f"  - 跳过(无植物): {stats['skipped_no_plant']}")
    print(f"  - 跳过(无疾病): {stats['skipped_no_disease']}")
    print(f"  - 范围编码拆分跳过: {stats['skipped_range_expanded']}")
    print(f"  - 重复记录合并: {stats['duplicates_merged']}")
    print(f"  - 证据统计:")
    for evidence_type, count in stats['evidence_counts'].items():
        print(f"    - {evidence_type}: {count}")

    return records, stats


def insert_associations(conn, records):
    """批量插入关联数据"""
    print(f"[{datetime.now()}] 开始插入数据...")

    cursor = conn.cursor()
    total_inserted = 0
    total_updated = 0

    # 批量插入
    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i:i + BATCH_SIZE]

        # 使用 ON CONFLICT DO UPDATE 处理重复记录
        insert_query = """
            INSERT INTO bio_resource_disease_associations (
                bio_resource_id,
                disease_id,
                evidence_therapeutic_target,
                evidence_transcriptome,
                evidence_clinical_trial_plant,
                evidence_clinical_trial_ingredient,
                confidence_score,
                source,
                source_version
            ) VALUES %s
            ON CONFLICT (bio_resource_id, disease_id)
            DO UPDATE SET
                evidence_therapeutic_target = EXCLUDED.evidence_therapeutic_target,
                evidence_transcriptome = EXCLUDED.evidence_transcriptome,
                evidence_clinical_trial_plant = EXCLUDED.evidence_clinical_trial_plant,
                evidence_clinical_trial_ingredient = EXCLUDED.evidence_clinical_trial_ingredient,
                confidence_score = EXCLUDED.confidence_score,
                source = EXCLUDED.source,
                source_version = EXCLUDED.source_version
        """

        execute_values(cursor, insert_query, batch)
        batch_inserted = cursor.rowcount
        total_inserted += batch_inserted

        if (i + BATCH_SIZE) % 10000 == 0:
            print(f"  - 已插入 {i + BATCH_SIZE}/{len(records)} 条记录...")

    conn.commit()
    cursor.close()

    print(f"[{datetime.now()}] 数据插入完成:")
    print(f"  - 总插入/更新: {total_inserted}")

    return total_inserted


def generate_report(stats, total_inserted):
    """生成导入报告"""
    report_file = f'{DATA_DIR}/processed/bio_resource_disease_associations_import_report.txt'

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("植物-疾病关联数据导入报告\n")
        f.write("=" * 80 + "\n")
        f.write(f"导入时间: {datetime.now()}\n")
        f.write(f"数据源: CMAUP v2.0 Plant-Human Disease Associations\n")
        f.write("\n")

        f.write("数据处理统计:\n")
        f.write("-" * 80 + "\n")
        f.write(f"总记录数: {stats['total']}\n")
        f.write(f"唯一关联数: {stats['success']}\n")
        f.write(f"跳过(无植物映射): {stats['skipped_no_plant']}\n")
        f.write(f"跳过(无疾病映射): {stats['skipped_no_disease']}\n")
        f.write(f"范围编码拆分跳过: {stats.get('skipped_range_expanded', 0)}\n")
        f.write(f"重复记录合并: {stats.get('duplicates_merged', 0)}\n")
        f.write(f"成功率: {stats['success'] / stats['total'] * 100:.2f}%\n")
        f.write("\n")

        f.write("证据类型统计:\n")
        f.write("-" * 80 + "\n")
        for evidence_type, count in sorted(stats['evidence_counts'].items()):
            percentage = count / stats['success'] * 100 if stats['success'] > 0 else 0
            f.write(f"{evidence_type}: {count} ({percentage:.2f}%)\n")
        f.write("\n")

        f.write("数据库导入统计:\n")
        f.write("-" * 80 + "\n")
        f.write(f"插入/更新记录数: {total_inserted}\n")
        f.write("\n")

        f.write("范围编码处理说明:\n")
        f.write("-" * 80 + "\n")
        f.write("范围编码（如 2A00-2F9Z）已被拆分为起始和结束编码分别处理。\n")
        f.write("如果拆分后的编码在数据库中存在，则会创建对应的关联记录。\n")
        f.write("\n")

        f.write("=" * 80 + "\n")

    print(f"[{datetime.now()}] 报告已生成: {report_file}")
    return report_file


def main():
    """主函数"""
    print("=" * 80)
    print("植物-疾病关联数据导入")
    print("=" * 80)

    try:
        # 连接数据库
        print(f"[{datetime.now()}] 连接数据库...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("  - 数据库连接成功")

        # 加载映射
        bio_resource_mapping = load_bio_resource_mapping(conn)
        disease_mapping = load_disease_mapping(conn)

        # 加载关联数据
        df = load_associations_data()

        # 准备记录
        records, stats = prepare_records(df, bio_resource_mapping, disease_mapping)

        # 插入数据
        total_inserted = insert_associations(conn, records)

        # 生成报告
        report_file = generate_report(stats, total_inserted)

        # 关闭连接
        conn.close()
        print(f"[{datetime.now()}] 数据库连接已关闭")

        print("\n" + "=" * 80)
        print("导入完成！")
        print(f"报告文件: {report_file}")
        print("=" * 80)

    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise


if __name__ == '__main__':
    main()


