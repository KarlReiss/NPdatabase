#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 bio_resources_with_tcmid.txt 更新数据库中的 bio_resources 表

功能:
1. 读取 bio_resources_with_tcmid.txt
2. 映射字段到数据库表结构
3. 添加 TCMID 相关字段
4. 清空并重新导入数据

作者: Claude Code
日期: 2026-02-05
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
import sys

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'npdb',
    'user': os.environ.get('DB_USER', 'yfguo'),
    'password': os.environ.get('DB_PASSWORD', '')
}

# 文件路径
INPUT_FILE = "/home/yfguo/NPdatabase/data/processed/bio_resources_with_tcmid.txt"

# 字段映射: bio_resources_with_tcmid.txt -> bio_resources 表
FIELD_MAPPING = {
    # 基本标识
    'org_id': 'resource_id',                    # NPO16221 -> resource_id

    # 名称信息
    'org_name': 'latin_name',                   # 拉丁名
    'tcmid_chinese_name': 'chinese_name',       # TCMID 中文名

    # 分类学信息
    'kingdom_name': 'taxonomy_kingdom',         # 界
    'family_name': 'taxonomy_family',           # 科
    'genus_name': 'taxonomy_genus',             # 属
    'species_name': 'taxonomy_species',         # 种
    'org_tax_id': 'taxonomy_id',                # NCBI Taxonomy ID

    # CMAUP 补充字段
    'species_tax_id': 'species_tax_id',         # 种的Taxonomy ID
    'genus_tax_id': 'genus_tax_id',             # 属的Taxonomy ID
    'family_tax_id': 'family_tax_id',           # 科的Taxonomy ID
    'cmaup_id': 'cmaup_id',                     # CMAUP ID

    # TCMID 字段
    'tcmid_component_id': 'tcmid_id',           # TCMID Component ID

    # 统计信息
    'num_of_np_act': 'num_of_natural_products', # 有活性的天然产物数
}


def connect_db():
    """连接数据库"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"✓ 成功连接到数据库: {DB_CONFIG['database']}")
        return conn
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        sys.exit(1)


def load_data(file_path):
    """加载数据文件"""
    print(f"\n正在加载数据文件: {file_path}")
    df = pd.read_csv(file_path, sep='\t', encoding='utf-8', low_memory=False)
    print(f"✓ 加载完成: {len(df)} 条记录, {len(df.columns)} 个字段")
    return df


def determine_resource_type(row):
    """根据分类信息判断资源类型"""
    kingdom = str(row.get('kingdom_name', '')).lower()

    if 'plant' in kingdom or 'viridiplantae' in kingdom:
        return 'Plant'
    elif 'animal' in kingdom or 'metazoa' in kingdom:
        return 'Animal'
    elif 'fung' in kingdom:
        return 'Fungus'
    elif 'bacteria' in kingdom or 'archaea' in kingdom:
        return 'Microorganism'
    else:
        return 'Unknown'


def transform_data(df):
    """转换数据格式，映射到数据库字段"""
    print("\n正在转换数据格式...")

    # 去重：保留第一条记录
    original_count = len(df)
    df = df.drop_duplicates(subset=['org_id'], keep='first')
    if len(df) < original_count:
        print(f"  去重: {original_count} -> {len(df)} 条记录 (删除 {original_count - len(df)} 条重复)")

    records = []
    for idx, row in df.iterrows():
        record = {}

        # 映射字段
        for src_field, dst_field in FIELD_MAPPING.items():
            value = row.get(src_field)
            # 处理空值
            if pd.isna(value) or value == '':
                record[dst_field] = None
            else:
                record[dst_field] = str(value)

        # 添加资源类型
        record['resource_type'] = determine_resource_type(row)

        # 处理中文名（如果为空，使用拉丁名）
        if not record.get('chinese_name'):
            record['chinese_name'] = record.get('latin_name')

        records.append(record)

    print(f"✓ 转换完成: {len(records)} 条记录")
    return records


def add_tcmid_fields(conn):
    """添加 TCMID 相关字段到 bio_resources 表"""
    print("\n正在添加 TCMID 相关字段...")

    cursor = conn.cursor()

    try:
        # 添加 tcmid_id 字段（如果不存在）
        cursor.execute("""
            ALTER TABLE bio_resources
            ADD COLUMN IF NOT EXISTS tcmid_id VARCHAR(500);
        """)

        # 添加索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_bio_resources_tcmid_id
            ON bio_resources(tcmid_id);
        """)

        # 添加注释
        cursor.execute("""
            COMMENT ON COLUMN bio_resources.tcmid_id
            IS 'TCMID Component ID (多个用逗号分隔)';
        """)

        conn.commit()
        print("✓ TCMID 字段添加完成")

    except Exception as e:
        conn.rollback()
        print(f"✗ 添加字段失败: {e}")
        raise
    finally:
        cursor.close()


