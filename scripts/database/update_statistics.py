#!/usr/bin/env python3
"""
更新统计字段
根据实际关联数据更新各表的计数字段
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


def update_natural_products_stats(conn):
    """更新 natural_products 表的统计字段"""
    print(f"[{datetime.now()}] 更新 natural_products 统计字段...")
    cur = conn.cursor()

    # 更新 num_of_organism (来源生物资源数)
    print("  - 更新 num_of_organism...")
    cur.execute("""
        UPDATE natural_products np
        SET num_of_organism = COALESCE(stats.cnt, 0)
        FROM (
            SELECT natural_product_id, COUNT(DISTINCT bio_resource_id) as cnt
            FROM bio_resource_natural_products
            GROUP BY natural_product_id
        ) stats
        WHERE np.id = stats.natural_product_id
    """)
    updated1 = cur.rowcount

    # 没有关联的设为0
    cur.execute("""
        UPDATE natural_products
        SET num_of_organism = 0
        WHERE id NOT IN (SELECT DISTINCT natural_product_id FROM bio_resource_natural_products)
    """)

    # 更新 num_of_target (靶点数)
    print("  - 更新 num_of_target...")
    cur.execute("""
        UPDATE natural_products np
        SET num_of_target = COALESCE(stats.cnt, 0)
        FROM (
            SELECT natural_product_id, COUNT(DISTINCT target_id) as cnt
            FROM bioactivity
            GROUP BY natural_product_id
        ) stats
        WHERE np.id = stats.natural_product_id
    """)
    updated2 = cur.rowcount

    # 没有活性数据的设为0
    cur.execute("""
        UPDATE natural_products
        SET num_of_target = 0
        WHERE id NOT IN (SELECT DISTINCT natural_product_id FROM bioactivity)
    """)

    # 更新 num_of_activity (活性记录数)
    print("  - 更新 num_of_activity...")
    cur.execute("""
        UPDATE natural_products np
        SET num_of_activity = COALESCE(stats.cnt, 0)
        FROM (
            SELECT natural_product_id, COUNT(*) as cnt
            FROM bioactivity
            GROUP BY natural_product_id
        ) stats
        WHERE np.id = stats.natural_product_id
    """)
    updated3 = cur.rowcount

    # 没有活性数据的设为0
    cur.execute("""
        UPDATE natural_products
        SET num_of_activity = 0
        WHERE id NOT IN (SELECT DISTINCT natural_product_id FROM bioactivity)
    """)

    conn.commit()
    print(f"  - 更新完成: organism={updated1}, target={updated2}, activity={updated3}")

    # 验证
    cur.execute("""
        SELECT
            AVG(num_of_organism)::numeric(10,2) as avg_organism,
            AVG(num_of_target)::numeric(10,2) as avg_target,
            AVG(num_of_activity)::numeric(10,2) as avg_activity,
            MAX(num_of_organism) as max_organism,
            MAX(num_of_target) as max_target,
            MAX(num_of_activity) as max_activity
        FROM natural_products
    """)
    row = cur.fetchone()
    print(f"  - 统计: avg_organism={row[0]}, avg_target={row[1]}, avg_activity={row[2]}")
    print(f"  - 最大值: max_organism={row[3]}, max_target={row[4]}, max_activity={row[5]}")

    cur.close()


def update_bio_resources_stats(conn):
    """更新 bio_resources 表的统计字段"""
    print(f"[{datetime.now()}] 更新 bio_resources 统计字段...")
    cur = conn.cursor()

    # 检查是否有 num_of_natural_products 字段
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'bio_resources' AND column_name = 'num_of_natural_products'
    """)
    if not cur.fetchone():
        print("  - 添加 num_of_natural_products 字段...")
        cur.execute("ALTER TABLE bio_resources ADD COLUMN num_of_natural_products INTEGER DEFAULT 0")
        conn.commit()

    # 更新 num_of_natural_products
    print("  - 更新 num_of_natural_products...")
    cur.execute("""
        UPDATE bio_resources br
        SET num_of_natural_products = COALESCE(stats.cnt, 0)
        FROM (
            SELECT bio_resource_id, COUNT(DISTINCT natural_product_id) as cnt
            FROM bio_resource_natural_products
            GROUP BY bio_resource_id
        ) stats
        WHERE br.id = stats.bio_resource_id
    """)
    updated = cur.rowcount

    # 没有关联的设为0
    cur.execute("""
        UPDATE bio_resources
        SET num_of_natural_products = 0
        WHERE id NOT IN (SELECT DISTINCT bio_resource_id FROM bio_resource_natural_products)
    """)

    conn.commit()
    print(f"  - 更新完成: {updated} 条记录")

    # 验证
    cur.execute("""
        SELECT
            AVG(num_of_natural_products)::numeric(10,2) as avg_np,
            MAX(num_of_natural_products) as max_np,
            COUNT(*) FILTER (WHERE num_of_natural_products > 0) as has_np_count
        FROM bio_resources
    """)
    row = cur.fetchone()
    print(f"  - 统计: avg={row[0]}, max={row[1]}, 有关联记录数={row[2]}")

    cur.close()


