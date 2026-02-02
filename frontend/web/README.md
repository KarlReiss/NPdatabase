# Natural Product Database - Web Frontend

Vue 3 前端应用，用于展示天然产物数据库的数据。

## 技术栈

- **框架**: Vue 3 + TypeScript
- **路由**: Vue Router (Hash 模式)
- **构建工具**: Vite
- **样式**: Tailwind CSS (内联类)
- **API 客户端**: Axios

## 运行方式

```bash
cd /home/yfguo/NPdatabase/frontend/web
npm install
npm run dev
```

默认访问：
- 本机：`http://localhost:3001/`
- 局域网：`http://192.168.1.6:3001/`

如果需要稳定预览（避免刷新问题），可使用：

```bash
npm run build
npm run preview -- --host 0.0.0.0 --port 3001
```

## 项目结构

```
src/
├── api/                    # API 客户端
│   ├── client.ts           # Axios 配置
│   ├── naturalProducts.ts  # 天然产物 API
│   ├── targets.ts          # 靶点 API
│   ├── search.ts           # 搜索 API
│   ├── stats.ts            # 统计 API
│   └── types.ts            # API 类型定义
├── components/             # 公共组件
│   ├── AppHeader.vue       # 导航头部
│   └── SortIcon.vue        # 排序图标
├── pages/                  # 页面组件
│   ├── Home.vue                    # 首页
│   ├── NaturalProductList.vue      # 天然产物列表
│   ├── NaturalProductDetail.vue    # 天然产物详情
│   ├── TargetList.vue              # 靶点列表
│   ├── TargetDetail.vue            # 靶点详情
│   ├── BioResourceList.vue         # 生物资源列表
│   ├── BioResourceDetail.vue       # 生物资源详情
│   ├── PrescriptionList.vue        # 处方列表
│   ├── PrescriptionDetail.vue      # 处方详情
│   ├── DiseaseList.vue             # 疾病列表
│   ├── DiseaseDetail.vue           # 疾病详情
│   ├── TopicList.vue               # 专题列表
│   └── TopicDetail.vue             # 专题详情
├── router/                 # 路由配置
│   └── index.ts
├── utils/                  # 工具函数
│   └── format.ts           # 格式化函数
├── App.vue                 # 根组件
├── main.ts                 # 入口文件
├── types.ts                # 全局类型定义
├── mockData.ts             # Mock 数据（开发用）
└── style.css               # 全局样式
```

## 主要页面

### 首页 (Home.vue)
- 搜索功能（关键词/SMILES）
- 数据库统计展示
- 快速导航卡片

### 天然产物列表 (NaturalProductList.vue)
- 侧边栏筛选（理化属性、活性、疾病）
- 数据表格（可排序）
- 分页功能
- 结构图预览

### 天然产物详情 (NaturalProductDetail.vue)
- 结构图展示
- 理化属性
- 生物活性数据
- 相关靶点
- 来源信息

### 靶点列表/详情
- 靶点基本信息
- 相关天然产物
- 疾病关联

### 生物资源列表/详情
- 药材/物种信息
- 包含的天然产物
- 传统用途

## 路由说明

主要路由：
- `/` - 首页
- `/natural-products` - 天然产物列表
- `/natural-products/:id` - 天然产物详情
- `/targets` - 靶点列表
- `/targets/:id` - 靶点详情
- `/bio-resources` - 生物资源列表
- `/bio-resources/:id` - 生物资源详情
- `/prescriptions` - 处方列表
- `/prescriptions/:id` - 处方详情
- `/diseases` - 疾病列表
- `/diseases/:id` - 疾病详情
- `/topics` - 专题列表
- `/topics/:id` - 专题详情

兼容性重定向（旧路由）：
- `/compounds` → `/natural-products`
- `/resources` → `/bio-resources`

## API 配置

API 基础地址配置在 `src/api/client.ts`：

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080/api';
```

可通过环境变量 `VITE_API_BASE_URL` 配置后端地址。

## 开发说明

### 命名规范

- **组件文件**: PascalCase (如 `NaturalProductList.vue`)
- **路由路径**: kebab-case (如 `/natural-products`)
- **API 文件**: camelCase (如 `naturalProducts.ts`)

### 数据模型

核心类型定义在 `src/types.ts` 和 `src/api/types.ts`：

- `NaturalProduct`: 天然产物（原 Compound）
- `Target`: 靶点
- `BioactivityRecord`: 生物活性记录
- `BioResource`: 生物资源（原 Species）
- `Prescription`: 处方

### Mock 数据

开发阶段使用 `src/mockData.ts` 中的 mock 数据。生产环境将连接后端 API。

## 构建部署

```bash
# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

构建产物在 `dist/` 目录，可直接部署到静态服务器。

## 注意事项

- 使用 Hash 路由模式，便于静态部署
- 双语界面（中英文混合）
- 响应式设计，支持移动端
- 所有 API 调用需要处理错误情况
