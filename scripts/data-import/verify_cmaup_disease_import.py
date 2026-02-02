#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMAUP 疾病数据导入验证脚本
============================
验证疾病数据和植物-疾病关联数据的导入情况
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': 'yfguo',
    'password': '',
    'host': 'localhost',
    'port': 5432
}


def connect_db():
    """连接数据库"""
    return psycopg2.connect(**DB_CONFIG)


def verify_disease_import(conn):
    """
    验证疾病数据导入情况
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("CMAUP 疾病数据导入验证报告")
    report_lines.append("=" * 80)
    report_lines.append("")

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # 1. 总体统计
        report_lines.append("## 1. 疾病数据统计")
        report_lines.append("-" * 80)

        cur.execute("SELECT COUNT(*) as count FROM diseases")
        total_diseases = cur.fetchone()['count']
        report_lines.append(f"总疾病记录数: {total_diseases}")

        cur.execute("""
            SELECT COUNT(*) as count FROM diseases
            WHERE num_of_related_plants > 0
        """)
        related_diseases = cur.fetchone()['count']
        report_lines.append(f"有关联植物的疾病数: {related_diseases}")

        cur.execute("""
            SELECT COUNT(*) as count FROM diseases
            WHERE num_of_related_targets > 0
        """)
        targets_diseases = cur.fetchone()['count']
        report_lines.append(f"有关联靶点的疾病数: {targets_diseases}")
        report_lines.append("")

        # 2. ICD-11 分类统计
        report_lines.append("## 2. ICD-11 分类统计 (Top 10)")
        report_lines.append("-" * 80)

        cur.execute("""
            SELECT 
                disease_category,
                COUNT(*) as count
            FROM diseases
            WHERE disease_category IS NOT NULL
            GROUP BY disease_category
            ORDER BY count DESC
            LIMIT 10
        """)
        results = cur.fetchall()
        for row in results:
            report_lines.append(f"{row['disease_category']}: {row['count']}")
        report_lines.append("")

        # 3. 植物-疾病关联统计
        report_lines.append("## 3. 植物-疾病关联统计")
        report_lines.append("-" * 80)

        cur.execute("SELECT COUNT(*) as count FROM bio_resource_disease_associations")
        total_associations = cur.fetchone()['count']
        report_lines.append(f"总关联记录数: {total_associations}")

        cur.execute("""
            SELECT COUNT(DISTINCT bio_resource_id) as count
            FROM bio_resource_disease_associations
        """)
        total_plants = cur.fetchone()['count']
        report_lines.append(f"涉及的生物资源数: {total_plants}")

        cur.execute("""
            SELECT COUNT(DISTINCT disease_id) as count
            FROM bio_resource_disease_associations
        """)
        associated_diseases = cur.fetchone()['count']
        report_lines.append(f"涉及的疾病数: {associated_diseases}")

        # 计算平均每个疾病的植物数
        cur.execute("""
            SELECT 
                AVG(num_of_related_plants) as avg_plants,
                MAX(num_of_related_plants) as max_plants,
                MIN(num_of_related_plants) as min_plants
            FROM diseases
            WHERE num_of_related_plants > 0
        """)
        result = cur.fetchone()
        if result['avg_plants']:
            report_lines.append(f"平均每个疾病关联植物数: {result['avg_plants']:.1f}")
            report_lines.append(f"最大关联植物数: {result['max_plants']}")
            report_lines.append(f"最小关联植物数: {result['min_plants']}")
        report_lines.append("")

        # 4. 证据类型统计
        report_lines.append("## 4. 证据类型统计")
        report_lines.append("-" * 80)

        cur.execute("""
            SELECT 
                COUNT(CASE WHEN evidence_therapeutic_target IS NOT NULL 
                          AND evidence_therapeutic_target != '' THEN 1 END) as target_evidence,
                COUNT(CASE WHEN evidence_transcriptome = true THEN 1 END) as transcriptome_evidence,
                COUNT(CASE WHEN evidence_clinical_trial_plant IS NOT NULL 
                          AND evidence_clinical_trial_plant != '' THEN 1 END) as plant_trial_evidence,
                COUNT(CASE WHEN evidence_clinical_trial_ingredient IS NOT NULL 
                          AND evidence_clinical_trial_ingredient != '' THEN 1 END) as ingredient_trial_evidence
            FROM bio_resource_disease_associations
        """)
        result = cur.fetchone()

        report_lines.append(f"治疗靶点证据: {result['target_evidence']}")
        report_lines.append(f"转录组证据: {result['transcriptome_evidence']}")
        report_lines.append(f"植物临床试验证据: {result['plant_trial_evidence']}")
        report_lines.append(f"成分临床试验证据: {result['ingredient_trial_evidence']}")
        report_lines.append("")

        # 5. 置信度分布
        report_lines.append("## 5. 置信度分布")
        report_lines.append("-" * 80)

        cur.execute("""
            SELECT 
                ROUND(confidence_score::numeric, 1) as score,
                COUNT(*) as count
            FROM bio_resource_disease_associations
            WHERE confidence_score IS NOT NULL
            GROUP BY score
            ORDER BY score DESC
        """)
        results = cur.fetchall()
        for row in results:
            report_lines.append(f"置信度 {row['score']}: {row['count']}")
        report_lines.append("")

        # 6. 示例数据
        report_lines.append("## 6. 示例数据")
        report_lines.append("-" * 80)

        report_lines.append("疾病示例 (Top 5 by 关联植物数):")
        cur.execute("""
            SELECT 
                d.disease_id,
                d.icd11_code,
                d.disease_name,
                d.disease_category,
                d.num_of_related_plants,
                d.num_of_related_targets
            FROM diseases d
            WHERE d.num_of_related_plants > 0
            ORDER BY d.num_of_related_plants DESC
            LIMIT 5
        """)
        results = cur.fetchall()
        for row in results:
            report_lines.append(f"  {row['disease_name']} ({row['icd11_code']})")
            report_lines.append(f"    分类: {row['disease_category']}")
            report_lines.append(f"    关联植物: {row['num_of_related_plants']}")
            report_lines.append(f"    关联靶点: {row['num_of_related_targets']}")
            report_lines.append("")

        report_lines.append("植物-疾病关联示例 (Top 5):")
        cur.execute("""
            SELECT 
                br.id,
                br.resource_id,
                br.latin_name,
                d.disease_name,
                d.icd11_code,
                brda.confidence_score,
                CASE 
                    WHEN brda.evidence_therapeutic_target IS NOT NULL 
                    AND brda.evidence_therapeutic_target != '' THEN 'Target'
                END as evidence_type
            FROM bio_resource_disease_associations brda
            JOIN bio_resources br ON brda.bio_resource_id = br.id
            JOIN diseases d ON brda.disease_id = d.id
            ORDER BY brda.confidence_score DESC
            LIMIT 5
        """)
        results = cur.fetchall()
        for row in results:
            report_lines.append(f"  {row['latin_name']} -> {row['disease_name']}")
            report_lines.append(f"    植物ID: {row['resource_id']}, 疾病代码: {row['icd11_code']}")
            report_lines.append(f"    置信度: {row['confidence_score']}, 证据: {row['evidence_type']}")
            report_lines.append("")

    report_lines.append("=" * 80)
    report_lines.append("验证完成")
    report_lines.append("=" * 80)

    return '\n'.join(report_lines)


def main():
    """主函数"""
    print("CMAUP 疾病数据导入验证")
    print("=" * 80)

    conn = connect_db()
    try:
        # 生成验证报告
        report = verify_disease_import(conn)

        # 保存报告
        report_file = '/home/yfguo/NPdatabase/scripts/data-import/output/PHASE4_STEP4_CMAUP_DISEASE_IMPORT_REPORT.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        # 打印报告
        print("\n" + report)
        print(f"\n报告已保存到: {report_file}")

    finally:
        conn.close()

    print("\n验证完成!")


if __name__ == '__main__':
    main()
