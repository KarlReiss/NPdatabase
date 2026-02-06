#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新natural_products表 - 使用NPASS+CMAUP整合数据

功能：
1. 清空natural_products表的现有数据
2. 从整合文件导入新数据
3. 删除不必要的字段（cmaup_np_id, data_source, match_method, name_initial）
4. 调整字段映射以匹配数据库结构

作者：Claude Code
日期：2026-02-05
"""

import psycopg2
import csv
import os
from datetime import datetime

# 配置
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'npdb'
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

INTEGRATED_FILE = '/home/yfguo/NPdatabase/data/processed/natural_products_integrated.txt'
BATCH_SIZE = 1000

# 字段映射：整合文件字段 -> 数据库字段
# 不需要的字段：cmaup_np_id, data_source, match_method, name_initial, gene_cluster
FIELD_MAPPING = {
    'np_id': 'np_id',
    'inchikey': 'inchikey',
    'pref_name': 'pref_name',
    'iupac_name': 'iupac_name',
    # 'name_initial': None,  # 删除
    'chembl_id': 'chembl_id',
    'pubchem_id': 'pubchem_id',
    'molecular_weight': 'molecular_weight',
    'log_s': 'log_s',  # 新增字段
    'log_d': 'log_d',  # 新增字段
    'log_p': 'log_p',  # 新增字段（原始值）
    'h_bond_acceptors': 'h_bond_acceptors',
    'h_bond_donors': 'h_bond_donors',
    'tpsa': 'tpsa',  # 新增字段（原始值）
    'rotatable_bonds': 'rotatable_bonds',
    'ring_count': 'ring_count',  # 新增字段
    'inchi': 'inchi',
    'smiles': 'smiles',
    'num_of_organism': 'num_of_organism',
    'num_of_target': 'num_of_target',
    'num_of_activity': 'num_of_activity',
    'if_quantity': 'if_quantity',  # 恢复字段
    # 'gene_cluster': None,  # 已删除（无数据）
    # 'cmaup_np_id': None,  # 删除
    # 'data_source': None,  # 删除
    # 'match_method': None,  # 删除
}


def connect_db():
    """连接数据库"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        raise


def convert_value(value, field_name):
    """
    转换字段值

    参数：
        value: 原始值（字符串）
        field_name: 数据库字段名

    返回：
        转换后的值
    """
    # 空值处理
    if value == '' or value == 'n.a.' or value == 'N.A.':
        return None

    # 布尔值字段
    if field_name == 'if_quantity':
        return value.lower() in ('yes', 'true', '1')

    # 数值字段
    numeric_fields = ['molecular_weight', 'xlogp', 'psa', 'log_s', 'log_d', 'log_p', 'tpsa',
                     'h_bond_donors', 'h_bond_acceptors', 'rotatable_bonds', 'ring_count',
                     'num_of_organism', 'num_of_target', 'num_of_activity']
    if field_name in numeric_fields:
        try:
            if field_name in ['molecular_weight', 'xlogp', 'psa', 'log_s', 'log_d', 'log_p', 'tpsa']:
                return float(value) if value else None
            else:
                # 先转换为float再转为int（处理'0.0'这样的值）
                return int(float(value)) if value else None
        except ValueError:
            return None

    # 文本字段
    return value if value else None


def clear_table(conn):
    """清空natural_products表"""
    print("\n正在清空natural_products表...")
    cursor = conn.cursor()
    try:
        # 先删除所有记录
        cursor.execute("TRUNCATE TABLE natural_products RESTART IDENTITY CASCADE;")
        conn.commit()
        print("  ✓ 表已清空")
    except Exception as e:
        conn.rollback()
        print(f"  ✗ 清空表失败: {e}")
        raise
    finally:
        cursor.close()


