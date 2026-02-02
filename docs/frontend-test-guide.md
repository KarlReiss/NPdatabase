# 前端联调与测试教程（Vue 原型）

**更新日期**：2026-01-29  
**环境说明**：代码与数据库均部署在服务器，服务器 IP 为 `192.168.1.6`；你在局域网本地 PC（Windows）上通过 IP 访问进行测试。

---

## 1. 前置条件

- 后端服务已启动并监听 `192.168.1.6:8080`
- 前端项目路径：`/home/yfguo/NPdatabase/frontend/prototype-vue`
- 已安装 Node.js 与 npm

---

## 2. 使用后台启动脚本（推荐）

项目已提供后台启动脚本：`/home/yfguo/NPdatabase/scripts/backend-service.sh`

### 2.1 启动
```bash
cd /home/yfguo/NPdatabase
DB_USER=yfguo DB_PASSWORD=npdb2024 SERVER_ADDRESS=0.0.0.0 ./scripts/backend-service.sh start
```

### 2.2 停止
```bash
./scripts/backend-service.sh stop
```

### 2.3 重启
```bash
./scripts/backend-service.sh restart
```

### 2.4 状态
```bash
./scripts/backend-service.sh status
```

### 2.5 查看日志
```bash
./scripts/backend-service.sh logs
```

**日志路径**：`backend/logs/backend.log`

---

## 3. 后端接口基础检查（服务器上执行）

在服务器上执行以下命令，确认核心接口可用：

1) 健康检查
```bash
curl -i http://192.168.1.6:8080/api/health
```

2) 统计接口
```bash
curl -i http://192.168.1.6:8080/api/stats
```

3) 天然产物列表
```bash
curl -i "http://192.168.1.6:8080/api/natural-products?page=1&pageSize=5"
```

4) 靶点列表
```bash
curl -i "http://192.168.1.6:8080/api/targets?page=1&pageSize=5"
```

5) 搜索接口
```bash
curl -i "http://192.168.1.6:8080/api/search?q=EGFR&type=all"
```

**期望结果**：接口返回 `code=0`，数据结构包含 `data` 字段。

---

## 4. 前端启动（开发模式，推荐）

开发模式通过 Vite 代理 `/api` 到后端，避免 CORS 问题。

```bash
cd /home/yfguo/NPdatabase/frontend/prototype-vue
VITE_API_PROXY_TARGET=http://192.168.1.6:8080 npm run dev -- --host 0.0.0.0 --port 3001
```

**在 Win 本地 PC 浏览器访问：**
```
http://192.168.1.6:3001
```

---

## 5. 前端启动（生产/预览模式）

若需要验证生产构建输出：

```bash
cd /home/yfguo/NPdatabase/frontend/prototype-vue
VITE_API_BASE_URL=http://192.168.1.6:8080 npm run build
npm run preview -- --host 0.0.0.0 --port 3001
```

**在 Win 本地 PC 浏览器访问：**
```
http://192.168.1.6:3001
```

---

## 6. 功能验收清单（Win 本地 PC 操作）

### 6.1 首页
- 统计卡片显示真实数字（非 `—`）
- 搜索框输入关键词后可跳转到列表或详情

### 6.2 化合物列表
- 列表有真实数据、总数正确
- 表头排序可用
- 筛选（MW/XLogP/PSA/活性阈值/毒性）生效
- 分页可切换

### 6.3 化合物详情
- 详情基础信息完整
- 活性表格有记录
- 靶点与来源资源可显示

### 6.4 靶点列表
- 数据可加载
- 排序与分页可用

### 6.5 靶点详情
- 详情信息可显示
- 相关天然产物列表可显示

---

## 7. 常见问题排查

### 7.1 页面一直刷新/打不开
- 确认前端启动命令包含 `--host 0.0.0.0`
- 确认服务器防火墙未阻止 3001 端口

### 7.2 前端请求报错
- 推荐使用开发模式（代理）而不是直接访问后端
- 若必须生产模式，请确认后端已开启 CORS 或使用 Nginx 反代

### 7.3 搜索无结果
- 确认关键字存在于数据库（`np_id` 或 `target_id` 或名称）
- 使用 `/api/search` 接口先验证返回数据

---

## 8. 备注

- 我已在本机完成 `npm run build` 的构建测试，构建通过。
- 若需要自动化测试脚本或更细的验收表，可再扩展此文档。
