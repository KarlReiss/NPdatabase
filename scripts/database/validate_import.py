#!/usr/bin/env python3
"""
数据验证脚本
检查数据质量和完整性
"""

import psycopg2
from datetime import datetime

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': 'yfguo',
    'host': 'localhost',
    'port': 5432
}


def check_table_counts(conn):
    """检查各表记录数"""
    print(f"\n[{datetime.now()}] 表记录数统计")
    print("-" * 50)
    cur = conn.cursor()

    tables = [
        ('natural_products', '天然产物'),
        ('targets', '靶点'),
        ('bio_resources', '生物资源'),
        ('bioactivity', '活性数据'),
        ('toxicity', '毒性数据'),
        ('bio_resource_natural_products', '生物资源-天然产物关联'),
        ('prescriptions', '处方'),
        ('prescription_resources', '处方-生物资源关联'),
        ('prescription_natural_products', '处方-天然产物关联'),
    ]

    for table, desc in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"  {table:40} {count:>10,} ({desc})")
        except Exception as e:
            print(f"  {table:40} ERROR: {e}")

    cur.close()


def check_natural_products_quality(conn):
    """检查天然产物数据质量"""
    print(f"\n[{datetime.now()}] 天然产物数据质量")
    print("-" * 50)
    cur = conn.cursor()

    # 关键字段完整性
    checks = [
        ('np_id IS NOT NULL', 'np_id非空'),
        ('inchikey IS NOT NULL', 'inchikey非空'),
        ('smiles IS NOT NULL', 'smiles非空'),
        ('pref_name IS NOT NULL', 'pref_name非空'),
        ('molecular_weight IS NOT NULL', '分子量非空'),
        ('xlogp IS NOT NULL', 'xlogp非空'),
    ]

    cur.execute("SELECT COUNT(*) FROM natural_products")
    total = cur.fetchone()[0]

    for condition, desc in checks:
        cur.execute(f"SELECT COUNT(*) FROM natural_products WHERE {condition}")
        count = cur.fetchone()[0]
        pct = 100 * count / total if total > 0 else 0
        print(f"  {desc:30} {count:>10,} / {total:,} ({pct:.1f}%)")

    # 检查重复
    print("\n  重复检查:")
    cur.execute("SELECT COUNT(*) - COUNT(DISTINCT np_id) FROM natural_products")
    dup_np_id = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) - COUNT(DISTINCT inchikey) FROM natural_products WHERE inchikey IS NOT NULL")
    dup_inchikey = cur.fetchone()[0]
    print(f"    - np_id重复: {dup_np_id}")
    print(f"    - inchikey重复: {dup_inchikey}")

    # 分子量分布
    print("\n  分子量分布:")
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE molecular_weight < 100) as lt100,
            COUNT(*) FILTER (WHERE molecular_weight >= 100 AND molecular_weight < 500) as lt500,
            COUNT(*) FILTER (WHERE molecular_weight >= 500 AND molecular_weight < 1000) as lt1000,
            COUNT(*) FILTER (WHERE molecular_weight >= 1000) as ge1000
        FROM natural_products
    """)
    row = cur.fetchone()
    print(f"    - <100: {row[0]:,}")
    print(f"    - 100-500: {row[1]:,}")
    print(f"    - 500-1000: {row[2]:,}")
    print(f"    - >=1000: {row[3]:,}")

    cur.close()


def check_bioactivity_quality(conn):
    """检查活性数据质量"""
    print(f"\n[{datetime.now()}] 活性数据质量")
    print("-" * 50)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM bioactivity")
    total = cur.fetchone()[0]

    # 活性类型分布
    print("  活性类型分布 (Top 10):")
    cur.execute("""
        SELECT activity_type, COUNT(*) as cnt
        FROM bioactivity
        WHERE activity_type IS NOT NULL
        GROUP BY activity_type
        ORDER BY cnt DESC
        LIMIT 10
    """)
    for row in cur.fetchall():
        pct = 100 * row[1] / total if total > 0 else 0
        print(f"    - {row[0]:20} {row[1]:>10,} ({pct:.1f}%)")

    # 活性值分布
    print("\n  活性值分布:")
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE activity_value IS NULL) as null_val,
            COUNT(*) FILTER (WHERE activity_value_std < 1) as lt1,
            COUNT(*) FILTER (WHERE activity_value_std >= 1 AND activity_value_std < 100) as lt100,
            COUNT(*) FILTER (WHERE activity_value_std >= 100 AND activity_value_std < 1000) as lt1000,
            COUNT(*) FILTER (WHERE activity_value_std >= 1000 AND activity_value_std < 10000) as lt10000,
            COUNT(*) FILTER (WHERE activity_value_std >= 10000) as ge10000
        FROM bioactivity
    """)
    row = cur.fetchone()
    print(f"    - NULL: {row[0]:,}")
    print(f"    - <1 nM: {row[1]:,}")
    print(f"    - 1-100 nM: {row[2]:,}")
    print(f"    - 100-1000 nM: {row[3]:,}")
    print(f"    - 1-10 μM: {row[4]:,}")
    print(f"    - >=10 μM: {row[5]:,}")

    # 文献来源
    print("\n  文献来源类型:")
    cur.execute("""
        SELECT ref_id_type, COUNT(*) as cnt
        FROM bioactivity
        WHERE ref_id_type IS NOT NULL
        GROUP BY ref_id_type
        ORDER BY cnt DESC
    """)
    for row in cur.fetchall():
        print(f"    - {row[0]:20} {row[1]:>10,}")

    cur.close()