def clear_table(conn):
    """清空 bio_resources 表"""
    print("\n正在清空 bio_resources 表...")

    cursor = conn.cursor()

    try:
        cursor.execute("TRUNCATE TABLE bio_resources CASCADE;")
        conn.commit()
        print("✓ 表已清空")

    except Exception as e:
        conn.rollback()
        print(f"✗ 清空表失败: {e}")
        raise
    finally:
        cursor.close()


def insert_data(conn, records):
    """批量插入数据"""
    print(f"\n正在插入数据: {len(records)} 条记录...")

    cursor = conn.cursor()

    # 构建插入语句
    fields = list(records[0].keys())
    placeholders = ', '.join(['%s'] * len(fields))
    insert_sql = f"""
        INSERT INTO bio_resources ({', '.join(fields)})
        VALUES ({placeholders})
    """

    try:
        # 准备数据
        values = []
        for record in records:
            values.append(tuple(record[field] for field in fields))

        # 批量插入
        batch_size = 1000
        total = len(values)

        for i in range(0, total, batch_size):
            batch = values[i:i+batch_size]
            cursor.executemany(insert_sql, batch)
            conn.commit()
            print(f"  已插入: {min(i+batch_size, total)}/{total} 条记录")

        print(f"✓ 数据插入完成: {total} 条记录")

    except Exception as e:
        conn.rollback()
        print(f"✗ 插入数据失败: {e}")
        raise
    finally:
        cursor.close()


def verify_data(conn):
    """验证数据"""
    print("\n正在验证数据...")

    cursor = conn.cursor()

    try:
        # 统计总记录数
        cursor.execute("SELECT COUNT(*) FROM bio_resources;")
        total = cursor.fetchone()[0]
        print(f"  总记录数: {total}")

        # 统计有 TCMID ID 的记录数
        cursor.execute("""
            SELECT COUNT(*) FROM bio_resources
            WHERE tcmid_id IS NOT NULL AND tcmid_id != '';
        """)
        tcmid_count = cursor.fetchone()[0]
        print(f"  有 TCMID ID 的记录: {tcmid_count} ({tcmid_count/total*100:.2f}%)")

        # 统计资源类型分布
        cursor.execute("""
            SELECT resource_type, COUNT(*)
            FROM bio_resources
            GROUP BY resource_type
            ORDER BY COUNT(*) DESC;
        """)
        print("\n  资源类型分布:")
        for row in cursor.fetchall():
            print(f"    {row[0]}: {row[1]}")

        # 显示示例记录
        cursor.execute("""
            SELECT resource_id, latin_name, chinese_name, tcmid_id
            FROM bio_resources
            WHERE tcmid_id IS NOT NULL AND tcmid_id != ''
            LIMIT 5;
        """)
        print("\n  示例记录 (有 TCMID ID):")
        for row in cursor.fetchall():
            print(f"    {row[0]}: {row[1]} ({row[2]}) - TCMID: {row[3][:50]}...")

        print("\n✓ 数据验证完成")

    except Exception as e:
        print(f"✗ 验证失败: {e}")
    finally:
        cursor.close()


def main():
    """主函数"""
    print("=" * 80)
    print("更新 bio_resources 表 - 使用 bio_resources_with_tcmid.txt")
    print("=" * 80)

    # 1. 加载数据
    df = load_data(INPUT_FILE)

    # 2. 转换数据
    records = transform_data(df)

    # 3. 连接数据库
    conn = connect_db()

    try:
        # 4. 添加 TCMID 字段
        add_tcmid_fields(conn)

        # 5. 清空表
        clear_table(conn)

        # 6. 插入数据
        insert_data(conn, records)

        # 7. 验证数据
        verify_data(conn)

        print("\n" + "=" * 80)
        print("✓ 更新完成!")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ 更新失败: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
