#!/usr/bin/env python3
"""
导入毒性数据到 toxicity 表
数据源: NPASS toxicity
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': 'yfguo',
    'host': 'localhost',
    'port': 5432
}

# 数据文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data'
NPASS_TOXICITY = f'{DATA_DIR}/NPASS/NPASS3.0_toxicity.txt'


def clean_value(val):
    """清理数据值，将 n.a. 和空字符串转为 None"""
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in ('n.a.', 'n.a', 'na', '', '-'):
            return None
    return val


def load_np_mapping(conn):
    """加载natural_products ID映射"""
    print(f"[{datetime.now()}] 加载ID映射...")
    cur = conn.cursor()
    cur.execute("SELECT np_id, id FROM natural_products")
    np_map = {row[0]: row[1] for row in cur.fetchall()}
    print(f"  - natural_products映射: {len(np_map)} 条")
    cur.close()
    return np_map


def process_toxicity_data(np_map):
    """处理毒性数据"""
    print(f"[{datetime.now()}] 加载 NPASS toxicity...")

    df = pd.read_csv(NPASS_TOXICITY, sep='\t', dtype=str)
    print(f"  - 原始记录数: {len(df)}")

    records = []
    skipped_np = 0

    for _, row in df.iterrows():
        np_id = clean_value(row.get('np_id'))

        # 查找外键ID
        if np_id not in np_map:
            skipped_np += 1
            continue

        # 解析毒性值
        toxicity_value = None
        try:
            val = clean_value(row.get('activity_value'))
            if val:
                toxicity_value = float(val)
                # 负数或超大值设为None
                if toxicity_value < 0 or toxicity_value > 1e13:
                    toxicity_value = None
        except (ValueError, TypeError):
            pass

        record = {
            'natural_product_id': np_map[np_id],
            'toxicity_type': clean_value(row.get('activity_type')),
            'toxicity_value': toxicity_value,
            'toxicity_units': clean_value(row.get('activity_units')),
            'assay_organism': clean_value(row.get('assay_organism')),
            'ref_id': clean_value(row.get('ref_id')),
            'ref_id_type': clean_value(row.get('ref_id_type')),
        }
        records.append(record)

    print(f"  - 有效记录数: {len(records)}")
    print(f"  - 跳过(无匹配NP): {skipped_np}")

    return records


def insert_to_db(conn, records, batch_size=2000):
    """批量插入数据库"""
    cur = conn.cursor()

    # 插入SQL
    insert_sql = """
        INSERT INTO toxicity (
            natural_product_id, toxicity_type, toxicity_value, toxicity_units,
            assay_organism, ref_id, ref_id_type
        ) VALUES %s
    """

    # 转换为元组列表
    values = [
        (
            r['natural_product_id'], r['toxicity_type'], r['toxicity_value'], r['toxicity_units'],
            r['assay_organism'], r['ref_id'], r['ref_id_type']
        )
        for r in records
    ]

    # 批量插入
    total = len(values)
    inserted = 0

    print(f"[{datetime.now()}] 开始插入数据 (共 {total} 条)...")

    for i in range(0, total, batch_size):
        batch = values[i:i+batch_size]
        execute_values(cur, insert_sql, batch, page_size=batch_size)
        conn.commit()
        inserted += len(batch)
        if inserted % 10000 == 0 or inserted == total:
            print(f"  - 进度: {inserted}/{total} ({100*inserted/total:.1f}%)")

    # 验证
    cur.execute("SELECT COUNT(*) FROM toxicity")
    count = cur.fetchone()[0]
    print(f"[{datetime.now()}] 导入完成! 表中总记录数: {count}")

    cur.close()
    return count


def main():
    print("=" * 60)
    print("毒性数据导入脚本")
    print("=" * 60)

    # 连接数据库
    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)

    # 加载ID映射
    np_map = load_np_mapping(conn)

    # 处理数据
    records = process_toxicity_data(np_map)

    # 插入数据库
    count = insert_to_db(conn, records)

    conn.close()

    print("=" * 60)
    print(f"导入完成! 共导入 {count} 条毒性记录")
    print("=" * 60)


if __name__ == '__main__':
    main()
