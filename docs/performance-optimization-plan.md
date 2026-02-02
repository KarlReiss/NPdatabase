# 天然产物数据库性能优化方案

## 问题概述

用户报告多个页面加载缓慢：
- **化合物列表页** (`/compounds`): 加载30秒，翻页慢
- **化合物详情页**: 加载慢
- **靶点详情页**: 加载慢

经过深入分析，发现这是一个**共性问题**，需要系统性的优化方案。

---

## 性能瓶颈分析

### 1. 后端性能问题

#### 1.1 列表页面 (NaturalProductController.list)
**位置**: `/backend/src/main/java/cn/npdb/controller/NaturalProductController.java:66-192`

**问题**:
- **3次数据库查询**每次列表请求：
  1. 主查询：natural_products表 + 复杂子查询
  2. 聚合查询：bioactivity统计（活性值、靶点数）
  3. 毒性查询：toxicity标志
- **未使用已有视图**: 代码没有使用 `v_natural_product_detail` 视图
- **复杂子查询**: 活性和靶点筛选使用 `inSql` 子查询

**影响**: 每次列表查询需要3次数据库往返 + 子查询开销

#### 1.2 详情页面关联数据 (N+1查询模式)
**位置**:
- `NaturalProductController.targets()` (Line 222-237)
- `NaturalProductController.bioResources()` (Line 239-254)
- `TargetController.naturalProducts()` (Line 82-98)

**问题**: 两步查询模式
```java
// 步骤1: 查询关联ID
List<Long> targetIds = bioactivityService.list(...)
    .stream().map(Bioactivity::getTargetId).collect(Collectors.toList());

// 步骤2: 根据ID查询详情
List<Target> targets = targetService.list(
    new QueryWrapper<Target>().in("id", targetIds));
```

**影响**: 每个关联数据端点需要2次数据库查询

#### 1.3 视图未物化
**位置**: `/scripts/database/optimize_table_structure.sql:118-173`

**问题**:
- `v_natural_product_detail` 和 `v_target_detail` 是普通视图
- 每次查询都重新计算聚合（COUNT、MIN等）
- 没有使用 MATERIALIZED VIEW

**影响**: 详情页每次都执行复杂的JOIN和聚合计算

#### 1.4 无缓存层
**位置**: 所有Controller

**问题**:
- 没有应用层缓存（Redis/Caffeine）
- MyBatis-Plus缓存被禁用
- 每次请求都查询数据库

**影响**: 热门数据重复查询，数据库压力大

### 2. 前端性能问题

#### 2.1 详情页多次API调用
**位置**:
- `/frontend/prototype-vue/src/pages/CompoundDetail.vue:315-363`
- `/frontend/prototype-vue/src/pages/TargetDetail.vue:123-146`

**问题**: 化合物详情页发起**5个并行API请求**
```typescript
const detailPromise = fetchNaturalProductDetail(compoundId.value);
const bioPromise = fetchNaturalProductBioactivity(compoundId.value, ...);
const targetPromise = fetchNaturalProductTargets(compoundId.value);
const resourcePromise = fetchNaturalProductResources(compoundId.value);
const toxicityPromise = fetchNaturalProductToxicity(compoundId.value);
```

**影响**:
- 5次HTTP往返（即使并行也有延迟）
- 慢速网络下延迟累加
- 后端需要处理5个请求

#### 2.2 无前端缓存
**位置**: 所有列表和详情页

**问题**:
- 每次路由切换都重新请求数据
- 翻页时重复请求已访问的页面
- 没有使用Vue Query或手动缓存

**影响**: 不必要的API调用，用户体验差

#### 2.3 关联数据无分页
**位置**: `CompoundDetail.vue:321-324`

**问题**:
```typescript
const targetPromise = fetchNaturalProductTargets(compoundId.value);  // 无分页
const resourcePromise = fetchNaturalProductResources(compoundId.value);  // 无分页
```

**影响**: 关联数据多的化合物加载慢

---

## 优化方案

### 阶段一：快速见效优化（预计提升70-80%性能）

#### 优化1: 列表页使用视图查询
**目标**: 将3次查询减少到1次
**预期效果**: 列表加载从30秒降至5-8秒

