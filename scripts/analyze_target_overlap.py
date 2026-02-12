import pandas as pd

# 读取三个文件
cmaup = pd.read_csv('/home/yfguo/NPdatabase/data/CMAUP/CMAUPv2.0_download_Targets.txt', sep='\t')
npass = pd.read_csv('/home/yfguo/NPdatabase/data/NPASS/NPASS3.0_target.txt', sep='\t')
ttd = pd.read_csv('/home/yfguo/NPdatabase/data/TTD/TTD_target_basic_info.csv')

# 提取有效的 Uniprot ID
cmaup_uniprot = set(cmaup['Uniprot_ID'].dropna())
npass_valid = npass[npass['uniprot_id'] != 'n.a.']
npass_uniprot = set(npass_valid['uniprot_id'].dropna())
ttd_uniprot = set(ttd['UNIPROID'].dropna())

print('=== Uniprot ID 统计 ===')
print(f'CMAUP 有效 Uniprot ID: {len(cmaup_uniprot)}')
print(f'NPASS 有效 Uniprot ID: {len(npass_uniprot)}')
print(f'TTD 有效 Uniprot ID: {len(ttd_uniprot)}')

print('\n=== 重叠分析 ===')
cmaup_npass = cmaup_uniprot & npass_uniprot
cmaup_ttd = cmaup_uniprot & ttd_uniprot
npass_ttd = npass_uniprot & ttd_uniprot
all_three = cmaup_uniprot & npass_uniprot & ttd_uniprot

print(f'CMAUP ∩ NPASS: {len(cmaup_npass)}')
print(f'CMAUP ∩ TTD: {len(cmaup_ttd)}')
print(f'NPASS ∩ TTD: {len(npass_ttd)}')
print(f'三者都有: {len(all_three)}')

print('\n=== 唯一靶点 ===')
print(f'仅在 CMAUP: {len(cmaup_uniprot - npass_uniprot - ttd_uniprot)}')
print(f'仅在 NPASS: {len(npass_uniprot - cmaup_uniprot - ttd_uniprot)}')
print(f'仅在 TTD: {len(ttd_uniprot - cmaup_uniprot - npass_uniprot)}')

print('\n=== 合并后总数 ===')
all_uniprot = cmaup_uniprot | npass_uniprot | ttd_uniprot
print(f'总唯一 Uniprot ID: {len(all_uniprot)}')
