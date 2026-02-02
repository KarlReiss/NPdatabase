#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CMAUP 植物补充数据导入验证脚本
=================================
验证 bio_resources 表的 taxonomy ID 信息导入情况
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


def verify_cmaup_import(conn):
    """
    验证CMAUP植物数据导入情况
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("CMAUP 植物补充数据导入验证报告")
    report_lines.append("=" * 80)
    report_lines.append("")

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # 1. 总体统计
        report_lines.append("## 1. 总体统计")
        report_lines.append("-" * 80)

        cur.execute("""
            SELECT 
                COUNT(*) as total_bio_resources,
                COUNT(CASE WHEN cmaup_id IS NOT NULL THEN 1 END) as updated_count
            FROM bio_resources
            WHERE resource_type = 'Plant'
        """)
        result = cur.fetchone()
        total_plants = result['total_bio_resources']
        updated_count = result['updated_count']
        update_rate = (updated_count / total_plants * 100) if total_plants > 0 else 0

        report_lines.append(f"生物资源总记录数 (植物): {total_plants}")
        report_lines.append(f"已更新taxonomy ID记录数: {updated_count}")
        report_lines.append(f"更新率: {update_rate:.2f}%")
        report_lines.append("")

        # 2. Taxonomy ID 填充情况
        report_lines.append("## 2. Taxonomy ID 填充情况")
        report_lines.append("-" * 80)

        cur.execute("""
            SELECT 
                COUNT(CASE WHEN cmaup_id IS NOT NULL THEN 1 END) as with_cmaup_id,
                COUNT(CASE WHEN species_tax_id IS NOT NULL THEN 1 END) as with_species_tax_id,
                COUNT(CASE WHEN genus_tax_id IS NOT NULL THEN 1 END) as with_genus_tax_id,
                COUNT(CASE WHEN family_tax_id IS NOT NULL THEN 1 END) as with_family_tax_id
            FROM bio_resources
            WHERE cmaup_id IS NOT NULL
        """)
        result = cur.fetchone()

        report_lines.append(f"填充 cmaup_id: {result['with_cmaup_id']}")
        report_lines.append(f"填充 species_tax_id: {result['with_species_tax_id']}")
        report_lines.append(f"填充 genus_tax_id: {result['with_genus_tax_id']}")
        report_lines.append(f"填充 family_tax_id: {result['with_family_tax_id']}")
        report_lines.append("")

        # 3. 未填充 species_tax_id 的记录
        report_lines.append("## 3. 未填充 species_tax_id 的记录分析")
        report_lines.append("-" * 80)

        cur.execute("""
            SELECT 
                COUNT(*) as missing_count
            FROM bio_resources
            WHERE cmaup_id IS NOT NULL
            AND (species_tax_id IS NULL OR species_tax_id = '')
        """)
        result = cur.fetchone()
        missing_count = result['missing_count']

        if missing_count > 0:
            report_lines.append(f"未填充 species_tax_id 的记录数: {missing_count}")
            report_lines.append("前10条记录:")
            report_lines.append("")

            cur.execute("""
                SELECT 
                    id,
                    resource_id,
                    latin_name,
                    cmaup_id,
                    genus_tax_id,
                    family_tax_id
                FROM bio_resources
                WHERE cmaup_id IS NOT NULL
                AND (species_tax_id IS NULL OR species_tax_id = '')
                LIMIT 10
            """)
            results = cur.fetchall()
            for row in results:
                report_lines.append(f"  ID: {row['id']}, CMAUP ID: {row['cmaup_id']}")
                report_lines.append(f"    拉丁名: {row['latin_name']}")
                report_lines.append(f"    属ID: {row['genus_tax_id']}, 科ID: {row['family_tax_id']}")
                report_lines.append("")
        else:
            report_lines.append("所有记录都已填充 species_tax_id")
            report_lines.append("")

        # 4. 唯一分类统计
        report_lines.append("## 4. 唯一分类统计")
        report_lines.append("-" * 80)

        cur.execute("""
            SELECT 
                COUNT(DISTINCT family_tax_id) as unique_families,
                COUNT(DISTINCT genus_tax_id) as unique_genera,
                COUNT(DISTINCT species_tax_id) as unique_species
            FROM bio_resources
            WHERE cmaup_id IS NOT NULL
        """)
        result = cur.fetchone()

        report_lines.append(f"唯一科 (family): {result['unique_families']}")
        report_lines.append(f"唯一属 (genus): {result['unique_genera']}")
        report_lines.append(f"唯一种 (species): {result['unique_species']}")
        report_lines.append("")

        # 5. 数据完整性验证
        report_lines.append("## 5. 数据完整性验证")
        report_lines.append("-" * 80)

        # 检查 taxonomy_id 与新字段的一致性
        cur.execute("""
            SELECT 
                COUNT(*) as inconsistent_count
            FROM bio_resources
            WHERE cmaup_id IS NOT NULL
            AND (
                (taxonomy_species != latin_name AND 
                 taxonomy_species IS NOT NULL AND 
                 latin_name IS NOT NULL)
                OR (taxonomy_genus IS NULL AND genus_tax_id IS NOT NULL)
                OR (taxonomy_family IS NULL AND family_tax_id IS NOT NULL)
            )
        """)
        result = cur.fetchone()
        inconsistent_count = result['inconsistent_count']

        report_lines.append(f"taxonomy 信息与新 taxonomy ID 不一致的记录: {inconsistent_count}")

        if inconsistent_count > 0:
            report_lines.append("前5条不一致记录:")
            report_lines.append("")

            cur.execute("""
                SELECT 
                    id,
                    resource_id,
                    latin_name,
                    taxonomy_species,
                    taxonomy_genus,
                    taxonomy_family,
                    species_tax_id,
                    genus_tax_id,
                    family_tax_id
                FROM bio_resources
                WHERE cmaup_id IS NOT NULL
                AND (
                    (taxonomy_species != latin_name AND 
                     taxonomy_species IS NOT NULL AND 
                     latin_name IS NOT NULL)
                    OR (taxonomy_genus IS NULL AND genus_tax_id IS NOT NULL)
                    OR (taxonomy_family IS NULL AND family_tax_id IS NOT NULL)
                )
                LIMIT 5
            """)
            results = cur.fetchall()
            for row in results:
                report_lines.append(f"  ID: {row['id']}")
                report_lines.append(f"    拉丁名: {row['latin_name']}")
                report_lines.append(f"    taxonomy_species: {row['taxonomy_species']}")
                report_lines.append(f"    taxonomy_genus: {row['taxonomy_genus']}")
                report_lines.append(f"    taxonomy_family: {row['taxonomy_family']}")
                report_lines.append("")

        # 6. 示例数据
        report_lines.append("## 6. 示例数据（已更新记录）")
        report_lines.append("-" * 80)

        cur.execute("""
            SELECT 
                id,
                resource_id,
                latin_name,
                chinese_name,
                taxonomy_genus,
                taxonomy_family,
                taxonomy_species,
                species_tax_id,
                genus_tax_id,
                family_tax_id,
                cmaup_id
            FROM bio_resources
            WHERE cmaup_id IS NOT NULL
            ORDER BY id
            LIMIT 5
        """)
        results = cur.fetchall()

        for row in results:
            report_lines.append(f"ID: {row['id']} | CMAUP ID: {row['cmaup_id']}")
            report_lines.append(f"  拉丁名: {row['latin_name']}")
            report_lines.append(f"  中文名: {row['chinese_name'] or 'N/A'}")
            report_lines.append(f"  属: {row['taxonomy_genus']} (ID: {row['genus_tax_id']})")
            report_lines.append(f"  科: {row['taxonomy_family']} (ID: {row['family_tax_id']})")
            report_lines.append(f"  种: {row['taxonomy_species']} (ID: {row['species_tax_id']})")
            report_lines.append("")

    report_lines.append("=" * 80)
    report_lines.append("验证完成")
    report_lines.append("=" * 80)

    return '\n'.join(report_lines)


def main():
    """主函数"""
    print("CMAUP 植物补充数据导入验证")
    print("=" * 80)

    conn = connect_db()
    try:
        # 生成验证报告
        report = verify_cmaup_import(conn)

        # 保存报告
        report_file = '/home/yfguo/NPdatabase/scripts/data-import/output/PHASE4_STEP3_CMAUP_PLANT_IMPORT_REPORT.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        # 打印报告
        print("\n" + report)
        print(f"\n报告已保存到: {report_file}")

    finally:
        conn.close()

    print("\n验证完成！")


if __name__ == '__main__':
    main()