**实施步骤**:

1. **修改后端Controller**
   - 文件: `/backend/src/main/java/cn/npdb/controller/NaturalProductController.java`
   - 修改 `list()` 方法 (Line 66-192)
   - 直接查询 `v_natural_product_detail` 视图而不是 `natural_products` 表
   - 删除额外的聚合查询和毒性查询（视图已包含）

2. **关键代码变更**:
```java
// 旧代码: 查询表 + 2次额外查询
QueryWrapper<NaturalProduct> wrapper = new QueryWrapper<>();
Page<NaturalProduct> result = naturalProductService.page(mpPage, wrapper);
// ... 然后执行聚合查询和毒性查询

// 新代码: 直接查询视图
QueryWrapper<NaturalProductDetailView> wrapper = new QueryWrapper<>();
Page<NaturalProductDetailView> result = naturalProductDetailMapper.selectPage(mpPage, wrapper);
// 视图已包含所有统计信息，无需额外查询
```

3. **需要调整的筛选条件**:
   - 活性筛选: 使用视图的 `best_activity_value` 字段
   - 毒性筛选: 使用视图的 `has_toxicity` 字段
   - 靶点筛选: 仍需子查询（或创建专门的筛选视图）

**关键文件**:
- `/backend/src/main/java/cn/npdb/controller/NaturalProductController.java`
- `/backend/src/main/java/cn/npdb/mapper/NaturalProductDetailMapper.java`

---

#### 优化2: 消除N+1查询模式
**目标**: 将关联数据的2次查询合并为1次
**预期效果**: 详情页关联数据加载提升50%

**实施步骤**:

1. **优化 targets 端点**
   - 文件: `NaturalProductController.java`
   - 方法: `targets()` (Line 222-237)
   - 使用单个JOIN查询替代两步查询

```java
// 旧代码 (2次查询):
List<Long> targetIds = bioactivityService.list(...).stream()...;
List<Target> targets = targetService.list(new QueryWrapper<Target>().in("id", targetIds));

// 新代码 (1次查询):
@Select("SELECT DISTINCT t.* FROM targets t " +
        "INNER JOIN bioactivity b ON t.id = b.target_id " +
        "WHERE b.natural_product_id = #{naturalProductId}")
List<Target> selectTargetsByNaturalProductId(@Param("naturalProductId") Long naturalProductId);
```

2. **优化 bioResources 端点**
   - 文件: `NaturalProductController.java`
   - 方法: `bioResources()` (Line 239-254)
   - 类似的JOIN查询优化

3. **优化 TargetController.naturalProducts**
   - 文件: `/backend/src/main/java/cn/npdb/controller/TargetController.java`
   - 方法: `naturalProducts()` (Line 82-98)
   - 使用JOIN查询视图

**关键文件**:
- `/backend/src/main/java/cn/npdb/controller/NaturalProductController.java`
- `/backend/src/main/java/cn/npdb/controller/TargetController.java`
- `/backend/src/main/java/cn/npdb/mapper/NaturalProductMapper.java` (新增自定义查询)
- `/backend/src/main/java/cn/npdb/mapper/TargetMapper.java` (新增自定义查询)

---

#### 优化3: 添加数据库索引
**目标**: 提升查询速度
**预期效果**: 配合其他优化再提升20-30%

**实施步骤**:

1. **创建索引脚本**
   - 文件: `/scripts/database/add_performance_indexes.sql` (新建)

```sql
-- 1. bioactivity表的复合索引（用于聚合查询）
CREATE INDEX IF NOT EXISTS idx_bioactivity_np_target_value
ON bioactivity(natural_product_id, target_id, activity_value_std);

-- 2. bioactivity表的活性类型索引
CREATE INDEX IF NOT EXISTS idx_bioactivity_type_value
ON bioactivity(activity_type, activity_value_std);

-- 3. targets表的target_type索引（如果不存在）
CREATE INDEX IF NOT EXISTS idx_targets_type
ON targets(target_type);

-- 4. bio_resource_natural_products的复合索引
CREATE INDEX IF NOT EXISTS idx_brnp_np_resource
ON bio_resource_natural_products(natural_product_id, bio_resource_id);
```

