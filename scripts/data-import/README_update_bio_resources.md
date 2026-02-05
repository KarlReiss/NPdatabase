# 更新 bio_resources 表 - 使用 bio_resources_with_tcmid.txt

## 概述

本脚本用于将 `bio_resources_with_tcmid.txt` 的数据导入到数据库的 `bio_resources` 表中。

## 字段映射关系

### bio_resources_with_tcmid.txt (27 个字段) → bio_resources 表

| 源字段 (txt) | 目标字段 (数据库) | 说明 |
|-------------|------------------|------|
| org_id | resource_id | 资源ID (如: NPO16221) |
| org_name | latin_name | 拉丁名 |
| tcmid_chinese_name | chinese_name | TCMID 中文名 |
| kingdom_name | taxonomy_kingdom | 界 |
| family_name | taxonomy_family | 科 |
| genus_name | taxonomy_genus | 属 |
| species_name | taxonomy_species | 种 |
| org_tax_id | taxonomy_id | NCBI Taxonomy ID |
| species_tax_id | species_tax_id | 种的Taxonomy ID |
| genus_tax_id | genus_tax_id | 属的Taxonomy ID |
| family_tax_id | family_tax_id | 科的Taxonomy ID |
| cmaup_id | cmaup_id | CMAUP ID |
| tcmid_component_id | tcmid_id | TCMID Component ID |
| num_of_np_act | num_of_natural_products | 有活性的天然产物数 |

### 自动生成的字段

| 字段 | 生成逻辑 | 说明 |
|------|---------|------|
| resource_type | 根据 kingdom_name 判断 | Plant, Animal, Fungus, Microorganism, Unknown |

### 数据文件中没有的字段（将被设为 NULL）

以下字段在 `bio_resources_with_tcmid.txt` 中不存在，导入后将为空：

- **名称信息**: english_name, pinyin_name, alias
- **分类学信息**: taxonomy_phylum, taxonomy_class, taxonomy_order
- **药用部位**: medicinal_part, medicinal_part_latin
- **产地与分布**: origin_region, distribution, habitat
- **中医属性**: tcm_property, tcm_flavor, tcm_meridian, tcm_toxicity
- **功效与主治**: functions, indications, contraindications
- **矿物属性**: mineral_composition, mineral_crystal_system, mineral_hardness, mineral_color
- **微生物属性**: microbe_strain, microbe_culture_condition, microbe_fermentation_product
- **动物属性**: animal_class, animal_conservation_status
- **外部数据库**: tcmsp_id, herb_id
- **参考文献**: pharmacopoeia_ref, literature_ref
- **图片**: image_url
- **统计信息**: num_of_prescriptions

## 使用步骤

### 1. 准备数据库

确保数据库已创建并运行：

```bash
# 启动 PostgreSQL
sudo systemctl start postgresql

# 检查数据库是否存在
psql -U postgres -l | grep npdb
```

### 2. 添加 TCMID 字段

```bash
psql -U postgres -d npdb -f scripts/database/add_tcmid_fields_to_bio_resources.sql
```

### 3. 运行导入脚本

```bash
# 设置数据库密码（如果需要）
export DB_USER=postgres
export DB_PASSWORD=your_password

# 运行导入脚本
python3 scripts/data-import/update_bio_resources_from_tcmid.py
```

### 4. 验证数据

```bash
psql -U postgres -d npdb -c "
SELECT COUNT(*) as total,
       COUNT(CASE WHEN tcmid_id IS NOT NULL AND tcmid_id != '' THEN 1 END) as with_tcmid,
       COUNT(CASE WHEN tcmid_id IS NOT NULL AND tcmid_id != '' THEN 1 END) * 100.0 / COUNT(*) as tcmid_percentage
FROM bio_resources;
"
```

## 数据统计

### 预期结果

- **总记录数**: 49,054 条
- **有 TCMID ID 的记录**: 1,205 条 (2.46%)
- **有 TCMID 中文名的记录**: 1,205 条 (2.46%)

### 资源类型分布

根据 kingdom_name 自动判断：
- **Plant** (植物): 大部分记录
- **Animal** (动物): 少量
- **Fungus** (真菌): 少量
- **Microorganism** (微生物): 少量
- **Unknown** (未知): 少量

## 注意事项

### ⚠️ 重要警告

1. **数据将被清空**: 脚本会先执行 `TRUNCATE TABLE bio_resources CASCADE`，清空所有现有数据
2. **级联删除**: CASCADE 会同时清空关联表的数据（如 bio_resource_natural_products）
3. **备份建议**: 运行前请先备份数据库

### 备份命令

```bash
# 备份整个数据库
pg_dump -U postgres npdb > backup_npdb_$(date +%Y%m%d_%H%M%S).sql

# 仅备份 bio_resources 表
pg_dump -U postgres -t bio_resources npdb > backup_bio_resources_$(date +%Y%m%d_%H%M%S).sql
```

### 恢复命令

```bash
# 恢复整个数据库
psql -U postgres npdb < backup_npdb_20260205_034500.sql

# 恢复单个表
psql -U postgres npdb < backup_bio_resources_20260205_034500.sql
```

## 字段缺失处理

由于数据文件中缺少很多字段，建议后续：

1. **补充中医属性**: tcm_property, tcm_flavor, tcm_meridian, tcm_toxicity
2. **补充功效信息**: functions, indications, contraindications
3. **补充产地信息**: origin_region, distribution
4. **补充外部链接**: tcmsp_id, herb_id

可以从以下数据源补充：
- TCMID 数据库
- TCMSP 数据库
- 中国药典
- 其他中医药数据库

## 脚本说明

### update_bio_resources_from_tcmid.py

**功能**:
1. 读取 `bio_resources_with_tcmid.txt`
2. 映射字段到数据库表结构
3. 自动判断资源类型
4. 清空并重新导入数据
5. 验证导入结果

**参数**:
- 通过环境变量配置: `DB_USER`, `DB_PASSWORD`
- 默认数据库: `npdb`
- 默认主机: `localhost:5432`

**输出**:
- 导入进度显示
- 数据统计信息
- 示例记录展示

## 后续步骤

导入完成后，建议：

1. **更新统计信息**:
   ```sql
   ANALYZE bio_resources;
   ```

2. **重建索引**:
   ```sql
   REINDEX TABLE bio_resources;
   ```

3. **更新关联表**:
   - 导入 `prescription_resources_data.txt` 到 `prescription_resources` 表
   - 更新 `bio_resource_natural_products` 表

4. **验证视图**:
   ```sql
   SELECT * FROM v_bio_resource_detail LIMIT 10;
   ```

## 问题排查

### 连接失败

```bash
# 检查 PostgreSQL 是否运行
sudo systemctl status postgresql

# 检查端口
sudo netstat -tlnp | grep 5432

# 检查用户权限
psql -U postgres -c "\du"
```

### 导入失败

```bash
# 检查文件是否存在
ls -lh /home/yfguo/NPdatabase/data/processed/bio_resources_with_tcmid.txt

# 检查文件编码
file /home/yfguo/NPdatabase/data/processed/bio_resources_with_tcmid.txt

# 检查表结构
psql -U postgres -d npdb -c "\d bio_resources"
```

## 联系方式

如有问题，请查看：
- 项目文档: `/home/yfguo/NPdatabase/docs/`
- 数据库文档: `/home/yfguo/NPdatabase/docs/database.md`