def update_targets_stats(conn):
    """更新 targets 表的统计字段"""
    print(f"[{datetime.now()}] 更新 targets 统计字段...")
    cur = conn.cursor()

    # 检查是否有统计字段
    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'targets' AND column_name = 'num_of_natural_products'
    """)
    if not cur.fetchone():
        print("  - 添加 num_of_natural_products 字段...")
        cur.execute("ALTER TABLE targets ADD COLUMN num_of_natural_products INTEGER DEFAULT 0")
        conn.commit()

    cur.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'targets' AND column_name = 'num_of_activities'
    """)
    if not cur.fetchone():
        print("  - 添加 num_of_activities 字段...")
        cur.execute("ALTER TABLE targets ADD COLUMN num_of_activities INTEGER DEFAULT 0")
        conn.commit()

    # 更新 num_of_natural_products
    print("  - 更新 num_of_natural_products...")
    cur.execute("""
        UPDATE targets t
        SET num_of_natural_products = COALESCE(stats.cnt, 0)
        FROM (
            SELECT target_id, COUNT(DISTINCT natural_product_id) as cnt
            FROM bioactivity
            GROUP BY target_id
        ) stats
        WHERE t.id = stats.target_id
    """)
    updated1 = cur.rowcount

    # 没有活性数据的设为0
    cur.execute("""
        UPDATE targets
        SET num_of_natural_products = 0
        WHERE id NOT IN (SELECT DISTINCT target_id FROM bioactivity)
    """)

    # 更新 num_of_activities
    print("  - 更新 num_of_activities...")
    cur.execute("""
        UPDATE targets t
        SET num_of_activities = COALESCE(stats.cnt, 0)
        FROM (
            SELECT target_id, COUNT(*) as cnt
            FROM bioactivity
            GROUP BY target_id
        ) stats
        WHERE t.id = stats.target_id
    """)
    updated2 = cur.rowcount

    # 没有活性数据的设为0
    cur.execute("""
        UPDATE targets
        SET num_of_activities = 0
        WHERE id NOT IN (SELECT DISTINCT target_id FROM bioactivity)
    """)

    conn.commit()
    print(f"  - 更新完成: np={updated1}, activities={updated2}")

    # 验证
    cur.execute("""
        SELECT
            AVG(num_of_natural_products)::numeric(10,2) as avg_np,
            AVG(num_of_activities)::numeric(10,2) as avg_act,
            MAX(num_of_natural_products) as max_np,
            MAX(num_of_activities) as max_act
        FROM targets
    """)
    row = cur.fetchone()
    print(f"  - 统计: avg_np={row[0]}, avg_activities={row[1]}")
    print(f"  - 最大值: max_np={row[2]}, max_activities={row[3]}")

    cur.close()


def validate_data(conn):
    """验证数据完整性"""
    print(f"\n[{datetime.now()}] 数据验证...")
    cur = conn.cursor()

    # 检查外键完整性
    print("  - 检查 bioactivity 外键...")
    cur.execute("""
        SELECT COUNT(*) FROM bioactivity b
        WHERE NOT EXISTS (SELECT 1 FROM natural_products np WHERE np.id = b.natural_product_id)
    """)
    orphan_np = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM bioactivity b
        WHERE NOT EXISTS (SELECT 1 FROM targets t WHERE t.id = b.target_id)
    """)
    orphan_target = cur.fetchone()[0]

    print(f"    - 孤立记录(无NP): {orphan_np}, 孤立记录(无Target): {orphan_target}")

    print("  - 检查 bio_resource_natural_products 外键...")
    cur.execute("""
        SELECT COUNT(*) FROM bio_resource_natural_products brnp
        WHERE NOT EXISTS (SELECT 1 FROM natural_products np WHERE np.id = brnp.natural_product_id)
    """)
    orphan_np2 = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*) FROM bio_resource_natural_products brnp
        WHERE NOT EXISTS (SELECT 1 FROM bio_resources br WHERE br.id = brnp.bio_resource_id)
    """)
    orphan_br = cur.fetchone()[0]

    print(f"    - 孤立记录(无NP): {orphan_np2}, 孤立记录(无BR): {orphan_br}")

    print("  - 检查 toxicity 外键...")
    cur.execute("""
        SELECT COUNT(*) FROM toxicity t
        WHERE NOT EXISTS (SELECT 1 FROM natural_products np WHERE np.id = t.natural_product_id)
    """)
    orphan_np3 = cur.fetchone()[0]
    print(f"    - 孤立记录(无NP): {orphan_np3}")

    # 检查空值情况
    print("\n  - 检查关键字段空值...")
    cur.execute("SELECT COUNT(*) FROM natural_products WHERE np_id IS NULL")
    null_np_id = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM natural_products WHERE smiles IS NULL")
    null_smiles = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM targets WHERE target_id IS NULL")
    null_target_id = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM bio_resources WHERE resource_id IS NULL")
    null_resource_id = cur.fetchone()[0]

    print(f"    - natural_products: np_id为空={null_np_id}, smiles为空={null_smiles}")
    print(f"    - targets: target_id为空={null_target_id}")
    print(f"    - bio_resources: resource_id为空={null_resource_id}")

    cur.close()


def main():
    print("=" * 60)
    print("统计字段更新脚本")
    print("=" * 60)

    # 连接数据库
    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)

    # 更新各表统计字段
    update_natural_products_stats(conn)
    update_bio_resources_stats(conn)
    update_targets_stats(conn)

    # 验证数据
    validate_data(conn)

    conn.close()

    print("\n" + "=" * 60)
    print("统计字段更新完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