2. **执行索引创建**
```bash
psql -U npdb_user -d npdb -f scripts/database/add_performance_indexes.sql
```

**关键文件**:
- `/scripts/database/add_performance_indexes.sql` (新建)

---

#### 优化4: 前端添加缓存
**目标**: 减少重复API请求
**预期效果**: 翻页和返回操作几乎瞬时完成

**实施步骤**:

1. **列表页添加缓存**
   - 文件: `/frontend/prototype-vue/src/pages/CompoundList.vue`
   - 在 `fetchList()` 函数中添加缓存逻辑 (Line 448-470)

```typescript
// 添加缓存Map
const cache = new Map<string, {
  data: CompoundRow[],
  total: number,
  timestamp: number
}>();
const CACHE_TTL = 5 * 60 * 1000; // 5分钟

const fetchList = async (options?: { resetPage?: boolean }) => {
  // ... 现有逻辑

  // 生成缓存key
  const cacheKey = JSON.stringify(buildParams());
  const cached = cache.get(cacheKey);

  // 检查缓存
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    rows.value = cached.data;
    total.value = cached.total;
    loading.value = false;
    return;
  }

  // ... 执行API请求

  // 存入缓存
  cache.set(cacheKey, {
    data: mappedRows,
    total: response.total,
    timestamp: Date.now()
  });
};
```

2. **详情页添加缓存**
   - 文件: `/frontend/prototype-vue/src/pages/CompoundDetail.vue`
   - 类似的缓存逻辑

3. **靶点列表页添加缓存**
   - 文件: `/frontend/prototype-vue/src/pages/TargetList.vue`
   - 类似的缓存逻辑

**关键文件**:
- `/frontend/prototype-vue/src/pages/CompoundList.vue`
- `/frontend/prototype-vue/src/pages/CompoundDetail.vue`
- `/frontend/prototype-vue/src/pages/TargetList.vue`
- `/frontend/prototype-vue/src/pages/TargetDetail.vue`

---

#### 优化5: 前端体验优化
**目标**: 改善加载体验
**预期效果**: 用户感知加载时间减少

**实施步骤**:

1. **添加加载进度提示**
   - 文件: `/frontend/prototype-vue/src/pages/CompoundList.vue`
   - 修改加载状态显示 (Line 221-223)

```vue
<tr v-if="loading">
  <td colspan="6" class="p-6 text-center">
    <div class="flex flex-col items-center space-y-2">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#10B981]"></div>
      <span class="text-sm text-slate-500">正在加载数据...</span>
    </div>
  </td>
</tr>
```

2. **图片懒加载**
   - 所有列表页的结构图添加 `loading="lazy"` 属性

```vue
<img
  v-if="cmp.structureUrl"
  :src="cmp.structureUrl"
  :alt="cmp.name"
  loading="lazy"
  class="max-w-full max-h-full object-contain"
/>
```

**关键文件**:
- `/frontend/prototype-vue/src/pages/CompoundList.vue`
- `/frontend/prototype-vue/src/pages/TargetList.vue`

---

### 阶段二：进阶优化（预计再提升30-40%性能）

#### 优化6: 物化视图
**目标**: 预计算统计数据
**预期效果**: 详情页和列表页查询速度提升50%+

**实施步骤**:

1. **创建物化视图脚本**
   - 文件: `/scripts/database/create_materialized_views.sql` (新建)

