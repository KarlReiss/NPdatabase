#!/usr/bin/env python3
"""
导入活性数据到 bioactivity 表
数据源: NPASS activities + CMAUP Ingredient_Target_Associations
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
NPASS_ACTIVITIES = f'{DATA_DIR}/NPASS/NPASS3.0_activities.txt'
CMAUP_ACTIVITIES = f'{DATA_DIR}/CMAUP/CMAUPv2.0_download_Ingredient_Target_Associations_ActivityValues_References.txt'


def clean_value(val):
    """清理数据值，将 n.a. 和空字符串转为 None"""
    if pd.isna(val):
        return None
    if isinstance(val, str):
        val = val.strip()
        if val.lower() in ('n.a.', 'n.a', 'na', '', '-'):
            return None
    return val


def load_id_mappings(conn):
    """加载ID映射表"""
    print(f"[{datetime.now()}] 加载ID映射...")

    # natural_products: np_id -> id
    cur = conn.cursor()
    cur.execute("SELECT np_id, id FROM natural_products")
    np_map = {row[0]: row[1] for row in cur.fetchall()}
    print(f"  - natural_products映射: {len(np_map)} 条")

    # targets: target_id -> id
    cur.execute("SELECT target_id, id FROM targets")
    target_map = {row[0]: row[1] for row in cur.fetchall()}
    print(f"  - targets映射: {len(target_map)} 条")

    cur.close()
    return np_map, target_map


def standardize_activity_value(value, units):
    """标准化活性值到nM"""
    if value is None:
        return None, 'nM'

    try:
        val = float(value)
        if val < 0 or val > 1e13:
            return None, 'nM'  # 负数或超大值返回None
    except (ValueError, TypeError):
        return None, 'nM'

    units_lower = str(units).lower() if units else ''

    # 转换到nM
    if 'um' in units_lower or 'μm' in units_lower or units_lower == 'microm':
        val = val * 1000  # μM -> nM
    elif 'mm' in units_lower:
        val = val * 1000000  # mM -> nM
    elif 'pm' in units_lower:
        val = val / 1000  # pM -> nM
    elif 'nm' in units_lower:
        pass  # 已经是nM
    elif 'ug/ml' in units_lower or 'μg/ml' in units_lower:
        pass  # 保持原值，无法直接转换
    # 其他单位保持原值

    return val, 'nM'


def process_npass_activities(np_map, target_map):
    """处理NPASS活性数据"""
    print(f"[{datetime.now()}] 加载 NPASS activities...")

    records = []
    skipped_np = 0
    skipped_target = 0

    # 分块读取大文件
    chunk_size = 50000
    for chunk_num, chunk in enumerate(pd.read_csv(NPASS_ACTIVITIES, sep='\t', dtype=str, chunksize=chunk_size)):
        for _, row in chunk.iterrows():
            np_id = clean_value(row.get('np_id'))
            target_id = clean_value(row.get('target_id'))

            # 查找外键ID
            if np_id not in np_map:
                skipped_np += 1
                continue
            if target_id not in target_map:
                skipped_target += 1
                continue

            # 解析活性值（负数和超大值设为None，因为数据库有检查约束和精度限制）
            activity_value = None
            try:
                val = clean_value(row.get('activity_value'))
                if val:
                    activity_value = float(val)
                    # 负数或超过数据库精度限制的值设为None
                    if activity_value < 0 or activity_value > 1e13:
                        activity_value = None
            except (ValueError, TypeError):
                pass

            # 标准化活性值
            activity_value_std, activity_units_std = standardize_activity_value(
                activity_value,
                clean_value(row.get('activity_units'))
            )

            record = {
                'natural_product_id': np_map[np_id],
                'target_id': target_map[target_id],
                'activity_type': clean_value(row.get('activity_type')),
                'activity_type_grouped': clean_value(row.get('activity_type_grouped')),
                'activity_relation': clean_value(row.get('activity_relation')),
                'activity_value': activity_value,
                'activity_units': clean_value(row.get('activity_units')),
                'activity_value_std': activity_value_std,
                'activity_units_std': activity_units_std,
                'assay_organism': clean_value(row.get('assay_organism')),
                'assay_tax_id': clean_value(row.get('assay_tax_id')),
                'assay_strain': clean_value(row.get('assay_strain')),
                'assay_tissue': clean_value(row.get('assay_tissue')),
                'assay_cell_type': clean_value(row.get('assay_cell_type')),
                'ref_id': clean_value(row.get('ref_id')),
                'ref_id_type': clean_value(row.get('ref_id_type')),
            }
            records.append(record)

        print(f"  - 已处理 {(chunk_num + 1) * chunk_size} 行...")

    print(f"  - NPASS活性记录: {len(records)}")
    print(f"  - 跳过(无匹配NP): {skipped_np}")
    print(f"  - 跳过(无匹配Target): {skipped_target}")

    return records


def process_cmaup_activities(np_map, target_map, existing_keys):
    """处理CMAUP活性数据"""
    print(f"[{datetime.now()}] 加载 CMAUP activities...")

    df = pd.read_csv(CMAUP_ACTIVITIES, sep='\t', dtype=str)
    print(f"  - 原始记录数: {len(df)}")

    records = []
    skipped_np = 0
    skipped_target = 0
    skipped_dup = 0

    for _, row in df.iterrows():
        np_id = clean_value(row.get('Ingredient_ID'))
        target_id = clean_value(row.get('Target_ID'))

        # 查找外键ID
        if np_id not in np_map:
            skipped_np += 1
            continue
        if target_id not in target_map:
            skipped_target += 1
            continue

        # 检查是否重复
        key = (np_map[np_id], target_map[target_id],
               clean_value(row.get('Activity_Type')),
               clean_value(row.get('Activity_Value')),
               clean_value(row.get('Reference_ID')))
        if key in existing_keys:
            skipped_dup += 1
            continue
        existing_keys.add(key)

        # 解析活性值（负数和超大值设为None）
        activity_value = None
        try:
            val = clean_value(row.get('Activity_Value'))
            if val:
                activity_value = float(val)
                if activity_value < 0 or activity_value > 1e13:
                    activity_value = None
        except (ValueError, TypeError):
            pass

        # 标准化活性值
        activity_value_std, activity_units_std = standardize_activity_value(
            activity_value,
            clean_value(row.get('Activity_Unit'))
        )

        record = {
            'natural_product_id': np_map[np_id],
            'target_id': target_map[target_id],
            'activity_type': clean_value(row.get('Activity_Type')),
            'activity_type_grouped': clean_value(row.get('Activity_Type')),  # CMAUP没有分组
            'activity_relation': clean_value(row.get('Activity_Relationship')),
            'activity_value': activity_value,
            'activity_units': clean_value(row.get('Activity_Unit')),
            'activity_value_std': activity_value_std,
            'activity_units_std': activity_units_std,
            'assay_organism': None,
            'assay_tax_id': None,
            'assay_strain': None,
            'assay_tissue': None,
            'assay_cell_type': None,
            'ref_id': clean_value(row.get('Reference_ID')),
            'ref_id_type': clean_value(row.get('Reference_ID_Type')),
        }
        records.append(record)

    print(f"  - CMAUP新增活性记录: {len(records)}")
    print(f"  - 跳过(无匹配NP): {skipped_np}")
    print(f"  - 跳过(无匹配Target): {skipped_target}")
    print(f"  - 跳过(重复): {skipped_dup}")

    return records


def insert_to_db(conn, records, batch_size=5000):
    """批量插入数据库"""
    cur = conn.cursor()

    # 插入SQL
    insert_sql = """
        INSERT INTO bioactivity (
            natural_product_id, target_id, activity_type, activity_type_grouped,
            activity_relation, activity_value, activity_units,
            activity_value_std, activity_units_std,
            assay_organism, assay_tax_id, assay_strain, assay_tissue, assay_cell_type,
            ref_id, ref_id_type
        ) VALUES %s
    """

    # 转换为元组列表
    values = [
        (
            r['natural_product_id'], r['target_id'], r['activity_type'], r['activity_type_grouped'],
            r['activity_relation'], r['activity_value'], r['activity_units'],
            r['activity_value_std'], r['activity_units_std'],
            r['assay_organism'], r['assay_tax_id'], r['assay_strain'], r['assay_tissue'], r['assay_cell_type'],
            r['ref_id'], r['ref_id_type']
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
        if inserted % 50000 == 0 or inserted == total:
            print(f"  - 进度: {inserted}/{total} ({100*inserted/total:.1f}%)")

    # 验证
    cur.execute("SELECT COUNT(*) FROM bioactivity")
    count = cur.fetchone()[0]
    print(f"[{datetime.now()}] 导入完成! 表中总记录数: {count}")

    cur.close()
    return count


def main():
    print("=" * 60)
    print("活性数据导入脚本")
    print("=" * 60)

    # 连接数据库
    print(f"[{datetime.now()}] 连接数据库...")
    conn = psycopg2.connect(**DB_CONFIG)

    # 加载ID映射
    np_map, target_map = load_id_mappings(conn)

    # 处理NPASS数据
    npass_records = process_npass_activities(np_map, target_map)

    # 构建去重键集合
    existing_keys = set()
    for r in npass_records:
        key = (r['natural_product_id'], r['target_id'],
               r['activity_type'], r['activity_value'], r['ref_id'])
        existing_keys.add(key)

    # 处理CMAUP数据
    cmaup_records = process_cmaup_activities(np_map, target_map, existing_keys)

    # 合并记录
    all_records = npass_records + cmaup_records
    print(f"[{datetime.now()}] 总活性记录数: {len(all_records)}")

    # 插入数据库
    count = insert_to_db(conn, all_records)

    conn.close()

    print("=" * 60)
    print(f"导入完成! 共导入 {count} 条活性记录")
    print("=" * 60)


if __name__ == '__main__':
    main()
