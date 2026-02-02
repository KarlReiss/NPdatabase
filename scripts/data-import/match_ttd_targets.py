#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTD 靶点匹配到现有靶点
======================
功能: 将 TTD_target_basic_info.csv 中的靶点匹配到 targets 表
匹配策略:
  1. 优先级1: UniProt ID精确匹配
  2. 优先级2: 靶点名称精确匹配
  3. 优先级3: 基因名匹配
  4. 优先级4: 记录为未匹配，需要创建新记录

输出:
  - matched_targets.json: 成功匹配的靶点
  - unmatched_targets.json: 未匹配的靶点
  - target_matching_report.txt: 匹配报告
"""

import csv
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from collections import defaultdict
import os
import re

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'npdb',
    'user': os.environ.get('DB_USER', 'yfguo'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'host': 'localhost',
    'port': 5432
}

# 文件路径
DATA_DIR = '/home/yfguo/NPdatabase/data/TTD'
OUTPUT_DIR = '/home/yfguo/NPdatabase/scripts/data-import/output'
TTD_FILE = os.path.join(DATA_DIR, 'TTD_target_basic_info.csv')
MATCHED_OUTPUT = os.path.join(OUTPUT_DIR, 'matched_targets.json')
UNMATCHED_OUTPUT = os.path.join(OUTPUT_DIR, 'unmatched_targets.json')
REPORT_OUTPUT = os.path.join(OUTPUT_DIR, 'target_matching_report.txt')

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)


def connect_db():
    """连接数据库"""
    return psycopg2.connect(**DB_CONFIG)


def load_targets(conn):
    """加载所有靶点数据到内存"""
    print("加载现有靶点数据...")
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, target_id, target_name, uniprot_id, gene_name
            FROM targets
        """)
        targets = cur.fetchall()

    print(f"已加载 {len(targets)} 条靶点记录")
    return targets


def normalize_uniprot_id(uniprot_id):
    """标准化UniProt ID（去除空格，转大写）"""
    if not uniprot_id:
        return ""
    # 提取UniProt ID（格式如 FGFR1_HUMAN）
    uniprot_id = uniprot_id.strip().upper()
    return uniprot_id


def normalize_target_name(name):
    """标准化靶点名称（转小写，去除多余空格和括号内容）"""
    if not name:
        return ""
    # 去除括号及其内容
    name = re.sub(r'\([^)]*\)', '', name)
    # 转小写，去除多余空格
    return ' '.join(name.lower().strip().split())


def normalize_gene_name(gene_name):
    """标准化基因名（转大写，去除空格）"""
    if not gene_name:
        return ""
    return gene_name.strip().upper()


def match_target_by_uniprot(ttd_target, targets):
    """
    优先级1: UniProt ID精确匹配
    """
    ttd_uniprot = normalize_uniprot_id(ttd_target['UNIPROID'])
    if not ttd_uniprot:
        return None, None

    for target in targets:
        target_uniprot = normalize_uniprot_id(target['uniprot_id'])
        if target_uniprot == ttd_uniprot:
            return target['id'], 'exact_uniprot'

    return None, None


def match_target_by_name(ttd_target, targets):
    """
    优先级2: 靶点名称精确匹配
    """
    ttd_name = normalize_target_name(ttd_target['TARGNAME'])
    if not ttd_name:
        return None, None

    for target in targets:
        target_name = normalize_target_name(target['target_name'])
        if target_name == ttd_name:
            return target['id'], 'exact_name'

    return None, None


def match_target_by_gene(ttd_target, targets):
    """
    优先级3: 基因名匹配
    """
    ttd_gene = normalize_gene_name(ttd_target['GENENAME'])
    if not ttd_gene:
        return None, None

    for target in targets:
        target_gene = normalize_gene_name(target['gene_name'])
        if target_gene and target_gene == ttd_gene:
            return target['id'], 'exact_gene'

    return None, None


