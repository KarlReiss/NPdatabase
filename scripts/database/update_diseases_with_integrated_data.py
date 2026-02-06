#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新diseases表 - 使用整合的疾病数据

功能：
1. 清空diseases表的现有数据
2. 从整合文件导入新数据
3. 删除不必要的字段（disease_id, description, symptoms, num_of_related_plants, num_of_related_targets）
4. 添加有价值的字段（disease_name_cmaup）
5. 优化表结构

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
DB_USER = os.environ.get('DB_USER', 'yfguo')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')

INTEGRATED_FILE = '/home/yfguo/NPdatabase/data/processed/integrated_disease_table.tsv'
BATCH_SIZE = 100


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


def backup_and_restructure_table(conn):
    """
    备份并重构表结构
    1. 删除不必要的字段
    2. 添加新字段
    """
    print("\n正在重构diseases表结构...")
    cursor = conn.cursor()

    try:
        # 1. 删除视图依赖（如果有）
        print("  - 检查视图依赖...")
        cursor.execute("""
            SELECT table_name
            FROM information_schema.views
            WHERE table_schema = 'public'
            AND table_name LIKE '%disease%';
        """)
        views = cursor.fetchall()
        if views:
            print(f"    发现相关视图: {[v[0] for v in views]}")

        # 2. 清空表
        print("  - 清空表数据...")
        cursor.execute("TRUNCATE TABLE diseases RESTART IDENTITY CASCADE;")
        conn.commit()

        # 3. 删除不必要的字段
        print("  - 删除不必要的字段...")
        fields_to_drop = [
            'disease_id',
            'description',
            'symptoms',
            'num_of_related_plants',
            'num_of_related_targets'
        ]

        for field in fields_to_drop:
            try:
                cursor.execute(f"ALTER TABLE diseases DROP COLUMN IF EXISTS {field};")
                print(f"    ✓ 删除 {field}")
            except Exception as e:
                print(f"    ⚠ 删除 {field} 失败: {e}")

        conn.commit()

        # 4. 添加新字段
        print("  - 添加新字段...")
        cursor.execute("""
            ALTER TABLE diseases
            ADD COLUMN IF NOT EXISTS disease_name_cmaup VARCHAR(500);
        """)
        cursor.execute("""
            COMMENT ON COLUMN diseases.disease_name_cmaup IS 'CMAUP数据库中的疾病名称';
        """)
        print("    ✓ 添加 disease_name_cmaup")

        conn.commit()

        # 5. 确保必要字段存在
        print("  - 确保必要字段存在...")
        cursor.execute("""
            ALTER TABLE diseases
            ADD COLUMN IF NOT EXISTS icd11_code VARCHAR(50);
        """)
        cursor.execute("""
            ALTER TABLE diseases
            ADD COLUMN IF NOT EXISTS disease_name VARCHAR(500);
        """)
        cursor.execute("""
            ALTER TABLE diseases
            ADD COLUMN IF NOT EXISTS disease_name_zh VARCHAR(500);
        """)
        cursor.execute("""
            ALTER TABLE diseases
            ADD COLUMN IF NOT EXISTS disease_category VARCHAR(200);
        """)

        conn.commit()

        print("  ✓ 表结构重构完成")

    except Exception as e:
        conn.rollback()
        print(f"  ✗ 表结构重构失败: {e}")
        raise
    finally:
        cursor.close()


def import_data(conn):
    """导入整合数据"""
    print(f"\n正在从整合文件导入数据...")
    print(f"  文件: {INTEGRATED_FILE}")

    cursor = conn.cursor()

    # 读取整合文件
    with open(INTEGRATED_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter='\t')

        # 构建INSERT语句
        insert_sql = """
            INSERT INTO diseases (
                icd11_code,
                disease_name,
                disease_name_zh,
                disease_name_cmaup,
                disease_category
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        batch = []
        total_count = 0
        success_count = 0
        error_count = 0

        for row_num, row in enumerate(reader, start=1):
            try:
                # 字段映射
                icd11_code = row.get('Code', '').strip()
                disease_name = row.get('TitleEN', '').strip()
                disease_name_zh = row.get('Title', '').strip()
                disease_name_cmaup = row.get('Disease_CMAUP', '').strip()
                disease_category = row.get('Disease_Category_CMAUP', '').strip()

                # 验证必填字段
                if not icd11_code or not disease_name:
                    print(f"  ⚠ 跳过行 {row_num}: 缺少必填字段")
                    error_count += 1
                    continue

                values = (
                    icd11_code,
                    disease_name,
                    disease_name_zh if disease_name_zh else None,
                    disease_name_cmaup if disease_name_cmaup else None,
                    disease_category if disease_category else None
                )

                batch.append(values)
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
        cursor.execute("SELECT COUNT(*) FROM diseases;")
        count = cursor.fetchone()[0]
        print(f"  - 总记录数: {count:,}")

        # 2. 字段完整性
        cursor.execute("""
            SELECT
                COUNT(*) FILTER (WHERE icd11_code IS NOT NULL) as icd11_count,
                COUNT(*) FILTER (WHERE disease_name IS NOT NULL) as name_count,
                COUNT(*) FILTER (WHERE disease_name_zh IS NOT NULL) as name_zh_count,
                COUNT(*) FILTER (WHERE disease_name_cmaup IS NOT NULL) as name_cmaup_count,
                COUNT(*) FILTER (WHERE disease_category IS NOT NULL) as category_count
            FROM diseases;
        """)
        row = cursor.fetchone()
        print(f"  - 有ICD-11编码: {row[0]:,} ({row[0]/count*100:.2f}%)")
        print(f"  - 有英文名称: {row[1]:,} ({row[1]/count*100:.2f}%)")
        print(f"  - 有中文名称: {row[2]:,} ({row[2]/count*100:.2f}%)")
        print(f"  - 有CMAUP名称: {row[3]:,} ({row[3]/count*100:.2f}%)")
        print(f"  - 有疾病分类: {row[4]:,} ({row[4]/count*100:.2f}%)")

        # 3. 疾病分类统计
        print("\n  疾病分类分布:")
        cursor.execute("""
            SELECT disease_category, COUNT(*) as count
            FROM diseases
            WHERE disease_category IS NOT NULL
            GROUP BY disease_category
            ORDER BY count DESC
            LIMIT 10;
        """)
        for row in cursor.fetchall():
            print(f"    {row[0]}: {row[1]:,}")

        # 4. 示例记录
        print("\n  示例记录（前3条）:")
        cursor.execute("""
            SELECT icd11_code, disease_name, disease_name_zh,
                   disease_name_cmaup, disease_category
            FROM diseases
            ORDER BY id
            LIMIT 3;
        """)

        for row in cursor.fetchall():
            print(f"\n    ICD-11: {row[0]}")
            print(f"    英文名: {row[1]}")
            print(f"    中文名: {row[2]}")
            print(f"    CMAUP名: {row[3]}")
            print(f"    分类: {row[4]}")

        # 5. 显示当前表结构
        print("\n  当前表结构:")
        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'diseases'
            ORDER BY ordinal_position;
        """)
        for col in cursor.fetchall():
            print(f"    - {col[0]:<30} {col[1]}")

        print("\n✓ 验证完成")

    except Exception as e:
        print(f"  ✗ 验证失败: {e}")
    finally:
        cursor.close()


def main():
    """主函数"""
    print("=" * 80)
    print("更新diseases表 - 使用整合的疾病数据")
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
        # 1. 重构表结构
        backup_and_restructure_table(conn)

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
