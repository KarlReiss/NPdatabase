#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导入 prescription_resources 数据

功能:
1. 读取 prescription_resources_data.txt
2. 合并重复的 (prescription_id, bio_resource_id)
3. 将字符串 ID 转换为数据库 ID (BIGINT)
4. 导入到 prescription_resources 表

作者: Claude Code
日期: 2026-02-05
"""

import pandas as pd
import psycopg2
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
INPUT_FILE = "/home/yfguo/NPdatabase/data/processed/prescription_resources_data.txt"


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
    df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
    print(f"✓ 加载完成: {len(df)} 条记录")
    return df


def merge_duplicates(df):
    """合并重复的 (prescription_id, bio_resource_id)"""
    print("\n正在合并重复记录...")

    original_count = len(df)

    # 按 (prescription_id, bio_resource_id) 分组
    # 合并 component_id (用逗号分隔)
    # 保留第一个 barcode
    merged = df.groupby(['prescription_id', 'bio_resource_id']).agg({
        'component_id': lambda x: ','.join(sorted(set(x.astype(str)))),
        'barcode': 'first'
    }).reset_index()

    print(f"  原始记录数: {original_count}")
    print(f"  合并后记录数: {len(merged)}")
    print(f"  合并了 {original_count - len(merged)} 条重复记录")

    return merged


def build_id_mappings(conn):
    """构建 ID 映射表"""
    print("\n正在构建 ID 映射...")

    cursor = conn.cursor()

    # 构建 prescription_id 映射: TCMF1 -> id (通过 tcmid_id 字段)
    cursor.execute("SELECT id, tcmid_id FROM prescriptions WHERE tcmid_id IS NOT NULL;")
    prescription_map = {row[1]: row[0] for row in cursor.fetchall()}
    print(f"  处方 ID 映射 (通过 tcmid_id): {len(prescription_map)} 个")

    # 构建 bio_resource_id 映射: NPO8101 -> id
    cursor.execute("SELECT id, resource_id FROM bio_resources;")
    bio_resource_map = {row[1]: row[0] for row in cursor.fetchall()}
    print(f"  生物资源 ID 映射: {len(bio_resource_map)} 个")

    cursor.close()

    return prescription_map, bio_resource_map


def transform_data(df, prescription_map, bio_resource_map):
    """转换数据：将字符串 ID 转换为数据库 ID"""
    print("\n正在转换数据...")

    records = []
    skipped = 0

    for idx, row in df.iterrows():
        prescription_str_id = row['prescription_id']
        bio_resource_str_id = row['bio_resource_id']

        # 查找数据库 ID
        prescription_id = prescription_map.get(prescription_str_id)
        bio_resource_id = bio_resource_map.get(bio_resource_str_id)

        # 如果找不到对应的 ID，跳过
        if prescription_id is None:
            skipped += 1
            continue

        if bio_resource_id is None:
            skipped += 1
            continue

        records.append({
            'prescription_id': prescription_id,
            'bio_resource_id': bio_resource_id,
            'tcmid_component_id': row['component_id']
        })

    print(f"  转换完成: {len(records)} 条记录")
    if skipped > 0:
        print(f"  跳过 {skipped} 条记录 (找不到对应的 ID)")

    return records


def clear_table(conn):
    """清空 prescription_resources 表"""
    print("\n正在清空 prescription_resources 表...")

    cursor = conn.cursor()

    try:
        cursor.execute("TRUNCATE TABLE prescription_resources CASCADE;")
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

    insert_sql = """
        INSERT INTO prescription_resources
        (prescription_id, bio_resource_id, tcmid_component_id)
        VALUES (%s, %s, %s)
    """

    try:
        # 准备数据
        values = [
            (r['prescription_id'], r['bio_resource_id'], r['tcmid_component_id'])
            for r in records
        ]

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
        cursor.execute("SELECT COUNT(*) FROM prescription_resources;")
        total = cursor.fetchone()[0]
        print(f"  总记录数: {total}")

        # 统计有 TCMID Component ID 的记录数
        cursor.execute("""
            SELECT COUNT(*) FROM prescription_resources
            WHERE tcmid_component_id IS NOT NULL AND tcmid_component_id != '';
        """)
        tcmid_count = cursor.fetchone()[0]
        print(f"  有 TCMID Component ID 的记录: {tcmid_count} ({tcmid_count/total*100:.2f}%)")

        # 统计唯一处方数
        cursor.execute("SELECT COUNT(DISTINCT prescription_id) FROM prescription_resources;")
        unique_prescriptions = cursor.fetchone()[0]
        print(f"  涉及的唯一处方数: {unique_prescriptions}")

        # 统计唯一生物资源数
        cursor.execute("SELECT COUNT(DISTINCT bio_resource_id) FROM prescription_resources;")
        unique_resources = cursor.fetchone()[0]
        print(f"  涉及的唯一生物资源数: {unique_resources}")

        # 检查唯一约束
        cursor.execute("""
            SELECT prescription_id, bio_resource_id, COUNT(*)
            FROM prescription_resources
            GROUP BY prescription_id, bio_resource_id
            HAVING COUNT(*) > 1;
        """)
        duplicates = cursor.fetchall()
        if duplicates:
            print(f"  ⚠ 发现 {len(duplicates)} 个违反唯一约束的记录")
        else:
            print(f"  ✓ 唯一约束验证通过")

        # 显示示例记录
        cursor.execute("""
            SELECT
                pr.prescription_id,
                p.prescription_id as prescription_code,
                pr.bio_resource_id,
                br.resource_id as resource_code,
                br.latin_name,
                br.chinese_name,
                LEFT(pr.tcmid_component_id, 50) as tcmid_preview
            FROM prescription_resources pr
            JOIN prescriptions p ON pr.prescription_id = p.id
            JOIN bio_resources br ON pr.bio_resource_id = br.id
            LIMIT 5;
        """)

        print("\n  示例记录:")
        for row in cursor.fetchall():
            print(f"    处方 {row[1]} + 生物资源 {row[3]} ({row[4]}, {row[5]}) - TCMID: {row[6]}...")

        print("\n✓ 数据验证完成")

    except Exception as e:
        print(f"✗ 验证失败: {e}")
    finally:
        cursor.close()


def main():
    """主函数"""
    print("=" * 80)
    print("导入 prescription_resources 数据")
    print("=" * 80)

    # 1. 加载数据
    df = load_data(INPUT_FILE)

    # 2. 合并重复记录
    df_merged = merge_duplicates(df)

    # 3. 连接数据库
    conn = connect_db()

    try:
        # 4. 构建 ID 映射
        prescription_map, bio_resource_map = build_id_mappings(conn)

        # 5. 转换数据
        records = transform_data(df_merged, prescription_map, bio_resource_map)

        # 6. 清空表
        clear_table(conn)

        # 7. 插入数据
        insert_data(conn, records)

        # 8. 验证数据
        verify_data(conn)

        print("\n" + "=" * 80)
        print("✓ 导入完成!")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ 导入失败: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