def match_targets(ttd_data, targets):
    """
    匹配所有TTD靶点
    """
    matched = []
    unmatched = []
    match_stats = defaultdict(int)

    total = len(ttd_data)
    print(f"\n开始匹配 {total} 条TTD靶点记录...")

    for idx, ttd_target in enumerate(ttd_data, 1):
        if idx % 100 == 0:
            print(f"进度: {idx}/{total}")

        result = {
            'ttd_id': ttd_target['TARGETID'],
            'ttd_former_id': ttd_target['FORMERID'],
            'uniprot_id': ttd_target['UNIPROID'],
            'target_name': ttd_target['TARGNAME'],
            'gene_name': ttd_target['GENENAME'],
            'target_type': ttd_target['TARGTYPE'],
            'synonyms': ttd_target['SYNONYMS'],
            'function': ttd_target['FUNCTION'],
            'pdb_structure': ttd_target['PDBSTRUC'],
            'bioclass': ttd_target['BIOCLASS'],
            'ec_number': ttd_target['ECNUMBER'],
            'sequence': ttd_target['SEQUENCE']
        }

        # 尝试匹配
        target_id = None
        match_method = None

        # 优先级1: UniProt ID精确匹配
        target_id, match_method = match_target_by_uniprot(ttd_target, targets)

        # 优先级2: 靶点名称精确匹配
        if not target_id:
            target_id, match_method = match_target_by_name(ttd_target, targets)

        # 优先级3: 基因名匹配
        if not target_id:
            target_id, match_method = match_target_by_gene(ttd_target, targets)

        # 记录结果
        if target_id:
            # 成功匹配
            result['target_id'] = target_id
            result['match_method'] = match_method
            if match_method == 'exact_uniprot':
                result['confidence'] = 'high'
            elif match_method == 'exact_name':
                result['confidence'] = 'high'
            else:
                result['confidence'] = 'medium'
            matched.append(result)
            match_stats[match_method] += 1
        else:
            # 未匹配
            result['match_method'] = 'no_match'
            result['confidence'] = 'none'
            unmatched.append(result)
            match_stats['no_match'] += 1

    return matched, unmatched, match_stats


def generate_report(matched, unmatched, match_stats, total_ttd):
    """
    生成匹配报告
    """
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("TTD 靶点匹配报告")
    report_lines.append("=" * 80)
    report_lines.append("")

    # 总体统计
    report_lines.append("## 总体统计")
    report_lines.append(f"总TTD靶点记录数: {total_ttd}")
    report_lines.append(f"成功匹配数: {len(matched)}")
    report_lines.append(f"未匹配数: {len(unmatched)}")
    report_lines.append(f"匹配率: {len(matched)/total_ttd*100:.2f}%")
    report_lines.append("")

    # 匹配方法统计
    report_lines.append("## 匹配方法统计")
    report_lines.append(f"UniProt ID精确匹配: {match_stats.get('exact_uniprot', 0)}")
    report_lines.append(f"靶点名称精确匹配: {match_stats.get('exact_name', 0)}")
    report_lines.append(f"基因名精确匹配: {match_stats.get('exact_gene', 0)}")
    report_lines.append(f"完全未匹配: {match_stats.get('no_match', 0)}")
    report_lines.append("")

    # 未匹配靶点示例
    if unmatched:
        report_lines.append("## 未匹配靶点示例（前20条）")
        report_lines.append("-" * 80)
        for target in unmatched[:20]:
            report_lines.append(f"TTD ID: {target['ttd_id']}")
            report_lines.append(f"  UniProt ID: {target['uniprot_id']}")
            report_lines.append(f"  靶点名称: {target['target_name']}")
            report_lines.append(f"  基因名: {target['gene_name']}")
            report_lines.append(f"  靶点类型: {target['target_type']}")
            report_lines.append("")

    # 统计唯一靶点
    unique_matched = set(t['ttd_id'] for t in matched)
    unique_unmatched = set(t['ttd_id'] for t in unmatched)

    report_lines.append("## 唯一靶点统计")
    report_lines.append(f"唯一匹配靶点数: {len(unique_matched)}")
    report_lines.append(f"唯一未匹配靶点数: {len(unique_unmatched)}")
    report_lines.append("")

    report_lines.append("=" * 80)

    return '\n'.join(report_lines)


def main():
    print("TTD 靶点匹配程序")
    print("=" * 80)

    # 读取TTD靶点数据
    print(f"\n读取TTD靶点数据: {TTD_FILE}")
    ttd_data = []
    with open(TTD_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        ttd_data = list(reader)

    print(f"已读取 {len(ttd_data)} 条TTD靶点记录")

    # 连接数据库并加载现有靶点
    conn = connect_db()
    try:
        targets = load_targets(conn)

        # 执行匹配
        matched, unmatched, match_stats = match_targets(ttd_data, targets)

        # 保存结果
        print(f"\n保存匹配结果...")
        with open(MATCHED_OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(matched, f, ensure_ascii=False, indent=2)
        print(f"已保存匹配结果: {MATCHED_OUTPUT}")

        with open(UNMATCHED_OUTPUT, 'w', encoding='utf-8') as f:
            json.dump(unmatched, f, ensure_ascii=False, indent=2)
        print(f"已保存未匹配结果: {UNMATCHED_OUTPUT}")

        # 生成报告
        report = generate_report(matched, unmatched, match_stats, len(ttd_data))
        with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"已保存匹配报告: {REPORT_OUTPUT}")

        # 打印报告
        print("\n" + report)

    finally:
        conn.close()

    print("\n匹配完成！")


if __name__ == '__main__':
    main()