def check_bio_resources_quality(conn):
    """检查生物资源数据质量"""
    print(f"\n[{datetime.now()}] 生物资源数据质量")
    print("-" * 50)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM bio_resources")
    total = cur.fetchone()[0]

    # 资源类型分布
    print("  资源类型分布:")
    cur.execute("""
        SELECT resource_type, COUNT(*) as cnt
        FROM bio_resources
        GROUP BY resource_type
        ORDER BY cnt DESC
    """)
    for row in cur.fetchall():
        pct = 100 * row[1] / total if total > 0 else 0
        rtype = row[0] if row[0] else 'NULL'
        print(f"    - {rtype:20} {row[1]:>10,} ({pct:.1f}%)")

    # 分类学信息完整性
    print("\n  分类学信息完整性:")
    checks = [
        ('taxonomy_kingdom IS NOT NULL', '界(Kingdom)'),
        ('taxonomy_family IS NOT NULL', '科(Family)'),
        ('taxonomy_genus IS NOT NULL', '属(Genus)'),
        ('taxonomy_species IS NOT NULL', '种(Species)'),
        ('taxonomy_id IS NOT NULL', '分类ID'),
    ]

    for condition, desc in checks:
        cur.execute(f"SELECT COUNT(*) FROM bio_resources WHERE {condition}")
        count = cur.fetchone()[0]
        pct = 100 * count / total if total > 0 else 0
        print(f"    - {desc:20} {count:>10,} / {total:,} ({pct:.1f}%)")

    cur.close()


def check_targets_quality(conn):
    """检查靶点数据质量"""
    print(f"\n[{datetime.now()}] 靶点数据质量")
    print("-" * 50)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM targets")
    total = cur.fetchone()[0]

    # 靶点类型分布
    print("  靶点类型分布:")
    cur.execute("""
        SELECT target_type, COUNT(*) as cnt
        FROM targets
        GROUP BY target_type
        ORDER BY cnt DESC
        LIMIT 10
    """)
    for row in cur.fetchall():
        pct = 100 * row[1] / total if total > 0 else 0
        ttype = row[0] if row[0] else 'NULL'
        print(f"    - {ttype:30} {row[1]:>6,} ({pct:.1f}%)")

    # UniProt ID完整性
    print("\n  UniProt ID完整性:")
    cur.execute("SELECT COUNT(*) FROM targets WHERE uniprot_id IS NOT NULL")
    has_uniprot = cur.fetchone()[0]
    pct = 100 * has_uniprot / total if total > 0 else 0
    print(f"    - 有UniProt ID: {has_uniprot:,} / {total:,} ({pct:.1f}%)")

    cur.close()


def check_relationships(conn):
    """检查关联关系"""
    print(f"\n[{datetime.now()}] 关联关系统计")
    print("-" * 50)
    cur = conn.cursor()

    # 天然产物关联统计
    print("  天然产物关联:")
    cur.execute("""
        SELECT
            COUNT(*) FILTER (WHERE num_of_organism > 0) as has_organism,
            COUNT(*) FILTER (WHERE num_of_target > 0) as has_target,
            COUNT(*) FILTER (WHERE num_of_activity > 0) as has_activity
        FROM natural_products
    """)
    row = cur.fetchone()
    cur.execute("SELECT COUNT(*) FROM natural_products")
    total = cur.fetchone()[0]
    print(f"    - 有来源生物资源: {row[0]:,} / {total:,} ({100*row[0]/total:.1f}%)")
    print(f"    - 有靶点: {row[1]:,} / {total:,} ({100*row[1]/total:.1f}%)")
    print(f"    - 有活性数据: {row[2]:,} / {total:,} ({100*row[2]/total:.1f}%)")

    # 毒性数据覆盖
    print("\n  毒性数据覆盖:")
    cur.execute("""
        SELECT COUNT(DISTINCT natural_product_id) FROM toxicity
    """)
    has_toxicity = cur.fetchone()[0]
    print(f"    - 有毒性数据的天然产物: {has_toxicity:,} / {total:,} ({100*has_toxicity/total:.1f}%)")

    cur.close()


def generate_summary(conn):
    """生成数据摘要"""
    print(f"\n[{datetime.now()}] 数据库摘要")
    print("=" * 60)
    cur = conn.cursor()

    # 核心统计
    cur.execute("SELECT COUNT(*) FROM natural_products")
    np_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM targets")
    target_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bio_resources")
    br_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bioactivity")
    ba_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM toxicity")
    tox_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bio_resource_natural_products")
    brnp_count = cur.fetchone()[0]

    print(f"""
  天然产物数据库统计
  ─────────────────────────────────────────────────
  天然产物 (Natural Products):     {np_count:>12,}
  靶点 (Targets):                  {target_count:>12,}
  生物资源 (Bio Resources):        {br_count:>12,}
  活性记录 (Bioactivity):          {ba_count:>12,}
  毒性记录 (Toxicity):             {tox_count:>12,}
  生物资源-天然产物关联:           {brnp_count:>12,}
  ─────────────────────────────────────────────────
    """)

    cur.close()


def main():
    print("=" * 60)
    print("天然产物数据库 - 数据验证报告")
    print("=" * 60)

    # 连接数据库
    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)

    # 执行各项检查
    check_table_counts(conn)
    check_natural_products_quality(conn)
    check_bioactivity_quality(conn)
    check_bio_resources_quality(conn)
    check_targets_quality(conn)
    check_relationships(conn)
    generate_summary(conn)

    conn.close()

    print("=" * 60)
    print("验证完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
