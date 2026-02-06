#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NPASS 3.0 与 CMAUP v2.0 天然产物数据整合脚本

功能：
1. 加载NPASS和CMAUP数据
2. CMAUP去重处理（去除7个重复InChIKey）
3. 四级匹配策略：np_id > InChIKey > PubChem ID > ChEMBL ID
4. 字段合并与补全
5. 生成整合文件和报告

作者：Claude Code
日期：2026-02-05
"""

import pandas as pd
import os
from datetime import datetime
from collections import defaultdict

# 文件路径配置
NPASS_FILE = '/home/yfguo/NPdatabase/data/NPASS/NPASS3.0_naturalproducts_generalinfo.txt'
CMAUP_FILE = '/home/yfguo/NPdatabase/data/CMAUP/CMAUPv2.0_download_Ingredients_All.txt'
OUTPUT_DIR = '/home/yfguo/NPdatabase/data/processed'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'natural_products_integrated.txt')
REPORT_FILE = os.path.join(OUTPUT_DIR, 'npass_cmaup_integration_report.txt')

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_npass_data():
    """加载NPASS 3.0数据"""
    print("正在加载NPASS 3.0数据...")
    df = pd.read_csv(NPASS_FILE, sep='\t', dtype=str, na_filter=False)
    print(f"  - 加载了 {len(df)} 条记录")
    print(f"  - 字段: {list(df.columns)}")
    return df


def load_cmaup_data():
    """加载CMAUP v2.0数据"""
    print("\n正在加载CMAUP v2.0数据...")
    df = pd.read_csv(CMAUP_FILE, sep='\t', dtype=str, na_filter=False)
    print(f"  - 加载了 {len(df)} 条记录")
    print(f"  - 字段: {list(df.columns)}")
    return df


def deduplicate_cmaup(df):
    """
    CMAUP去重处理
    根据InChIKey去重，保留第一条记录
    """
    print("\n正在对CMAUP数据去重...")
    original_count = len(df)

    # 标准化InChIKey（转大写，去除空格）
    df['InChIKey_normalized'] = df['InChIKey'].str.upper().str.strip()

    # 找出重复的InChIKey
    duplicates = df[df.duplicated(subset=['InChIKey_normalized'], keep=False)]
    if len(duplicates) > 0:
        print(f"  - 发现 {len(duplicates)} 条重复记录")
        duplicate_keys = duplicates['InChIKey_normalized'].unique()
        print(f"  - 涉及 {len(duplicate_keys)} 个不同的InChIKey:")
        for key in duplicate_keys:
            count = len(duplicates[duplicates['InChIKey_normalized'] == key])
            print(f"    * {key}: {count}条")

    # 去重，保留第一条
    df_dedup = df.drop_duplicates(subset=['InChIKey_normalized'], keep='first')
    removed_count = original_count - len(df_dedup)

    print(f"  - 去重前: {original_count} 条")
    print(f"  - 去重后: {len(df_dedup)} 条")
    print(f"  - 删除了: {removed_count} 条重复记录")

    return df_dedup


def build_cmaup_indexes(df):
    """
    构建CMAUP的多级索引
    返回：{
        'np_id': {np_id: row_dict},
        'inchikey': {inchikey: row_dict},
        'pubchem': {pubchem_id: row_dict},
        'chembl': {chembl_id: row_dict}
    }
    """
    print("\n正在构建CMAUP索引...")
    indexes = {
        'np_id': {},
        'inchikey': {},
        'pubchem': {},
        'chembl': {}
    }

    for idx, row in df.iterrows():
        row_dict = row.to_dict()

        # np_id索引
        if row['np_id'] and row['np_id'] != 'n.a.':
            indexes['np_id'][row['np_id']] = row_dict

        # InChIKey索引（标准化）
        if row['InChIKey_normalized'] and row['InChIKey_normalized'] != 'N.A.':
            indexes['inchikey'][row['InChIKey_normalized']] = row_dict

        # PubChem ID索引
        if row['pubchem_cid'] and row['pubchem_cid'] != 'n.a.':
            indexes['pubchem'][row['pubchem_cid']] = row_dict

        # ChEMBL ID索引
        if row['chembl_id'] and row['chembl_id'] != 'n.a.':
            indexes['chembl'][row['chembl_id']] = row_dict

    print(f"  - np_id索引: {len(indexes['np_id'])} 条")
    print(f"  - InChIKey索引: {len(indexes['inchikey'])} 条")
    print(f"  - PubChem ID索引: {len(indexes['pubchem'])} 条")
    print(f"  - ChEMBL ID索引: {len(indexes['chembl'])} 条")

    return indexes


def merge_fields(npass_row, cmaup_row, match_method):
    """
    合并NPASS和CMAUP的字段

    参数：
        npass_row: NPASS记录（字典）
        cmaup_row: CMAUP记录（字典或None）
        match_method: 匹配方法（'np_id', 'inchikey', 'pubchem', 'chembl', 'no_match'）

    返回：
        merged: 合并后的记录（字典）
    """
    merged = {}

    # 标识字段
    merged['np_id'] = npass_row['np_id']
    merged['cmaup_np_id'] = cmaup_row['np_id'] if cmaup_row else ''
    merged['inchikey'] = cmaup_row['InChIKey'] if cmaup_row else npass_row['inchikey']

    # 名称字段（优先NPASS）
    merged['pref_name'] = npass_row['pref_name']
    merged['iupac_name'] = npass_row['iupac_name'] if npass_row['iupac_name'] != 'n.a.' else (
        cmaup_row['iupac_name'] if cmaup_row and cmaup_row['iupac_name'] != 'n.a.' else 'n.a.'
    )
    merged['name_initial'] = npass_row['name_initial']

    # 外部ID（优先非空）
    merged['chembl_id'] = npass_row['chembl_id'] if npass_row['chembl_id'] != 'n.a.' else (
        cmaup_row['chembl_id'] if cmaup_row and cmaup_row['chembl_id'] != 'n.a.' else 'n.a.'
    )
    merged['pubchem_id'] = npass_row['pubchem_id'] if npass_row['pubchem_id'] != 'n.a.' else (
        cmaup_row['pubchem_cid'] if cmaup_row and cmaup_row['pubchem_cid'] != 'n.a.' else 'n.a.'
    )

    # 理化性质（来自CMAUP）
    if cmaup_row:
        merged['molecular_weight'] = cmaup_row['MW']
        merged['log_s'] = cmaup_row['LogS']
        merged['log_d'] = cmaup_row['LogD']
        merged['log_p'] = cmaup_row['LogP']
        merged['h_bond_acceptors'] = cmaup_row['nHA']
        merged['h_bond_donors'] = cmaup_row['nHD']
        merged['tpsa'] = cmaup_row['TPSA']
        merged['rotatable_bonds'] = cmaup_row['nRot']
        merged['ring_count'] = cmaup_row['nRing']
        merged['inchi'] = cmaup_row['InChI']
        merged['smiles'] = cmaup_row['SMILES']
    else:
        # NPASS独有记录，理化性质为空
        merged['molecular_weight'] = ''
        merged['log_s'] = ''
        merged['log_d'] = ''
        merged['log_p'] = ''
        merged['h_bond_acceptors'] = ''
        merged['h_bond_donors'] = ''
        merged['tpsa'] = ''
        merged['rotatable_bonds'] = ''
        merged['ring_count'] = ''
        merged['inchi'] = ''
        merged['smiles'] = ''

    # 生物学信息（来自NPASS）
    merged['num_of_organism'] = npass_row['num_of_organism']
    merged['num_of_target'] = npass_row['num_of_target']
    merged['num_of_activity'] = npass_row['num_of_activity']
    merged['gene_cluster'] = npass_row['gene_cluster']
    merged['if_quantity'] = npass_row['ifQuantity']

    # 数据来源标记
    if cmaup_row:
        merged['data_source'] = 'Both'
        merged['match_method'] = match_method
    else:
        merged['data_source'] = 'NPASS_only'
        merged['match_method'] = 'no_match'

    return merged


def integrate_data(npass_df, cmaup_df, cmaup_indexes):
    """
    执行数据整合

    参数：
        npass_df: NPASS数据框
        cmaup_df: CMAUP数据框（已去重）
        cmaup_indexes: CMAUP索引字典

    返回：
        integrated_records: 整合后的记录列表
        match_stats: 匹配统计字典
    """
    print("\n正在执行数据整合...")
    integrated_records = []
    match_stats = {
        'np_id': 0,
        'inchikey': 0,
        'pubchem': 0,
        'chembl': 0,
        'no_match': 0
    }
    matched_cmaup_ids = set()  # 记录已匹配的CMAUP记录

    # 遍历NPASS记录，执行四级匹配
    for idx, npass_row in npass_df.iterrows():
        if (idx + 1) % 10000 == 0:
            print(f"  - 已处理 {idx + 1}/{len(npass_df)} 条NPASS记录...")

        npass_dict = npass_row.to_dict()
        cmaup_match = None
        match_method = None

        # 标准化NPASS的InChIKey
        npass_inchikey_normalized = npass_row['inchikey'].upper().strip() if npass_row['inchikey'] else ''

        # 优先级1: np_id匹配
        if npass_row['np_id'] in cmaup_indexes['np_id']:
            cmaup_match = cmaup_indexes['np_id'][npass_row['np_id']]
            match_method = 'np_id'
            match_stats['np_id'] += 1
            matched_cmaup_ids.add(cmaup_match['np_id'])

        # 优先级2: InChIKey匹配
        elif npass_inchikey_normalized and npass_inchikey_normalized != 'N.A.' and npass_inchikey_normalized in cmaup_indexes['inchikey']:
            cmaup_match = cmaup_indexes['inchikey'][npass_inchikey_normalized]
            match_method = 'inchikey'
            match_stats['inchikey'] += 1
            matched_cmaup_ids.add(cmaup_match['np_id'])

        # 优先级3: PubChem ID匹配
        elif npass_row['pubchem_id'] != 'n.a.' and npass_row['pubchem_id'] in cmaup_indexes['pubchem']:
            cmaup_match = cmaup_indexes['pubchem'][npass_row['pubchem_id']]
            match_method = 'pubchem'
            match_stats['pubchem'] += 1
            matched_cmaup_ids.add(cmaup_match['np_id'])

        # 优先级4: ChEMBL ID匹配
        elif npass_row['chembl_id'] != 'n.a.' and npass_row['chembl_id'] in cmaup_indexes['chembl']:
            cmaup_match = cmaup_indexes['chembl'][npass_row['chembl_id']]
            match_method = 'chembl'
            match_stats['chembl'] += 1
            matched_cmaup_ids.add(cmaup_match['np_id'])

        else:
            match_stats['no_match'] += 1

        # 合并字段
        merged_record = merge_fields(npass_dict, cmaup_match, match_method)
        integrated_records.append(merged_record)

    print(f"  - NPASS记录处理完成: {len(integrated_records)} 条")

    # 添加CMAUP独有记录
    print("\n正在添加CMAUP独有记录...")
    cmaup_only_count = 0
    for idx, cmaup_row in cmaup_df.iterrows():
        if cmaup_row['np_id'] not in matched_cmaup_ids:
            cmaup_dict = cmaup_row.to_dict()
            # 创建CMAUP独有记录
            cmaup_only_record = {
                'np_id': cmaup_dict['np_id'],
                'cmaup_np_id': cmaup_dict['np_id'],
                'inchikey': cmaup_dict['InChIKey'],
                'pref_name': cmaup_dict['pref_name'],
                'iupac_name': cmaup_dict['iupac_name'],
                'name_initial': '',
                'chembl_id': cmaup_dict['chembl_id'],
                'pubchem_id': cmaup_dict['pubchem_cid'],
                'molecular_weight': cmaup_dict['MW'],
                'log_s': cmaup_dict['LogS'],
                'log_d': cmaup_dict['LogD'],
                'log_p': cmaup_dict['LogP'],
                'h_bond_acceptors': cmaup_dict['nHA'],
                'h_bond_donors': cmaup_dict['nHD'],
                'tpsa': cmaup_dict['TPSA'],
                'rotatable_bonds': cmaup_dict['nRot'],
                'ring_count': cmaup_dict['nRing'],
                'inchi': cmaup_dict['InChI'],
                'smiles': cmaup_dict['SMILES'],
                'num_of_organism': '',
                'num_of_target': '',
                'num_of_activity': '',
                'gene_cluster': '',
                'if_quantity': '',
                'data_source': 'CMAUP_only',
                'match_method': 'cmaup_only'
            }
            integrated_records.append(cmaup_only_record)
            cmaup_only_count += 1

    print(f"  - 添加了 {cmaup_only_count} 条CMAUP独有记录")
    print(f"  - 整合后总记录数: {len(integrated_records)} 条")

    return integrated_records, match_stats


def generate_report(npass_count, cmaup_original_count, cmaup_dedup_count,
                   integrated_count, match_stats, integrated_df):
    """
    生成整合报告

    参数：
        npass_count: NPASS原始记录数
        cmaup_original_count: CMAUP原始记录数
        cmaup_dedup_count: CMAUP去重后记录数
        integrated_count: 整合后总记录数
        match_stats: 匹配统计字典
        integrated_df: 整合后的数据框
    """
    print("\n正在生成整合报告...")

    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("NPASS 3.0 与 CMAUP v2.0 数据整合报告")
    report_lines.append("=" * 80)
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # 1. 数据规模统计
    report_lines.append("1. 数据规模统计")
    report_lines.append("-" * 80)
    report_lines.append(f"   NPASS原始记录数:        {npass_count:>10,}")
    report_lines.append(f"   CMAUP原始记录数:        {cmaup_original_count:>10,}")
    report_lines.append(f"   CMAUP去重后记录数:      {cmaup_dedup_count:>10,}")
    report_lines.append(f"   整合后总记录数:         {integrated_count:>10,}")
    report_lines.append("")

    # 2. 匹配统计
    total_matched = match_stats['np_id'] + match_stats['inchikey'] + match_stats['pubchem'] + match_stats['chembl']
    npass_only = match_stats['no_match']
    cmaup_only = integrated_count - npass_count

    report_lines.append("2. 匹配统计")
    report_lines.append("-" * 80)
    report_lines.append(f"   np_id匹配:              {match_stats['np_id']:>10,} ({match_stats['np_id']/npass_count*100:>6.2f}%)")
    report_lines.append(f"   InChIKey匹配:           {match_stats['inchikey']:>10,} ({match_stats['inchikey']/npass_count*100:>6.2f}%)")
    report_lines.append(f"   PubChem ID匹配:         {match_stats['pubchem']:>10,} ({match_stats['pubchem']/npass_count*100:>6.2f}%)")
    report_lines.append(f"   ChEMBL ID匹配:          {match_stats['chembl']:>10,} ({match_stats['chembl']/npass_count*100:>6.2f}%)")
    report_lines.append(f"   总匹配数:               {total_matched:>10,} ({total_matched/npass_count*100:>6.2f}%)")
    report_lines.append(f"   NPASS独有:              {npass_only:>10,} ({npass_only/npass_count*100:>6.2f}%)")
    report_lines.append(f"   CMAUP独有:              {cmaup_only:>10,} ({cmaup_only/integrated_count*100:>6.2f}%)")
    report_lines.append("")

    # 3. 数据补全统计
    report_lines.append("3. 数据补全统计")
    report_lines.append("-" * 80)

    # 统计补充理化性质的记录数（来自CMAUP的NPASS记录）
    enriched_with_properties = len(integrated_df[
        (integrated_df['data_source'] == 'Both') &
        (integrated_df['molecular_weight'] != '')
    ])
    report_lines.append(f"   补充理化性质的记录数:   {enriched_with_properties:>10,} (NPASS记录匹配到CMAUP)")

    # 统计补充生物学信息的记录数（来自NPASS的CMAUP记录）
    enriched_with_bio = len(integrated_df[
        (integrated_df['data_source'] == 'Both') &
        (integrated_df['num_of_organism'] != '')
    ])
    report_lines.append(f"   补充生物学信息的记录数: {enriched_with_bio:>10,} (CMAUP记录匹配到NPASS)")

    # 统计补充外部ID的记录数
    enriched_pubchem = len(integrated_df[
        (integrated_df['data_source'] == 'Both') &
        (integrated_df['pubchem_id'] != 'n.a.')
    ])
    enriched_chembl = len(integrated_df[
        (integrated_df['data_source'] == 'Both') &
        (integrated_df['chembl_id'] != 'n.a.')
    ])
    report_lines.append(f"   补充PubChem ID的记录数: {enriched_pubchem:>10,}")
    report_lines.append(f"   补充ChEMBL ID的记录数:  {enriched_chembl:>10,}")
    report_lines.append("")

    # 4. 数据质量统计
    report_lines.append("4. 数据质量统计")
    report_lines.append("-" * 80)

    # InChIKey覆盖率
    inchikey_coverage = len(integrated_df[integrated_df['inchikey'] != '']) / integrated_count * 100
    report_lines.append(f"   InChIKey覆盖率:         {inchikey_coverage:>6.2f}%")

    # SMILES覆盖率
    smiles_coverage = len(integrated_df[integrated_df['smiles'] != '']) / integrated_count * 100
    report_lines.append(f"   SMILES覆盖率:           {smiles_coverage:>6.2f}%")

    # 分子量覆盖率
    mw_coverage = len(integrated_df[integrated_df['molecular_weight'] != '']) / integrated_count * 100
    report_lines.append(f"   分子量覆盖率:           {mw_coverage:>6.2f}%")

    # PubChem ID覆盖率
    pubchem_coverage = len(integrated_df[integrated_df['pubchem_id'] != 'n.a.']) / integrated_count * 100
    report_lines.append(f"   PubChem ID覆盖率:       {pubchem_coverage:>6.2f}%")

    # ChEMBL ID覆盖率
    chembl_coverage = len(integrated_df[integrated_df['chembl_id'] != 'n.a.']) / integrated_count * 100
    report_lines.append(f"   ChEMBL ID覆盖率:        {chembl_coverage:>6.2f}%")
    report_lines.append("")

    # 5. 数据来源分布
    report_lines.append("5. 数据来源分布")
    report_lines.append("-" * 80)
    source_counts = integrated_df['data_source'].value_counts()
    for source, count in source_counts.items():
        report_lines.append(f"   {source:<20} {count:>10,} ({count/integrated_count*100:>6.2f}%)")
    report_lines.append("")

    report_lines.append("=" * 80)
    report_lines.append("整合完成！")
    report_lines.append("=" * 80)

    # 写入报告文件
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"  - 报告已保存到: {REPORT_FILE}")

    # 同时打印到控制台
    print("\n" + '\n'.join(report_lines))


def main():
    """主函数"""
    print("=" * 80)
    print("NPASS 3.0 与 CMAUP v2.0 天然产物数据整合")
    print("=" * 80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    # 1. 加载数据
    npass_df = load_npass_data()
    cmaup_df = load_cmaup_data()

    npass_count = len(npass_df)
    cmaup_original_count = len(cmaup_df)

    # 2. CMAUP去重
    cmaup_df = deduplicate_cmaup(cmaup_df)
    cmaup_dedup_count = len(cmaup_df)

    # 3. 构建CMAUP索引
    cmaup_indexes = build_cmaup_indexes(cmaup_df)

    # 4. 执行数据整合
    integrated_records, match_stats = integrate_data(npass_df, cmaup_df, cmaup_indexes)

    # 5. 转换为DataFrame
    print("\n正在生成输出文件...")
    integrated_df = pd.DataFrame(integrated_records)

    # 定义输出字段顺序
    output_columns = [
        'np_id', 'cmaup_np_id', 'inchikey',
        'pref_name', 'iupac_name', 'name_initial',
        'chembl_id', 'pubchem_id',
        'molecular_weight', 'log_s', 'log_d', 'log_p',
        'h_bond_acceptors', 'h_bond_donors', 'tpsa',
        'rotatable_bonds', 'ring_count',
        'inchi', 'smiles',
        'num_of_organism', 'num_of_target', 'num_of_activity',
        'gene_cluster', 'if_quantity',
        'data_source', 'match_method'
    ]

    integrated_df = integrated_df[output_columns]

    # 6. 保存整合文件
    integrated_df.to_csv(OUTPUT_FILE, sep='\t', index=False, encoding='utf-8')
    print(f"  - 整合文件已保存到: {OUTPUT_FILE}")
    print(f"  - 文件大小: {os.path.getsize(OUTPUT_FILE) / 1024 / 1024:.2f} MB")

    # 7. 生成报告
    generate_report(
        npass_count, cmaup_original_count, cmaup_dedup_count,
        len(integrated_df), match_stats, integrated_df
    )

    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == '__main__':
    main()