def import_data(conn):
    """导入整合数据"""
    print(f"\n正在从整合文件导入数据...")
    print(f"  文件: {INTEGRATED_FILE}")

    cursor = conn.cursor()

    # 读取整合文件
    with open(INTEGRATED_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')

        # 获取需要导入的数据库字段
        db_fields = [db_field for file_field, db_field in FIELD_MAPPING.items()
                    if db_field is not None]

        # 构建INSERT语句
        placeholders = ', '.join(['%s'] * len(db_fields))
        insert_sql = f"""
            INSERT INTO natural_products ({', '.join(db_fields)})
            VALUES ({placeholders})
        """

        batch = []
        total_count = 0
        success_count = 0
        error_count = 0

        for row_num, row in enumerate(reader, start=1):
            try:
                # 转换数据
                values = []
                for file_field, db_field in FIELD_MAPPING.items():
                    if db_field is not None:
                        value = convert_value(row.get(file_field, ''), db_field)
                        values.append(value)

                batch.append(tuple(values))
                total_count += 1

                # 批量插入
                if len(batch) >= BATCH_SIZE:
                    try:
                        cursor.executemany(insert_sql, batch)
                        conn.commit()
                        success_count += len(batch)
                        print(f"  - 已导入 {success_count:,} 条记录...")
                        batch = []
                    except Exception as e:
                        conn.rollback()
                        error_count += len(batch)
                        print(f"  ✗ 批量插入失败 (行 {row_num}): {e}")
                        batch = []

            except Exception as e:
                error_count += 1
                print(f"  ✗ 处理行 {row_num} 失败: {e}")
                continue

        # 插入剩余的记录
        if batch:
            try:
                cursor.executemany(insert_sql, batch)
                conn.commit()
                success_count += len(batch)
                print(f"  - 已导入 {success_count:,} 条记录...")
            except Exception as e:
                conn.rollback()
                error_count += len(batch)
                print(f"  ✗ 最后一批插入失败: {e}")

    cursor.close()

    print(f"\n导入完成:")
    print(f"  - 总记录数: {total_count:,}")
    print(f"  - 成功导入: {success_count:,}")
    print(f"  - 失败记录: {error_count:,}")

    return success_count, error_count


def verify_import(conn):
    """验证导入结果"""
    print("\n正在验证导入结果...")
    cursor = conn.cursor()

    try:
        # 1. 记录数
        cursor.execute("SELECT COUNT(*) FROM natural_products;")
        count = cursor.fetchone()[0]
        print(f"  - 总记录数: {count:,}")

        # 2. 有理化性质的记录数
        cursor.execute("""
            SELECT COUNT(*) FROM natural_products
            WHERE molecular_weight IS NOT NULL;
        """)
        mw_count = cursor.fetchone()[0]
        print(f"  - 有分子量的记录: {mw_count:,} ({mw_count/count*100:.2f}%)")

        # 3. 有SMILES的记录数
        cursor.execute("""
            SELECT COUNT(*) FROM natural_products
            WHERE smiles IS NOT NULL AND smiles != '';
        """)
        smiles_count = cursor.fetchone()[0]
        print(f"  - 有SMILES的记录: {smiles_count:,} ({smiles_count/count*100:.2f}%)")

        # 4. 有InChIKey的记录数
        cursor.execute("""
            SELECT COUNT(*) FROM natural_products
            WHERE inchikey IS NOT NULL AND inchikey != '';
        """)
        inchikey_count = cursor.fetchone()[0]
        print(f"  - 有InChIKey的记录: {inchikey_count:,} ({inchikey_count/count*100:.2f}%)")

        # 5. 有生物学信息的记录数
        cursor.execute("""
            SELECT COUNT(*) FROM natural_products
            WHERE num_of_organism > 0 OR num_of_target > 0 OR num_of_activity > 0;
        """)
        bio_count = cursor.fetchone()[0]
        print(f"  - 有生物学信息的记录: {bio_count:,} ({bio_count/count*100:.2f}%)")

        # 6. 示例记录
        print("\n示例记录（前3条有完整数据的）:")
        cursor.execute("""
            SELECT np_id, pref_name, molecular_weight, xlogp, smiles,
                   num_of_organism, num_of_target
            FROM natural_products
            WHERE molecular_weight IS NOT NULL
              AND smiles IS NOT NULL
              AND smiles != ''
            LIMIT 3;
        """)

        for row in cursor.fetchall():
            print(f"\n  np_id: {row[0]}")
            print(f"  名称: {row[1][:60]}...")
            print(f"  分子量: {row[2]}")
            print(f"  LogP: {row[3]}")
            print(f"  SMILES: {row[4][:60]}...")
            print(f"  生物体数: {row[5]}, 靶点数: {row[6]}")

        print("\n✓ 验证完成")

    except Exception as e:
        print(f"  ✗ 验证失败: {e}")
    finally:
        cursor.close()


def main():
    """主函数"""
    print("=" * 80)
    print("更新natural_products表 - 使用NPASS+CMAUP整合数据")
    print("=" * 80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 检查文件是否存在
    if not os.path.exists(INTEGRATED_FILE):
        print(f"\n✗ 错误: 整合文件不存在: {INTEGRATED_FILE}")
        return

    print(f"\n数据库配置:")
    print(f"  - 主机: {DB_HOST}:{DB_PORT}")
    print(f"  - 数据库: {DB_NAME}")
    print(f"  - 用户: {DB_USER}")

    # 连接数据库
    try:
        conn = connect_db()
        print("  ✓ 数据库连接成功")
    except Exception as e:
        print(f"  ✗ 数据库连接失败: {e}")
        return

    try:
        # 1. 清空表
        clear_table(conn)

        # 2. 导入数据
        success_count, error_count = import_data(conn)

        # 3. 验证导入
        verify_import(conn)

        print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        print("✓ 更新完成！")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ 更新失败: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
