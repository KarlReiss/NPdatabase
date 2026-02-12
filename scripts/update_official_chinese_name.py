#!/usr/bin/env python3
"""
更新 bio_resources 表的 official_chinese_name 字段
从 TCMID prescription_herbs.csv 文件中通过拉丁名匹配获取正式中文名
"""

import psycopg2
import csv
from collections import defaultdict

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'npdb',
    'user': 'yfguo',
    'password': 'npdb2024'
}

# CSV 文件路径
CSV_FILE = '/home/yfguo/NPdatabase/data/TCMID/prescription_herbs.csv'

def main():
    # 连接数据库
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        # 1. 添加列（如果不存在）
        print("添加 official_chinese_name 列...")
        cur.execute("""
            ALTER TABLE bio_resources
            ADD COLUMN IF NOT EXISTS official_chinese_name VARCHAR(255);
        """)
        conn.commit()
        print("✓ 列添加成功")

        # 2. 读取 CSV 文件，建立拉丁名到中文名的映射
        print(f"\n读取 CSV 文件: {CSV_FILE}")
        latin_to_chinese = {}

        with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                latin_name = row['LatinName'].strip()
                chinese_name = row['ChineseName'].strip()

                # 如果同一个拉丁名有多个中文名，只保留第一个（最常见的）
                if latin_name and chinese_name and latin_name not in latin_to_chinese:
                    latin_to_chinese[latin_name] = chinese_name

        print(f"✓ 读取到 {len(latin_to_chinese)} 个拉丁名-中文名映射")

        # 3. 查询所有 bio_resources 的拉丁名
        print("\n查询 bio_resources 表...")
        cur.execute("""
            SELECT id, resource_id, latin_name
            FROM bio_resources
            WHERE latin_name IS NOT NULL AND latin_name != ''
        """)
        resources = cur.fetchall()
        print(f"✓ 找到 {len(resources)} 条有拉丁名的记录")

        # 4. 批量更新
        print("\n开始更新 official_chinese_name...")
        updated_count = 0
        matched_count = 0

        for resource_id, resource_code, latin_name in resources:
            # 尝试精确匹配
            official_name = latin_to_chinese.get(latin_name)

            if official_name:
                cur.execute("""
                    UPDATE bio_resources
                    SET official_chinese_name = %s
                    WHERE id = %s
                """, (official_name, resource_id))
                matched_count += 1
                updated_count += 1

                if updated_count % 1000 == 0:
                    print(f"  已更新 {updated_count} 条记录...")
                    conn.commit()

        conn.commit()
        print(f"\n✓ 更新完成！")
        print(f"  - 总记录数: {len(resources)}")
        print(f"  - 匹配成功: {matched_count}")
        print(f"  - 匹配率: {matched_count/len(resources)*100:.2f}%")

        # 5. 显示一些示例
        print("\n示例数据（前 10 条匹配成功的）:")
        cur.execute("""
            SELECT resource_id, latin_name, chinese_name, official_chinese_name
            FROM bio_resources
            WHERE official_chinese_name IS NOT NULL
            LIMIT 10
        """)

        print(f"{'资源ID':<12} {'拉丁名':<30} {'别名':<20} {'正式名称':<15}")
        print("-" * 80)
        for row in cur.fetchall():
            resource_id, latin, chinese, official = row
            chinese_display = (chinese[:17] + '...') if chinese and len(chinese) > 20 else (chinese or '—')
            print(f"{resource_id:<12} {latin:<30} {chinese_display:<20} {official:<15}")

    except Exception as e:
        print(f"\n✗ 错误: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    main()
