# diseases 表结构说明

## 📋 问题说明

用户询问：diseases 表中的 disease_id 字段似乎不见了，是否需要在导入方案中增加？

## ✅ 答案

**不需要增加 disease_id 字段**。该字段已经在表结构优化时被删除。

## 🔍 原因分析

根据 `scripts/database/update_diseases_with_integrated_data.py` 脚本（第78-84行），diseases 表在数据整合时进行了结构优化，删除了以下字段：

```python
fields_to_drop = [
    'disease_id',        # ← 已删除
    'description',       # ← 已删除
    'symptoms',          # ← 已删除
    'num_of_related_plants',    # ← 已删除
    'num_of_related_targets'    # ← 已删除
]
```

## 📊 当前 diseases 表结构

### 保留的字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGSERIAL | 主键（自增） |
| icd11_code | VARCHAR(50) | ICD-11编码（唯一标识） |
| disease_name | VARCHAR(500) | 疾病英文名称 |
| disease_name_zh | VARCHAR(500) | 疾病中文名称 |
| disease_category | VARCHAR(200) | 疾病分类 |
| disease_name_cmaup | VARCHAR(500) | CMAUP疾病名称（新增） |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 删除的字段

| 字段 | 原类型 | 删除原因 |
|------|--------|---------|
| disease_id | VARCHAR(50) | 冗余字段，icd11_code 已足够作为唯一标识 |
| description | TEXT | 数据源中无此信息 |
| symptoms | TEXT | 数据源中无此信息 |
| num_of_related_plants | INT | 可通过关联表动态计算 |
| num_of_related_targets | INT | 可通过关联表动态计算 |

## 🎯 导入方案的正确性

### 当前导入脚本的映射方式

```python
# 映射 ICD-11 Code 到 disease_id（这里的 disease_id 是指数据库的 id 主键）
icd11_code = clean_value(row.get('ICD-11 Code'))
if not icd11_code or icd11_code not in disease_mapping:
    stats['skipped_no_disease'] += 1
    continue
disease_id = disease_mapping[icd11_code]  # 这是 diseases.id，不是 diseases.disease_id
```

### 映射逻辑

```python
def load_disease_mapping(conn):
    """加载疾病ID映射 (icd11_code -> id)"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, icd11_code FROM diseases WHERE icd11_code IS NOT NULL")
    mapping = {icd11_code: id for id, icd11_code in cursor.fetchall()}
    return mapping
```

**说明**：
- 源数据的 `ICD-11 Code` → diseases 表的 `icd11_code` 字段
- 通过 `icd11_code` 查找对应的 `id`（主键）
- 将 `id` 存储到 `bio_resource_disease_associations.disease_id` 外键字段

这是完全正确的做法！

## 📝 表结构演变历史

### 1. 初始设计（create_diseases_table.sql）

```sql
CREATE TABLE diseases (
    id BIGSERIAL PRIMARY KEY,
    disease_id VARCHAR(50) UNIQUE NOT NULL,  -- 业务ID，如 DIS0001
    icd11_code VARCHAR(50) NOT NULL,
    disease_name VARCHAR(500) NOT NULL,
    disease_name_zh VARCHAR(500),
    disease_category VARCHAR(200),
    description TEXT,
    symptoms TEXT,
    num_of_related_plants INT DEFAULT 0,
    num_of_related_targets INT DEFAULT 0,
    ...
);
```

### 2. 优化后的结构（当前）

```sql
CREATE TABLE diseases (
    id BIGSERIAL PRIMARY KEY,
    -- disease_id 已删除
    icd11_code VARCHAR(50) NOT NULL,         -- 作为唯一标识
    disease_name VARCHAR(500) NOT NULL,
    disease_name_zh VARCHAR(500),
    disease_category VARCHAR(200),
    disease_name_cmaup VARCHAR(500),         -- 新增
    -- description 已删除
    -- symptoms 已删除
    -- num_of_related_plants 已删除
    -- num_of_related_targets 已删除
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## ✅ 结论

1. **disease_id 字段已被删除**，这是正确的优化决策
2. **icd11_code 作为唯一标识**，足以满足业务需求
3. **导入脚本无需修改**，当前的映射逻辑完全正确
4. **统计字段已删除**，可通过关联表动态计算，避免数据不一致

## 🔄 如果需要统计字段

如果后续需要统计字段（如 num_of_related_plants），可以：

### 方案1: 动态计算（推荐）

```sql
-- 查询时动态计算
SELECT
    d.*,
    COUNT(DISTINCT brda.bio_resource_id) as num_of_related_plants
FROM diseases d
LEFT JOIN bio_resource_disease_associations brda ON d.id = brda.disease_id
GROUP BY d.id;
```

### 方案2: 创建物化视图

```sql
CREATE MATERIALIZED VIEW diseases_with_stats AS
SELECT
    d.*,
    COUNT(DISTINCT brda.bio_resource_id) as num_of_related_plants
FROM diseases d
LEFT JOIN bio_resource_disease_associations brda ON d.id = brda.disease_id
GROUP BY d.id;

-- 定期刷新
REFRESH MATERIALIZED VIEW diseases_with_stats;
```

### 方案3: 添加统计字段并定期更新

```sql
-- 添加字段
ALTER TABLE diseases ADD COLUMN num_of_related_plants INT DEFAULT 0;

-- 更新统计（使用 update_bio_resource_disease_stats.sql）
UPDATE diseases d
SET num_of_related_plants = (
    SELECT COUNT(DISTINCT bio_resource_id)
    FROM bio_resource_disease_associations
    WHERE disease_id = d.id
);
```

## 📚 相关文件

- `scripts/database/create_diseases_table.sql` - 初始表结构定义
- `scripts/database/update_diseases_with_integrated_data.py` - 表结构优化脚本
- `scripts/database/import_bio_resource_disease_associations.py` - 关联数据导入脚本
- `scripts/database/update_bio_resource_disease_stats.sql` - 统计更新脚本（可选）

## 🎯 总结

**disease_id 字段的删除是合理的优化决策**，因为：

1. ✅ ICD-11 Code 本身就是国际标准的疾病编码，足以作为唯一标识
2. ✅ 避免了维护两套ID系统的复杂性
3. ✅ 减少了数据冗余
4. ✅ 简化了表结构

**导入方案无需修改**，当前的实现完全正确！
