#!/usr/bin/env python3
"""
导入靶点数据到 targets 表
数据源: NPASS + CMAUP
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
NPASS_TARGET = f'{DATA_DIR}/NPASS/NPASS3.0_target.txt'
CMAUP_TARGET = f'{DATA_DIR}/CMAUP/CMAUPv2.0_download_Targets.txt'


def clean_value(val):
    """清理数据值，将 n.a. 和空字符串转为 None"""
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in ('n.a.', 'n.a', 'na', '', '-'):
            return None
    return val


def load_npass_targets():
    """加载NPASS靶点数据"""
    print(f"[{datetime.now()}] 加载 NPASS targets...")
    df = pd.read_csv(NPASS_TARGET, sep='\t', dtype=str)
    print(f"  - 记录数: {len(df)}")

    # 查看列名
    print(f"  - 列名: {list(df.columns)}")
    return df


def load_cmaup_targets():
    """加载CMAUP靶点数据"""
    print(f"[{datetime.now()}] 加载 CMAUP targets...")
    df = pd.read_csv(CMAUP_TARGET, sep='\t', dtype=str)
    print(f"  - 记录数: {len(df)}")

    # 查看列名
    print(f"  - 列名: {list(df.columns)}")
    return df


def prepare_records(df_npass, df_cmaup):
    """准备插入数据库的记录"""
    print(f"[{datetime.now()}] 准备数据库记录...")

    records = []
    seen_ids = set()

    # 处理NPASS数据
    for _, row in df_npass.iterrows():
        target_id = clean_value(row.get('target_id'))
        if not target_id or target_id in seen_ids:
            continue
        seen_ids.add(target_id)

        record = {
            'target_id': target_id,
            'target_type': clean_value(row.get('target_type')),
            'target_name': clean_value(row.get('target_name')),
            'target_organism': clean_value(row.get('target_organism')),
            'target_organism_tax_id': clean_value(row.get('target_organism_tax_id')),
            'uniprot_id': clean_value(row.get('uniprot_id')),
        }
        records.append(record)

    print(f"  - NPASS靶点数: {len(records)}")

    # 处理CMAUP数据（补充不在NPASS中的）
    cmaup_added = 0
    for _, row in df_cmaup.iterrows():
        target_id = clean_value(row.get('Target_ID'))
        if not target_id or target_id in seen_ids:
            # 如果已存在，尝试补充uniprot_id
            continue
        seen_ids.add(target_id)

        record = {
            'target_id': target_id,
            'target_type': clean_value(row.get('Target_type')),
            'target_name': clean_value(row.get('Protein_Name')),
            'target_organism': 'Homo sapiens',  # CMAUP主要是人类靶点
            'target_organism_tax_id': '9606',
            'uniprot_id': clean_value(row.get('Uniprot_ID')),
        }
        records.append(record)
        cmaup_added += 1

    print(f"  - CMAUP新增靶点数: {cmaup_added}")
    print(f"  - 总靶点数: {len(records)}")

    return records


def insert_to_db(records, batch_size=1000):
    """批量插入数据库"""
    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 插入SQL
    insert_sql = """
        INSERT INTO targets (
            target_id, target_type, target_name,
            target_organism, target_organism_tax_id, uniprot_id
        ) VALUES %s
        ON CONFLICT (target_id) DO UPDATE SET
            target_type = COALESCE(EXCLUDED.target_type, targets.target_type),
            target_name = COALESCE(EXCLUDED.target_name, targets.target_name),
            target_organism = COALESCE(EXCLUDED.target_organism, targets.target_organism),
            target_organism_tax_id = COALESCE(EXCLUDED.target_organism_tax_id, targets.target_organism_tax_id),
            uniprot_id = COALESCE(EXCLUDED.uniprot_id, targets.uniprot_id),
            updated_at = CURRENT_TIMESTAMP
    """

    # 转换为元组列表
    values = [
        (
            r['target_id'], r['target_type'], r['target_name'],
            r['target_organism'], r['target_organism_tax_id'], r['uniprot_id']
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
        print(f"  - 进度: {inserted}/{total} ({100*inserted/total:.1f}%)")

    # 验证
    cur.execute("SELECT COUNT(*) FROM targets")
    count = cur.fetchone()[0]
    print(f"[{datetime.now()}] 导入完成! 表中总记录数: {count}")

    cur.close()
    conn.close()

    return count


def main():
    print("=" * 60)
    print("靶点数据导入脚本")
    print("=" * 60)

    # 加载数据
    df_npass = load_npass_targets()
    df_cmaup = load_cmaup_targets()

    # 准备记录
    records = prepare_records(df_npass, df_cmaup)

    # 插入数据库
    count = insert_to_db(records)

    print("=" * 60)
    print(f"导入完成! 共导入 {count} 条靶点记录")
    print("=" * 60)


if __name__ == '__main__':
    main()
