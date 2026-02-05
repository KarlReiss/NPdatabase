# CMAUP 与 NPASS 物种数据整合文档

## 📋 整合概述

**整合日期**: 2026-02-05
**整合目标**: 将 CMAUP 植物数据与 NPASS 物种数据整合为统一的生物资源数据集

## 📊 数据源信息

### CMAUP 数据源
- **文件**: `data/CMAUP/CMAUPv2.0_download_Plants.txt`
- **记录数**: 7,865 条
- **数据类型**: 植物 (Plants)
- **字段**: Plant_ID, Plant_Name, Species_Tax_ID, Species_Name, Genus_Tax_ID, Genus_Name, Family_Tax_ID, Family_Name

### NPASS 数据源
- **文件**: `data/NPASS/NPASS3.0_species_info.txt`
- **记录数**: 48,940 条
- **数据类型**: 所有生物类型 (植物、动物、微生物等)
- **字段**: 23个字段，包括完整的分类学信息、统计信息、标记信息

## 🎯 匹配策略

### 匹配优先级

1. **优先级1: ID精确匹配**
   - CMAUP `Plant_ID` = NPASS `org_id`
   - 匹配数: 7,828 (99.53%)
   - 置信度: high

2. **优先级2: 拉丁名匹配**
   - CMAUP `Species_Name` = NPASS `species_name`
   - 标准化处理: 转小写、去除多余空格
   - 匹配数: 0
   - 置信度: high

3. **优先级3: 种ID匹配**
   - CMAUP `Species_Tax_ID` = NPASS `species_tax_id`
   - 匹配数: 0
   - 置信度: high

4. **优先级4: 属科组合匹配**
   - CMAUP `Genus_Name` + `Family_Name` = NPASS `genus_name` + `family_name`
   - 匹配数: 37 (0.47%)
   - 置信度: low (因为可能有多个匹配)

5. **优先级5: 属ID匹配**
   - CMAUP `Genus_Tax_ID` = NPASS `genus_tax_id`
   - 匹配数: 0
   - 置信度: medium

### 数据标准化

- **NA值处理**: 统一将 'NA', 'n.a.', 'N/A', 空字符串 转换为 NULL
- **拉丁名标准化**: 转小写、去除多余空格
- **ID标准化**: 去除变种后缀 (如 NPO5649.1 → NPO5649)

## 📈 整合结果

### 总体统计

| 指标 | 数值 |
|------|------|
| CMAUP总记录数 | 7,865 |
| NPASS总记录数 | 48,940 |
| **整合后总记录数** | **49,054** |

### 数据来源分布

| 数据来源 | 记录数 | 百分比 |
|---------|--------|--------|
| 匹配成功 (BOTH) | 7,865 | 16.03% |
| CMAUP独有 | 0 | 0.00% |
| NPASS独有 | 41,189 | 83.97% |

### 匹配率

- **CMAUP匹配率**: 100.00% (7,865/7,865)
- 所有CMAUP植物都成功匹配到NPASS记录

### 匹配方法统计

| 匹配方法 | 记录数 | 百分比 |
|---------|--------|--------|
| id_exact | 7,828 | 99.53% |
| genus_family_multiple | 37 | 0.47% |

### 匹配置信度统计

| 置信度 | 记录数 | 百分比 |
|--------|--------|--------|
| high | 7,828 | 99.53% |
| low | 37 | 0.47% |

## 📁 输出文件

### 1. 整合数据文件
- **路径**: `data/processed/bio_resources_integrated.txt`
- **格式**: TSV (Tab-Separated Values)
- **记录数**: 49,054 条 (含表头)
- **字段数**: 25 个字段

### 2. 整合报告
- **路径**: `scripts/data-import/output/integration_report.txt`
- **内容**: 匹配统计、数据来源分布、匹配方法统计

### 3. 未匹配CMAUP记录
- **路径**: `scripts/data-import/output/unmatched_cmaup.txt`
- **记录数**: 0 (所有CMAUP记录都成功匹配)

## 🗂️ 整合后字段结构

### 核心标识字段
- `org_id` - 生物ID (来自NPASS或CMAUP)
- `cmaup_id` - CMAUP Plant_ID (如果有)

