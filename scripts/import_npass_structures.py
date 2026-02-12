#!/usr/bin/env python3
"""
NPASS 结构数据导入脚本
用法: python3 import_npass_structures.py
"""

import psycopg2
from psycopg2.extras import execute_batch
import sys
from pathlib import Path

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'npdb',
    'user': 'yfguo',
    'password': 'npdb2024'
}

DATA_FILE = '/home/yfguo/NPdatabase/data/NPASS/NPASS3.0_naturalproducts_structure.txt'
BATCH_SIZE = 5000

def main():
    print("连接数据库...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print(f"读取数据文件: {DATA_FILE}")
        data_path = Path(DATA_FILE)

        if not data_path.exists():
            print(f"错误: 文件不存在 {DATA_FILE}")
            sys.exit(1)

        # 清空现有数据（可选）
        print("清空现有数据...")
        cursor.execute("TRUNCATE TABLE npass_structures RESTART IDENTITY;")
        conn.commit()

        # 读取并批量插入数据
        print("开始导入数据...")
        batch = []
        total_count = 0
        error_count = 0

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            # 跳过标题行
            header = f.readline()
            print(f"标题行: {header.strip()}")

            for line_num, line in enumerate(f, start=2):
                try:
                    line = line.strip()
                    if not line:
                        continue

                    parts = line.split('\t')
                    if len(parts) < 4:
                        print(f"警告: 第 {line_num} 行数据不完整，跳过")
                        error_count += 1
                        continue

                    np_id = parts[0].strip()
                    inchi = parts[1].strip() if len(parts) > 1 else None
                    inchikey = parts[2].strip() if len(parts) > 2 else None
                    smiles = parts[3].strip() if len(parts) > 3 else None

                    # 处理空值
                    if inchi == '': inchi = None
                    if inchikey == '': inchikey = None
                    if smiles == '': smiles = None

                    batch.append((np_id, inchi, inchikey, smiles))

                    # 批量插入
                    if len(batch) >= BATCH_SIZE:
                        execute_batch(
                            cursor,
                            "INSERT INTO npass_structures (np_id, inchi, inchikey, smiles) VALUES (%s, %s, %s, %s)",
                            batch
                        )
                        conn.commit()
                        total_count += len(batch)
                        print(f"已导入 {total_count} 条记录...")
                        batch = []

                except Exception as e:
                    print(f"错误: 第 {line_num} 行处理失败: {e}")
                    error_count += 1
                    continue

        # 插入剩余数据
        if batch:
            execute_batch(
                cursor,
                "INSERT INTO npass_structures (np_id, inchi, inchikey, smiles) VALUES (%s, %s, %s, %s)",
                batch
            )
            conn.commit()
            total_count += len(batch)

        print(f"\n导入完成!")
        print(f"成功导入: {total_count} 条记录")
        print(f"错误记录: {error_count} 条")

        # 验证导入结果
        cursor.execute("SELECT COUNT(*) FROM npass_structures;")
        db_count = cursor.fetchone()[0]
        print(f"数据库中记录数: {db_count}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