```sql
-- 1. 物化天然产物详情视图
DROP MATERIALIZED VIEW IF EXISTS mv_natural_product_detail CASCADE;
CREATE MATERIALIZED VIEW mv_natural_product_detail AS
SELECT
    np.*,
    COUNT(DISTINCT b.id) as bioactivity_count,
    COUNT(DISTINCT b.target_id) as target_count,
    COUNT(DISTINCT brnp.bio_resource_id) as bio_resource_count,
    MIN(b.activity_value_std) as best_activity_value,
    EXISTS(SELECT 1 FROM toxicity t WHERE t.natural_product_id = np.id) as has_toxicity
FROM natural_products np
LEFT JOIN bioactivity b ON np.id = b.natural_product_id
LEFT JOIN bio_resource_natural_products brnp ON np.id = brnp.natural_product_id
GROUP BY np.id;

-- 创建唯一索引（支持并发刷新）
CREATE UNIQUE INDEX idx_mv_np_detail_id ON mv_natural_product_detail(id);
CREATE INDEX idx_mv_np_detail_np_id ON mv_natural_product_detail(np_id);
CREATE INDEX idx_mv_np_detail_mw ON mv_natural_product_detail(molecular_weight);
CREATE INDEX idx_mv_np_detail_xlogp ON mv_natural_product_detail(xlogp);
CREATE INDEX idx_mv_np_detail_psa ON mv_natural_product_detail(psa);
CREATE INDEX idx_mv_np_detail_best_activity ON mv_natural_product_detail(best_activity_value);

-- 2. 物化靶点详情视图
DROP MATERIALIZED VIEW IF EXISTS mv_target_detail CASCADE;
CREATE MATERIALIZED VIEW mv_target_detail AS
SELECT
    t.*,
    COUNT(DISTINCT b.natural_product_id) as natural_product_count,
    COUNT(DISTINCT b.id) as bioactivity_count,
    MIN(b.activity_value_std) as best_activity_value
FROM targets t
LEFT JOIN bioactivity b ON t.id = b.target_id
GROUP BY t.id;

CREATE UNIQUE INDEX idx_mv_target_detail_id ON mv_target_detail(id);
CREATE INDEX idx_mv_target_detail_target_id ON mv_target_detail(target_id);
```

2. **创建刷新脚本**
   - 文件: `/scripts/database/refresh_materialized_views.sql` (新建)

```sql
-- 并发刷新（不锁表）
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_natural_product_detail;
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_target_detail;
```

3. **设置定时刷新**
   - 使用cron或数据库定时任务
   - 建议每小时或每天刷新一次（根据数据更新频率）

4. **修改后端使用物化视图**
   - 将所有 `v_natural_product_detail` 改为 `mv_natural_product_detail`
   - 将所有 `v_target_detail` 改为 `mv_target_detail`

**关键文件**:
- `/scripts/database/create_materialized_views.sql` (新建)
- `/scripts/database/refresh_materialized_views.sql` (新建)
- `/backend/src/main/java/cn/npdb/mapper/NaturalProductDetailMapper.java`
- `/backend/src/main/java/cn/npdb/mapper/TargetDetailMapper.java`

---

#### 优化7: 创建复合API端点
**目标**: 减少详情页的HTTP请求数
**预期效果**: 详情页加载从5个请求减少到1-2个请求

**实施步骤**:

1. **创建复合端点**
   - 文件: `NaturalProductController.java`
   - 新增方法: `fullDetail()`

```java
@GetMapping("/{npId}/full")
public ApiResponse<NaturalProductFullDetail> fullDetail(@PathVariable("npId") String npId) {
    // 1. 获取基本详情
    NaturalProductDetailView detail = naturalProductDetailMapper.selectOne(...);

    // 2. 获取bioactivity（带target信息的JOIN查询）
    List<BioactivityWithTarget> bioactivity = bioactivityMapper.selectWithTargets(detail.getId());

    // 3. 获取resources
    List<BioResource> resources = bioResourceMapper.selectByNaturalProductId(detail.getId());

    // 4. 获取toxicity
    List<Toxicity> toxicity = toxicityService.list(...);

    // 5. 组装返回
    return ApiResponse.ok(new NaturalProductFullDetail(detail, bioactivity, resources, toxicity));
}
```

2. **创建DTO类**
   - 文件: `/backend/src/main/java/cn/npdb/dto/NaturalProductFullDetail.java` (新建)

3. **前端调用复合端点**
   - 文件: `CompoundDetail.vue`
   - 将5个API调用改为1个