### 命名字段
- `org_name` - 生物名称 (优先NPASS)
- `cmaup_plant_name` - CMAUP植物名称 (如果有)
- `org_name_initial` - 首字母

### 分类学字段
- `org_tax_level` - 分类级别
- `org_tax_id` - 生物Taxonomy ID
- `subspecies_tax_id`, `subspecies_name` - 亚种信息
- `species_tax_id`, `species_name` - 种信息
- `genus_tax_id`, `genus_name` - 属信息
- `family_tax_id`, `family_name` - 科信息
- `kingdom_tax_id`, `kingdom_name` - 界信息
- `superkingdom_tax_id`, `superkingdom_name` - 超界信息

### 统计字段 (仅NPASS)
- `num_of_np_act` - 有活性的天然产物数
- `num_of_np_no_act` - 无活性的天然产物数
- `num_of_np_quantity` - 有含量数据的天然产物数

### 标记字段 (仅NPASS)
- `if_org_coculture` - 是否共培养
- `if_org_engineered` - 是否工程化
- `if_org_symbiont` - 是否共生

## 🔍 数据质量分析

### 优点
1. **匹配率极高**: 100% 的CMAUP植物都成功匹配
2. **匹配质量高**: 99.53% 为ID精确匹配，置信度高
3. **数据完整**: 保留了所有来源的数据，无数据丢失
4. **可追溯性**: 每条记录都标记了数据来源和匹配方法

### 需要注意的点
1. **低置信度匹配**: 37条记录 (0.47%) 使用属科组合匹配，可能需要人工审核
2. **NPASS独有记录**: 41,189条 (83.97%) 记录仅来自NPASS，未在CMAUP中找到对应

## 🛠️ 实施脚本

### 整合脚本
- **路径**: `scripts/data-import/integrate_cmaup_npass.py`
- **功能**:
  - 加载CMAUP和NPASS数据
  - 构建多个索引以加速匹配
  - 按优先级执行匹配
  - 合并数据并输出TSV文件
  - 生成详细报告

### 运行方法
```bash
python scripts/data-import/integrate_cmaup_npass.py
```

## 📝 示例记录

### 匹配成功记录 (BOTH)
```
org_id: NPO12205
cmaup_id: NPO12205
org_name: Eucalyptus apodophylla
cmaup_plant_name: Eucalyptus Apodophylla
species_name: Eucalyptus apodophylla
genus_name: Eucalyptus
family_name: Myrtaceae
```

### NPASS独有记录
```
org_id: NPO10
cmaup_id: (空)
org_name: Alexandrium ostenfeldii
cmaup_plant_name: (空)
species_name: Alexandrium ostenfeldii
genus_name: Alexandrium
family_name: Pyrocystaceae
```

## 🔄 下一步工作

### Phase 3: 数据库更新 (待用户确认)

1. **备份现有表**
   ```sql
   CREATE TABLE bio_resources_backup_20260205 AS
   SELECT * FROM bio_resources;
   ```

2. **更新表结构**
   - 添加新字段: `cmaup_plant_name`, `org_tax_level`, `org_tax_id`, 等
   - 参考: `scripts/database/enhance_bio_resources_table.sql`

3. **导入整合数据**
   ```sql
   TRUNCATE TABLE bio_resources CASCADE;
   COPY bio_resources FROM 'bio_resources_integrated.txt'
   WITH (FORMAT CSV, DELIMITER E'\t', HEADER true, NULL '');
   ```

4. **重建索引和约束**
   - 重建主键、外键、索引
   - 更新视图

5. **验证数据**
   - 检查记录数
   - 验证外键关联
   - 测试视图查询

## 📚 相关文档

- [数据库结构文档](database.md)
- [后端开发文档](backend-dev-doc.md)
- [CLAUDE.md](../CLAUDE.md) - 项目开发指南

## 🎉 总结

CMAUP 与 NPASS 物种数据整合工作已成功完成：

- ✅ 所有CMAUP植物 (7,865条) 100%匹配到NPASS
- ✅ 99.53% 为高置信度ID精确匹配
- ✅ 保留了所有NPASS独有记录 (41,189条)
- ✅ 数据完整性和可追溯性得到保证
- ✅ 生成了详细的整合报告和输出文件

整合后的数据集包含 49,054 条生物资源记录，为后续的数据库更新和应用开发提供了高质量的数据基础。
