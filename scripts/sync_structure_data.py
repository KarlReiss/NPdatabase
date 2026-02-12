#!/usr/bin/env python3
"""
同步 npass_structures 表的结构数据到 natural_products 表
用于补充 natural_products 表中缺失的 inchi, smiles, inchikey 字段
"""

import psycopg2
from datetime import datetime

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'npdb',
    'user': 'yfguo',
    'password': 'npdb2024'
}

def sync_structure_data():
    """同步结构数据"""
    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # 1. 统计需要更新的记录数
        print(f"\n[{datetime.now()}] 统计需要更新的记录...")
        cursor.execute("""
            SELECT
                COUNT(*) FILTER (WHERE np.inchi IS NULL AND ns.inchi IS NOT NULL) as inchi_updates,
                COUNT(*) FILTER (WHERE np.smiles IS NULL AND ns.smiles IS NOT NULL) as smiles_updates,
                COUNT(*) FILTER (WHERE np.inchikey IS NULL AND ns.inchikey IS NOT NULL) as inchikey_updates
            FROM natural_products np
            INNER JOIN npass_structures ns ON np.np_id = ns.np_id
            WHERE np.inchi IS NULL OR np.smiles IS NULL OR np.inchikey IS NULL;
        """)
        stats = cursor.fetchone()
        print(f"  - 可更新 inchi: {stats[0]} 条")
        print(f"  - 可更新 smiles: {stats[1]} 条")
        print(f"  - 可更新 inchikey: {stats[2]} 条")

        if stats[0] == 0 and stats[1] == 0 and stats[2] == 0:
            print("\n没有需要更新的数据!")
            return

        # 2. 执行更新
        print(f"\n[{datetime.now()}] 开始更新数据...")
        update_sql = """
            UPDATE natural_products np
            SET
                inchi = COALESCE(np.inchi, ns.inchi),
                smiles = COALESCE(np.smiles, ns.smiles),
                inchikey = COALESCE(np.inchikey, ns.inchikey),
                updated_at = CURRENT_TIMESTAMP
            FROM npass_structures ns
            WHERE np.np_id = ns.np_id
                AND (np.inchi IS NULL OR np.smiles IS NULL OR np.inchikey IS NULL)
                AND (ns.inchi IS NOT NULL OR ns.smiles IS NOT NULL OR ns.inchikey IS NOT NULL);
        """

        cursor.execute(update_sql)
        updated_count = cursor.rowcount
        conn.commit()

        print(f"  - 成功更新 {updated_count} 条记录")

        # 3. 验证更新结果
        print(f"\n[{datetime.now()}] 验证更新结果...")
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(*) FILTER (WHERE inchi IS NULL) as missing_inchi,
                COUNT(*) FILTER (WHERE smiles IS NULL) as missing_smiles,
                COUNT(*) FILTER (WHERE inchikey IS NULL) as missing_inchikey
            FROM natural_products;
        """)
        result = cursor.fetchone()
        print(f"  - 总记录数: {result[0]}")
        print(f"  - 缺失 inchi: {result[1]} 条")
        print(f"  - 缺失 smiles: {result[2]} 条")
        print(f"  - 缺失 inchikey: {result[3]} 条")

        print(f"\n[{datetime.now()}] 同步完成!")

    except Exception as e:
        print(f"错误: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("同步 npass_structures 结构数据到 natural_products")
    print("=" * 60)
    sync_structure_data()
    print("=" * 60)