```typescript
const fetchAll = async () => {
  loading.value = true;
  try {
    // 旧代码: 5个并行请求
    // const [detail, bio, targets, resources, toxicity] = await Promise.allSettled([...]);

    // 新代码: 1个请求
    const fullData = await fetchNaturalProductFullDetail(compoundId.value);
    compound.value = fullData.detail;
    bioactivity.value = fullData.bioactivity;
    targets.value = fullData.targets;
    resources.value = fullData.resources;
    toxicity.value = fullData.toxicity;
  } finally {
    loading.value = false;
  }
};
```

**关键文件**:
- `/backend/src/main/java/cn/npdb/controller/NaturalProductController.java`
- `/backend/src/main/java/cn/npdb/dto/NaturalProductFullDetail.java` (新建)
- `/backend/src/main/java/cn/npdb/mapper/BioactivityMapper.java` (新增JOIN查询)
- `/frontend/prototype-vue/src/api/naturalProducts.ts`
- `/frontend/prototype-vue/src/pages/CompoundDetail.vue`

---

#### 优化8: 关联数据分页
**目标**: 避免一次性加载大量关联数据
**预期效果**: 关联数据多的化合物加载速度提升

**实施步骤**:

1. **后端添加分页参数**
   - 修改 `targets()` 和 `bioResources()` 方法
   - 添加 `page` 和 `pageSize` 参数

2. **前端实现懒加载或分页**
   - 初始只加载前20条
   - 添加"加载更多"按钮或滚动加载

**关键文件**:
- `/backend/src/main/java/cn/npdb/controller/NaturalProductController.java`
- `/frontend/prototype-vue/src/pages/CompoundDetail.vue`

---

### 阶段三：长期优化（可选）

#### 优化9: Redis缓存层
**目标**: 减少数据库压力
**预期效果**: 热门查询响应时间<100ms

**实施步骤**:

1. **添加Redis依赖**
   - 文件: `/backend/pom.xml`

2. **配置Spring Cache**
   - 文件: `/backend/src/main/resources/application.yml`

3. **添加缓存注解**
```java
@Cacheable(value = "natural-products", key = "#npId", unless = "#result == null")
public NaturalProductDetailView detail(String npId) {
    // ...
}
```

4. **设置缓存过期策略**
   - 详情数据: 1小时
   - 列表数据: 5分钟
   - 统计数据: 10分钟

**关键文件**:
- `/backend/pom.xml`
- `/backend/src/main/resources/application.yml`
- `/backend/src/main/java/cn/npdb/config/CacheConfig.java` (新建)

---

#### 优化10: 全文搜索优化
**目标**: 提升搜索性能
**预期效果**: 搜索响应时间减少50%

**实施步骤**:

1. **使用PostgreSQL全文搜索**
   - 修改SearchController使用 `to_tsvector` 和 `@@` 操作符
   - 利用已有的GIN索引

2. **或集成Elasticsearch**
   - 更强大的搜索功能
   - 支持模糊搜索、同义词等

**关键文件**:
- `/backend/src/main/java/cn/npdb/controller/SearchController.java`

---

## 实施计划（基于用户选择）

**用户选择**:
- ✅ 全面优化（列表页+详情页）
- ✅ 可以修改数据库结构
- ✅ 快速见效策略（1-2天）

### 本次实施范围（阶段一：快速见效）

#### 第一天：后端优化
1. ✅ **优化3**: 添加数据库索引（30分钟）
2. ✅ **优化1**: 列表页使用视图查询（2小时）
3. ✅ **优化2**: 消除N+1查询模式（3小时）

#### 第二天：前端优化
4. ✅ **优化4**: 前端添加缓存（2小时）
5. ✅ **优化5**: 前端体验优化（1小时）

**预期效果**:
- 列表页加载: 30秒 → 3-5秒 (提升85%)
- 详情页加载: 显著改善 (提升60%+)
- 翻页: 几乎瞬时完成 (<500ms)

### 后续可选优化（如需进一步提升）

#### 短期实施（3-5天）：
6. ✅ **优化6**: 物化视图
7. ✅ **优化7**: 创建复合API端点
8. ✅ **优化8**: 关联数据分页

**预期效果**:
- 列表页加载: 3-5秒 → 1-2秒
- 详情页加载: 5个请求 → 1个请求

