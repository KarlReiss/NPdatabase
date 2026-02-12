#!/usr/bin/env python3
"""
将合并后的数据导入到MySQL数据库
"""

import pandas as pd
import pymysql
from pymysql import Error
import sys
from pathlib import Path

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Gyf20021211',
    'database': 'natural_products',
    'charset': 'utf8mb4'
}

# 数据文件路径
COMPOUNDS_FILE = 'data/processed/merged_compounds.csv'
TARGETS_FILE = 'data/processed/merged_targets.csv'

def get_db_connection():
    """创建数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print(f"成功连接到数据库: {DB_CONFIG['database']}")
        return connection
    except Error as e:
        print(f"数据库连接失败: {e}")
        sys.exit(1)

def import_compounds(connection):
    """导入化合物数据"""
    print("\n开始导入化合物数据...")

    # 读取数据
    df = pd.read_csv(COMPOUNDS_FILE, low_memory=False)
    print(f"读取到 {len(df)} 条化合物记录")

    cursor = connection.cursor()

    # 批量插入
    batch_size = 1000
    total = len(df)
    success_count = 0
    error_count = 0

    for i in range(0, total, batch_size):
        batch = df.iloc[i:i+batch_size]

        for _, row in batch.iterrows():
            try:
                sql = """
                INSERT INTO compounds (
                    source, compound_id, compound_name, molecular_formula,
                    molecular_weight, smiles, inchi, inchikey
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    compound_name = VALUES(compound_name),
                    molecular_formula = VALUES(molecular_formula),
                    molecular_weight = VALUES(molecular_weight),
                    smiles = VALUES(smiles),
                    inchi = VALUES(inchi),
                    inchikey = VALUES(inchikey)
                """

                cursor.execute(sql, (
                    row.get('source'),
                    row.get('compound_id'),
                    row.get('compound_name'),
                    row.get('molecular_formula'),
                    row.get('molecular_weight'),
                    row.get('smiles'),
                    row.get('inchi'),
                    row.get('inchikey')
                ))
                success_count += 1

            except Error as e:
                error_count += 1
                if error_count <= 10:  # 只打印前10个错误
                    print(f"插入错误: {e}")

        connection.commit()
        print(f"进度: {min(i+batch_size, total)}/{total} ({success_count} 成功, {error_count} 失败)")

    cursor.close()
    print(f"\n化合物导入完成: {success_count} 成功, {error_count} 失败")

def import_targets(connection):
    """导入靶点数据"""
    print("\n开始导入靶点数据...")

    # 读取数据
    df = pd.read_csv(TARGETS_FILE, low_memory=False)
    print(f"读取到 {len(df)} 条靶点记录")

    cursor = connection.cursor()

    # 批量插入
    batch_size = 1000
    total = len(df)
    success_count = 0
    error_count = 0

    for i in range(0, total, batch_size):
        batch = df.iloc[i:i+batch_size]

        for _, row in batch.iterrows():
            try:
                sql = """
                INSERT INTO targets (
                    source, compound_id, target_name, uniprot_id,
                    activity_type, activity_value, target_id, target_type, gene_name
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    target_name = VALUES(target_name),
                    uniprot_id = VALUES(uniprot_id),
                    activity_type = VALUES(activity_type),
                    activity_value = VALUES(activity_value),
                    target_type = VALUES(target_type),
                    gene_name = VALUES(gene_name)
                """

                cursor.execute(sql, (
                    row.get('source'),
                    row.get('compound_id'),
                    row.get('target_name'),
                    row.get('uniprot_id'),
                    row.get('activity_type'),
                    row.get('activity_value'),
                    row.get('target_id'),
                    row.get('target_type'),
                    row.get('gene_name')
                ))
                success_count += 1

            except Error as e:
                error_count += 1
                if error_count <= 10:  # 只打印前10个错误
                    print(f"插入错误: {e}")

        connection.commit()
        print(f"进度: {min(i+batch_size, total)}/{total} ({success_count} 成功, {error_count} 失败)")

    cursor.close()
    print(f"\n靶点导入完成: {success_count} 成功, {error_count} 失败")

def main():
    """主函数"""
    print("=" * 60)
    print("开始导入数据到数据库")
    print("=" * 60)

    # 检查文件是否存在
    if not Path(COMPOUNDS_FILE).exists():
        print(f"错误: 找不到化合物数据文件 {COMPOUNDS_FILE}")
        sys.exit(1)

    if not Path(TARGETS_FILE).exists():
        print(f"错误: 找不到靶点数据文件 {TARGETS_FILE}")
        sys.exit(1)

    # 连接数据库
    connection = get_db_connection()

    try:
        # 导入化合物数据
        import_compounds(connection)

        # 导入靶点数据
        import_targets(connection)

        print("\n" + "=" * 60)
        print("数据导入完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n导入过程中出错: {e}")
        connection.rollback()
    finally:
        connection.close()
        print("数据库连接已关闭")

if __name__ == '__main__':
    main()
