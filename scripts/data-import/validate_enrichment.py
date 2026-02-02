#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据完整性验证脚本
==================
验证所有数据补充步骤的完整性，包括：
- 外键完整性
- 数据量统计
- 匹配率统计
- 数据质量检查（空值、异常值）
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from collections import defaultdict
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


def check_foreign_key_integrity(conn):
    """
    检查外键完整性
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("1. 外键完整性检查")
    report_lines.append("=" * 80)
    report_lines.append("")

    issues = []

    with conn.cursor() as cur:
        # 1.1 bio_resource_natural_products 外键
        report_lines.append("### 1.1 bio_resource_natural_products")
        cur.execute("""
            SELECT COUNT(*) as count
            FROM bio_resource_natural_products brnp
            LEFT JOIN bio_resources br ON brnp.bio_resource_id = br.id
            WHERE br.id IS NULL
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("bio_resource_natural_products: {} 条记录引用不存在的 bio_resources".format(result[0]))
            report_lines.append(f"  ❌ 发现 {result[0]} 条记录引用不存在的 bio_resources")
        else:
            report_lines.append(f"  ✅ 所有记录的 bio_resource_id 有效")

        cur.execute("""
            SELECT COUNT(*) as count
            FROM bio_resource_natural_products brnp
            LEFT JOIN natural_products np ON brnp.natural_product_id = np.id
            WHERE np.id IS NULL
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("bio_resource_natural_products: {} 条记录引用不存在的 natural_products".format(result[0]))
            report_lines.append(f"  ❌ 发现 {result[0]} 条记录引用不存在的 natural_products")
        else:
            report_lines.append(f"  ✅ 所有记录的 natural_product_id 有效")

        # 1.2 bio_resource_disease_associations 外键
        report_lines.append("")
        report_lines.append("### 1.2 bio_resource_disease_associations")
        cur.execute("""
            SELECT COUNT(*) as count
            FROM bio_resource_disease_associations brda
            LEFT JOIN bio_resources br ON brda.bio_resource_id = br.id
            WHERE br.id IS NULL
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("bio_resource_disease_associations: {} 条记录引用不存在的 bio_resources".format(result[0]))
            report_lines.append(f"  ❌ 发现 {result[0]} 条记录引用不存在的 bio_resources")
        else:
            report_lines.append(f"  ✅ 所有记录的 bio_resource_id 有效")

        cur.execute("""
            SELECT COUNT(*) as count
            FROM bio_resource_disease_associations brda
            LEFT JOIN diseases d ON brda.disease_id = d.id
            WHERE d.id IS NULL
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("bio_resource_disease_associations: {} 条记录引用不存在的 diseases".format(result[0]))
            report_lines.append(f"  ❌ 发现 {result[0]} 条记录引用不存在的 diseases")
        else:
            report_lines.append(f"  ✅ 所有记录的 disease_id 有效")

        # 1.3 prescription_resources 外键
        report_lines.append("")
        report_lines.append("### 1.3 prescription_resources")
        cur.execute("""
            SELECT COUNT(*) as count
            FROM prescription_resources pr
            LEFT JOIN prescriptions p ON pr.prescription_id = p.id
            WHERE p.id IS NULL
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("prescription_resources: {} 条记录引用不存在的 prescriptions".format(result[0]))
            report_lines.append(f"  ❌ 发现 {result[0]} 条记录引用不存在的 prescriptions")
        else:
            report_lines.append(f"  ✅ 所有记录的 prescription_id 有效")

        cur.execute("""
            SELECT COUNT(*) as count
            FROM prescription_resources pr
            LEFT JOIN bio_resources br ON pr.bio_resource_id = br.id
            WHERE br.id IS NULL
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("prescription_resources: {} 条记录引用不存在的 bio_resources".format(result[0]))
            report_lines.append(f"  ❌ 发现 {result[0]} 条记录引用不存在的 bio_resources")
        else:
            report_lines.append(f"  ✅ 所有记录的 bio_resource_id 有效")

        # 1.4 prescription_natural_products 外键
        report_lines.append("")
        report_lines.append("### 1.4 prescription_natural_products")
        cur.execute("""
            SELECT COUNT(*) as count
            FROM prescription_natural_products pnp
            LEFT JOIN prescriptions p ON pnp.prescription_id = p.id
            WHERE p.id IS NULL
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("prescription_natural_products: {} 条记录引用不存在的 prescriptions".format(result[0]))
            report_lines.append(f"  ❌ 发现 {result[0]} 条记录引用不存在的 prescriptions")
        else:
            report_lines.append(f"  ✅ 所有记录的 prescription_id 有效")

        cur.execute("""
            SELECT COUNT(*) as count
            FROM prescription_natural_products pnp
            LEFT JOIN natural_products np ON pnp.natural_product_id = np.id
            WHERE np.id IS NULL
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("prescription_natural_products: {} 条记录引用不存在的 natural_products".format(result[0]))
            report_lines.append(f"  ❌ 发现 {result[0]} 条记录引用不存在的 natural_products")
        else:
            report_lines.append(f"  ✅ 所有记录的 natural_product_id 有效")

    report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("")

    return issues, '\n'.join(report_lines)


def check_data_statistics(conn):
    """
    检查数据量统计
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("2. 数据量统计")
    report_lines.append("=" * 80)
    report_lines.append("")

    stats = {}

    with conn.cursor() as cur:
        # 2.1 TTD 靶点数据
        report_lines.append("### 2.1 TTD 靶点数据")
        cur.execute("""
            SELECT 
                COUNT(*) as total_targets,
                COUNT(CASE WHEN gene_name IS NOT NULL THEN 1 END) as with_gene_name,
                COUNT(CASE WHEN synonyms IS NOT NULL THEN 1 END) as with_synonyms,
                COUNT(CASE WHEN function IS NOT NULL THEN 1 END) as with_function,
                COUNT(CASE WHEN pdb_structure IS NOT NULL THEN 1 END) as with_pdb,
                COUNT(CASE WHEN ec_number IS NOT NULL THEN 1 END) as with_ec,
                COUNT(CASE WHEN ttd_id IS NOT NULL THEN 1 END) as with_ttd_id
            FROM targets
        """)
        result = cur.fetchone()
        stats['targets'] = result
        report_lines.append(f"  总靶点数: {result[0]}")
        report_lines.append(f"  有基因名: {result[1]} ({result[1]/result[0]*100:.1f}%)")
        report_lines.append(f"  有同义词: {result[2]} ({result[2]/result[0]*100:.1f}%)")
        report_lines.append(f"  有功能描述: {result[3]} ({result[3]/result[0]*100:.1f}%)")
        report_lines.append(f"  有PDB结构: {result[4]} ({result[4]/result[0]*100:.1f}%)")
        report_lines.append(f"  有EC编号: {result[5]} ({result[5]/result[0]*100:.1f}%)")
        report_lines.append(f"  有TTD ID: {result[6]} ({result[6]/result[0]*100:.1f}%)")

        # 2.2 TCMID 处方数据
        report_lines.append("")
        report_lines.append("### 2.2 TCMID 处方数据")
        cur.execute("SELECT COUNT(*) as count FROM prescriptions")
        prescriptions_count = cur.fetchone()[0]
        stats['prescriptions'] = prescriptions_count
        report_lines.append(f"  处方总数: {prescriptions_count}")

        cur.execute("SELECT COUNT(*) as count FROM prescription_resources")
        pres_res_count = cur.fetchone()[0]
        stats['prescription_resources'] = pres_res_count
        report_lines.append(f"  处方-药材关联: {pres_res_count}")

        cur.execute("SELECT COUNT(*) as count FROM prescription_natural_products")
        pres_np_count = cur.fetchone()[0]
        stats['prescription_natural_products'] = pres_np_count
        report_lines.append(f"  处方-天然产物关联: {pres_np_count}")

        # 2.3 CMAUP 植物数据
        report_lines.append("")
        report_lines.append("### 2.3 CMAUP 植物数据")
        cur.execute("""
            SELECT 
                COUNT(*) as total_bio_resources,
                COUNT(CASE WHEN cmaup_id IS NOT NULL THEN 1 END) as with_cmaup_id,
                COUNT(CASE WHEN species_tax_id IS NOT NULL THEN 1 END) as with_species_tax_id,
                COUNT(CASE WHEN genus_tax_id IS NOT NULL THEN 1 END) as with_genus_tax_id,
                COUNT(CASE WHEN family_tax_id IS NOT NULL THEN 1 END) as with_family_tax_id
            FROM bio_resources
            WHERE resource_type = 'Plant'
        """)
        result = cur.fetchone()
        stats['bio_resources'] = result
        report_lines.append(f"  总植物资源数: {result[0]}")
        report_lines.append(f"  有CMAUP ID: {result[1]} ({result[1]/result[0]*100:.1f}%)")
        report_lines.append(f"  有种Tax ID: {result[2]} ({result[2]/result[0]*100:.1f}%)")
        report_lines.append(f"  有属Tax ID: {result[3]} ({result[3]/result[0]*100:.1f}%)")
        report_lines.append(f"  有科Tax ID: {result[4]} ({result[4]/result[0]*100:.1f}%)")

    report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("")

    return stats, '\n'.join(report_lines)


def check_matching_rates(conn):
    """
    检查匹配率统计
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("3. 匹配率统计")
    report_lines.append("=" * 80)
    report_lines.append("")

    rates = {}

    with conn.cursor() as cur:
        # 3.1 TTD 靶点匹配率
        report_lines.append("### 3.1 TTD 靶点匹配率")
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN ttd_id IS NOT NULL THEN 1 END) as matched
            FROM targets
        """)
        result = cur.fetchone()
        ttd_match_rate = (result[1] / result[0] * 100) if result[0] > 0 else 0
        rates['ttd'] = {
            'total': result[0],
            'matched': result[1],
            'rate': ttd_match_rate
        }
        report_lines.append(f"  总靶点数: {result[0]}")
        report_lines.append(f"  已匹配TTD: {result[1]}")
        report_lines.append(f"  匹配率: {ttd_match_rate:.2f}%")

        # 3.2 TCMID 药材匹配率
        report_lines.append("")
        report_lines.append("### 3.2 TCMID 药材匹配率")
        cur.execute("SELECT COUNT(*) as count FROM prescription_resources")
        total_herbs = cur.fetchone()[0]
        
        cur.execute("""
            SELECT COUNT(DISTINCT bio_resource_id) as count
            FROM prescription_resources
        """)
        unique_matched = cur.fetchone()[0]
        
        tcmid_match_rate = (unique_matched / total_herbs * 100) if total_herbs > 0 else 0
        rates['tcmid'] = {
            'total': total_herbs,
            'matched': unique_matched,
            'rate': tcmid_match_rate
        }
        report_lines.append(f"  处方-药材关联总数: {total_herbs}")
        report_lines.append(f"  唯一匹配药材数: {unique_matched}")
        report_lines.append(f"  匹配率: {tcmid_match_rate:.2f}%")

        # 3.3 CMAUP 植物匹配率
        report_lines.append("")
        report_lines.append("### 3.3 CMAUP 植物匹配率")
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN cmaup_id IS NOT NULL THEN 1 END) as matched
            FROM bio_resources
            WHERE resource_type = 'Plant'
        """)
        result = cur.fetchone()
        cmaup_match_rate = (result[1] / result[0] * 100) if result[0] > 0 else 0
        rates['cmaup'] = {
            'total': result[0],
            'matched': result[1],
            'rate': cmaup_match_rate
        }
        report_lines.append(f"  总植物资源数: {result[0]}")
        report_lines.append(f"  已匹配CMAUP: {result[1]}")
        report_lines.append(f"  匹配率: {cmaup_match_rate:.2f}%")

        # 3.4 疾病关联匹配率
        report_lines.append("")
        report_lines.append("### 3.4 疾病关联匹配率")
        cur.execute("""
            SELECT 
                COUNT(*) as total_diseases,
                COUNT(CASE WHEN num_of_related_plants > 0 THEN 1 END) as with_plants
            FROM diseases
        """)
        result = cur.fetchone()
        disease_plant_rate = (result[1] / result[0] * 100) if result[0] > 0 else 0
        rates['disease_plants'] = {
            'total': result[0],
            'matched': result[1],
            'rate': disease_plant_rate
        }
        report_lines.append(f"  总疾病数: {result[0]}")
        report_lines.append(f"  有植物关联: {result[1]}")
        report_lines.append(f"  匹配率: {disease_plant_rate:.2f}%")

    report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("")

    return rates, '\n'.join(report_lines)


def check_data_quality(conn):
    """
    检查数据质量（空值、异常值）
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("4. 数据质量检查")
    report_lines.append("=" * 80)
    report_lines.append("")

    issues = []

    with conn.cursor() as cur:
        # 4.1 targets 表质量检查
        report_lines.append("### 4.1 targets 表")
        cur.execute("""
            SELECT 
                COUNT(*) as count,
                target_type,
                target_name,
                target_organism
            FROM targets
            WHERE target_name IS NULL OR target_name = ''
            GROUP BY target_type, target_name, target_organism
            LIMIT 5
        """)
        results = cur.fetchall()
        if results:
            issues.append("targets: 发现 {} 条记录缺失 target_name".format(len(results)))
            report_lines.append(f"  ⚠️  发现 {len(results)} 条记录缺失 target_name")
        else:
            report_lines.append(f"  ✅ 所有记录都有 target_name")

        cur.execute("""
            SELECT 
                COUNT(*) as count,
                target_name
            FROM targets
            WHERE uniprot_id IS NOT NULL AND uniprot_id != ''
            AND LENGTH(uniprot_id) != 6
            GROUP BY target_name
            LIMIT 5
        """)
        results = cur.fetchall()
        if results:
            issues.append("targets: 发现 {} 条记录的 UniProt ID 格式异常".format(len(results)))
            report_lines.append(f"  ⚠️  发现 {len(results)} 条记录的 UniProt ID 格式可能异常")

        # 4.2 bio_resources 表质量检查
        report_lines.append("")
        report_lines.append("### 4.2 bio_resources 表")
        cur.execute("""
            SELECT 
                COUNT(*) as count
            FROM bio_resources
            WHERE resource_type = 'Plant'
            AND (latin_name IS NULL OR latin_name = '')
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("bio_resources: 发现 {} 条植物记录缺失 latin_name".format(result[0]))
            report_lines.append(f"  ⚠️  发现 {result[0]} 条植物记录缺失 latin_name")
        else:
            report_lines.append(f"  ✅ 所有植物记录都有 latin_name")

        # 4.3 diseases 表质量检查
        report_lines.append("")
        report_lines.append("### 4.3 diseases 表")
        cur.execute("""
            SELECT 
                COUNT(*) as count
            FROM diseases
            WHERE (disease_name IS NULL OR disease_name = '')
            OR (icd11_code IS NULL OR icd11_code = '')
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("diseases: 发现 {} 条记录缺失必填字段".format(result[0]))
            report_lines.append(f"  ⚠️  发现 {result[0]} 条记录缺失必填字段")
        else:
            report_lines.append(f"  ✅ 所有记录都有必填字段")

        # 4.4 bio_resource_disease_associations 表质量检查
        report_lines.append("")
        report_lines.append("### 4.4 bio_resource_disease_associations 表")
        cur.execute("""
            SELECT 
                COUNT(*) as count
            FROM bio_resource_disease_associations
            WHERE confidence_score < 0 OR confidence_score > 1
        """)
        result = cur.fetchone()
        if result[0] > 0:
            issues.append("bio_resource_disease_associations: 发现 {} 条记录的置信度超出范围".format(result[0]))
            report_lines.append(f"  ⚠️  发现 {result[0]} 条记录的置信度超出 [0,1] 范围")
        else:
            report_lines.append(f"  ✅ 所有置信度都在有效范围内")

    report_lines.append("")
    report_lines.append("-" * 80)
    report_lines.append("")

    return issues, '\n'.join(report_lines)


def generate_summary(fk_issues, stats, rates, quality_issues):
    """
    生成总结报告
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("5. 数据完整性验证总结")
    report_lines.append("=" * 80)
    report_lines.append("")

    # 5.1 总体评分
    report_lines.append("### 5.1 总体评分")
    report_lines.append("")

    score = 100
    score -= len(fk_issues) * 5
    score -= len(quality_issues) * 2
    score = max(0, score)

    report_lines.append(f"数据完整性评分: {score}/100")
    report_lines.append("")

    # 5.2 外键完整性
    report_lines.append("### 5.2 外键完整性")
    if len(fk_issues) == 0:
        report_lines.append("✅ 外键完整性检查通过")
    else:
        report_lines.append(f"❌ 发现 {len(fk_issues)} 个外键完整性问题")
        for issue in fk_issues:
            report_lines.append(f"  - {issue}")
    report_lines.append("")

    # 5.3 匹配率评估
    report_lines.append("### 5.3 匹配率评估")
    report_lines.append("")

    # 评估标准
    targets_score = "优秀" if rates['ttd']['rate'] >= 90 else "良好" if rates['ttd']['rate'] >= 70 else "一般"
    tcmid_score = "优秀" if rates['tcmid']['rate'] >= 80 else "良好" if rates['tcmid']['rate'] >= 60 else "一般"
    cmaup_score = "优秀" if rates['cmaup']['rate'] >= 85 else "良好" if rates['cmaup']['rate'] >= 60 else "一般"
    disease_score = "优秀" if rates['disease_plants']['rate'] >= 95 else "良好" if rates['disease_plants']['rate'] >= 80 else "一般"

    report_lines.append(f"TTD 靶点匹配: {rates['ttd']['rate']:.2f}% - {targets_score}")
    report_lines.append(f"TCMID 药材匹配: {rates['tcmid']['rate']:.2f}% - {tcmid_score}")
    report_lines.append(f"CMAUP 植物匹配: {rates['cmaup']['rate']:.2f}% - {cmaup_score}")
    report_lines.append(f"疾病关联匹配: {rates['disease_plants']['rate']:.2f}% - {disease_score}")
    report_lines.append("")

    # 5.4 数据质量
    report_lines.append("### 5.4 数据质量")
    if len(quality_issues) == 0:
        report_lines.append("✅ 数据质量检查通过")
    else:
        report_lines.append(f"⚠️  发现 {len(quality_issues)} 个数据质量问题")
        for issue in quality_issues:
            report_lines.append(f"  - {issue}")
    report_lines.append("")

    # 5.5 改进建议
    report_lines.append("### 5.5 改进建议")
    report_lines.append("")

    if rates['ttd']['rate'] < 90:
        report_lines.append("- 考虑进一步优化 TTD 靶点匹配算法")
    if rates['tcmid']['rate'] < 80:
        report_lines.append("- 考虑进一步优化 TCMID 药材匹配算法")
    if rates['cmaup']['rate'] < 85:
        report_lines.append("- 考虑进一步优化 CMAUP 植物匹配算法")
    if len(quality_issues) > 0:
        report_lines.append("- 建议修复发现的数据质量问题")
    if fk_issues:
        report_lines.append("- 建议修复外键完整性问题")

    report_lines.append("")
    report_lines.append("=" * 80)

    return '\n'.join(report_lines)


def main():
    """主函数"""
    print("=" * 80)
    print("数据完整性验证")
    print("=" * 80)

    conn = connect_db()
    try:
        # 1. 外键完整性检查
        print("\n1. 检查外键完整性...")
        fk_issues, fk_report = check_foreign_key_integrity(conn)

        # 2. 数据量统计
        print("2. 统计数据量...")
        stats, stats_report = check_data_statistics(conn)

        # 3. 匹配率统计
        print("3. 统计匹配率...")
        rates, rates_report = check_matching_rates(conn)

        # 4. 数据质量检查
        print("4. 检查数据质量...")
        quality_issues, quality_report = check_data_quality(conn)

        # 5. 生成总结
        print("5. 生成总结...")
        summary_report = generate_summary(fk_issues, stats, rates, quality_issues)

        # 合并报告 (每个报告已经是字符串)
        full_report = '\n'.join([
            fk_report,
            stats_report,
            rates_report,
            quality_report,
            summary_report
        ])

        # 保存报告
        report_file = '/home/yfguo/NPdatabase/scripts/data-import/output/PHASE5_DATA_INTEGRITY_VALIDATION_REPORT.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(full_report)

        # 打印报告
        print("\n" + full_report)
        print(f"\n报告已保存到: {report_file}")

    finally:
        conn.close()

    print("\n验证完成!")


if __name__ == '__main__':
    main()