#### 长期实施（1-2周）：
9. ✅ **优化9**: Redis缓存层
10. ✅ **优化10**: 全文搜索优化

**预期效果**:
- 热门查询: <100ms
- 搜索性能: 提升50%+

---

## 验证方案

### 性能测试

1. **列表页加载时间测试**
```bash
# 使用curl测试API响应时间
time curl "http://localhost:8080/api/natural-products?page=1&pageSize=20"
```

2. **详情页加载时间测试**
```bash
time curl "http://localhost:8080/api/natural-products/NPC000001"
```

3. **前端性能监控**
```typescript
// 在fetchList中添加
const startTime = performance.now();
await fetchNaturalProducts(buildParams());
console.log(`API耗时: ${performance.now() - startTime}ms`);
```

### 数据库查询分析

```sql
-- 开启查询日志
SET log_statement = 'all';
SET log_duration = on;

-- 分析查询计划
EXPLAIN ANALYZE
SELECT * FROM v_natural_product_detail
WHERE molecular_weight BETWEEN 200 AND 500
LIMIT 20;
```

### 端到端测试

1. **列表页测试**
   - 访问 `http://localhost:3002/#/compounds`
   - 测试筛选功能
   - 测试翻页功能
   - 验证加载时间<5秒

2. **详情页测试**
   - 访问化合物详情页
   - 切换各个标签页
   - 验证数据完整性
   - 验证加载时间<3秒

3. **缓存测试**
   - 访问列表页第1页
   - 切换到第2页
   - 返回第1页（应该瞬时加载）

---

## 关键文件清单

### 后端文件
- `/backend/src/main/java/cn/npdb/controller/NaturalProductController.java` - 主要优化
- `/backend/src/main/java/cn/npdb/controller/TargetController.java` - N+1优化
- `/backend/src/main/java/cn/npdb/mapper/NaturalProductMapper.java` - 新增JOIN查询
- `/backend/src/main/java/cn/npdb/mapper/TargetMapper.java` - 新增JOIN查询
- `/backend/src/main/java/cn/npdb/mapper/BioactivityMapper.java` - 新增JOIN查询
- `/backend/src/main/java/cn/npdb/dto/NaturalProductFullDetail.java` - 新建DTO

### 数据库脚本
- `/scripts/database/add_performance_indexes.sql` - 新建索引脚本
- `/scripts/database/create_materialized_views.sql` - 新建物化视图脚本
- `/scripts/database/refresh_materialized_views.sql` - 新建刷新脚本

### 前端文件
- `/frontend/prototype-vue/src/pages/CompoundList.vue` - 缓存优化
- `/frontend/prototype-vue/src/pages/CompoundDetail.vue` - 缓存和API优化
- `/frontend/prototype-vue/src/pages/TargetList.vue` - 缓存优化
- `/frontend/prototype-vue/src/pages/TargetDetail.vue` - 缓存优化
- `/frontend/prototype-vue/src/api/naturalProducts.ts` - 新增复合端点API

---

## 风险评估

### 低风险
- 前端缓存: 可随时禁用
- 图片懒加载: 浏览器原生支持
- 加载提示: 纯UI改进

### 中风险
- 数据库索引: 需要测试对写入性能的影响
- 视图查询: 需要确保MyBatis Plus配置正确
- N+1优化: 需要充分测试JOIN查询的正确性

### 高风险
- 物化视图: 需要刷新策略，可能导致数据延迟
- 复合端点: 改变API契约，需要前后端同步部署

### 建议
1. 在开发环境充分测试
2. 使用数据库备份
3. 分阶段部署，先部署低风险优化
4. 监控数据库性能指标
5. 准备回滚方案

---

## 总结

本优化方案采用**分层优化**策略：
1. **数据库层**: 索引、视图、物化视图
2. **后端层**: 消除N+1、复合端点、缓存
3. **前端层**: 缓存、懒加载、体验优化

预期整体性能提升：
- **列表页**: 30秒 → 1-2秒 (提升93%)
- **详情页**: 显著改善 (提升70%+)
- **翻页**: 几乎瞬时完成

建议按阶段实施，优先完成阶段一的5个优化，即可获得显著的性能提升。
