# DBeaver 连接 PostgreSQL 数据库指南

## 配置完成状态 ✅

PostgreSQL服务器已成功配置为允许远程连接！

---

## 服务器配置信息

### 已完成的配置

1. ✅ **PostgreSQL监听配置**
   - `listen_addresses = '*'` (监听所有网络接口)
   - 服务器正在监听: `0.0.0.0:5432` 和 `:::5432`

2. ✅ **访问控制配置** (`pg_hba.conf`)
   - 允许本地连接 (127.0.0.1)
   - 允许局域网连接 (192.168.1.0/24)
   - 允许桌面网络连接 (172.16.90.0/24)
   - 认证方式: scram-sha-256

3. ✅ **用户密码设置**
   - 用户 `yfguo` 密码已设置为: `npdb2024`

4. ✅ **PostgreSQL服务**
   - 服务已重启并正常运行
   - 版本: PostgreSQL 16.3

---

## DBeaver 连接配置

### 连接信息

```
数据库类型: PostgreSQL
主机地址: 192.168.1.6
端口: 5432
数据库名: npdb
用户名: yfguo
密码: npdb2024
```

### 在DBeaver中配置步骤

#### 1. 创建新连接

1. 打开 DBeaver
2. 点击菜单 **Database** → **New Database Connection**
3. 选择 **PostgreSQL**
4. 点击 **Next**

#### 2. 填写连接信息

在 **Main** 标签页中填写：

```
┌─────────────────────────────────────┐
│ Connection Settings                 │
├─────────────────────────────────────┤
│ Host:     192.168.1.6              │
│ Port:     5432                      │
│ Database: npdb                      │
│ Username: yfguo                     │
│ Password: npdb2024                  │
│                                     │
│ ☑ Save password                    │
└─────────────────────────────────────┘
```

#### 3. 下载驱动（首次连接）

1. 点击 **Test Connection** 按钮
2. 如果提示下载驱动，点击 **Download**
3. 等待驱动下载完成

#### 4. 测试连接

- 驱动下载完成后，再次点击 **Test Connection**
- 应该看到 "Connected" 成功消息
- 显示连接信息：
  ```
  Connected
  Server version: 16.3
  Driver version: 42.x.x
  ```

#### 5. 保存连接

1. 点击 **Finish** 保存连接
2. 连接会出现在左侧的 **Database Navigator** 中

---

## 数据库结构

连接成功后，您可以看到以下结构：

```
npdb
└── Schemas
    └── public
        ├── Tables (9张表)
        │   ├── natural_products              天然产物表
        │   ├── targets                       靶点表
        │   ├── bioactivity                   活性记录表
        │   ├── toxicity                      毒性记录表
        │   ├── bio_resources                 生物资源表
        │   ├── bio_resource_natural_products 生物资源-天然产物关联表
        │   ├── prescriptions                 处方表
        │   ├── prescription_resources        处方-生物资源关联表
        │   └── prescription_natural_products 处方-天然产物关联表
        │
        └── Views (4个视图)
            ├── v_natural_product_detail      天然产物详情视图
            ├── v_bio_resource_detail         生物资源详情视图
            ├── v_target_detail               靶点详情视图
            └── v_prescription_detail         处方详情视图
```

---

## DBeaver 常用操作

### 1. 查看表数据

- 右键点击表名 → **View Data** (或双击表名)
- 或按 `F3` 快捷键

### 2. 查看表结构

- 右键点击表名 → **View Table**
- 查看列、索引、外键、触发器等信息

### 3. 执行SQL查询

- 点击工具栏的 **SQL Editor** 按钮
- 或按 `Ctrl + ]` (Windows/Linux) 或 `Cmd + ]` (Mac)
- 输入SQL语句并按 `Ctrl + Enter` 执行

示例查询：
```sql
-- 查看天然产物数量
SELECT COUNT(*) FROM natural_products;

-- 查看天然产物详情（使用视图）
SELECT * FROM v_natural_product_detail LIMIT 10;

-- 查看活性数据
SELECT
    np.pref_name,
    t.target_name,
    b.activity_type,
    b.activity_value_std
FROM bioactivity b
JOIN natural_products np ON b.natural_product_id = np.id
JOIN targets t ON b.target_id = t.id
LIMIT 20;
```

### 4. 查看ER图（实体关系图）

- 右键点击 `public` schema → **View Diagram**
- 可以看到所有表之间的关系

### 5. 导出数据

- 右键点击表名 → **Export Data**
- 选择格式：CSV, Excel, JSON, SQL等
- 配置导出选项并执行

### 6. 导入数据

- 右键点击表名 → **Import Data**
- 选择数据文件
- 映射列并执行导入

---

## 网络连接说明

### 网络拓扑

```
桌面电脑 (172.16.90.9)
    │
    │ 通过局域网/路由器
    │
    ▼
服务器 (192.168.1.6:5432)
    │
    └── PostgreSQL npdb 数据库
```

### 连接要求

1. **网络可达性**: 确保桌面电脑能ping通服务器
   ```bash
   # 在桌面电脑的命令行中测试
   ping 192.168.1.6
   ```

2. **端口开放**: 5432端口需要开放
   ```bash
   # 在桌面电脑测试端口连通性
   telnet 192.168.1.6 5432
   # 或
   Test-NetConnection -ComputerName 192.168.1.6 -Port 5432
   ```

---

## 故障排查

### 问题1: 连接超时 (Connection timeout)

**可能原因:**
- 网络不通
- 防火墙阻止
- PostgreSQL未启动

**解决方法:**
```bash
# 在服务器上检查PostgreSQL状态
pg_ctl status -D /home/yfguo/postgres_data

# 检查端口监听
netstat -tlnp | grep 5432

# 应该看到: 0.0.0.0:5432
```

### 问题2: 认证失败 (Authentication failed)

**可能原因:**
- 密码错误
- pg_hba.conf配置问题

**解决方法:**
```bash
# 重置密码
psql -U yfguo -d npdb -c "ALTER USER yfguo WITH PASSWORD 'new_password';"

# 检查pg_hba.conf
cat /home/yfguo/postgres_data/pg_hba.conf | grep 172.16.90
```

### 问题3: 数据库不存在 (Database does not exist)

**解决方法:**
- 确认数据库名称拼写正确: `npdb` (全小写)
- 或在DBeaver中查看可用数据库列表

### 问题4: 驱动下载失败

**解决方法:**
- 检查网络连接
- 手动下载PostgreSQL JDBC驱动: https://jdbc.postgresql.org/
- 在DBeaver中手动添加驱动: **Database** → **Driver Manager**

---

## 安全建议

### 生产环境建议

1. **使用强密码**
   ```sql
   ALTER USER yfguo WITH PASSWORD 'your_strong_password_here';
   ```

2. **限制访问IP**
   - 在 `pg_hba.conf` 中只允许特定IP访问
   - 不要使用 `0.0.0.0/0` (允许所有IP)

3. **启用SSL连接**
   ```bash
   # 在postgresql.conf中启用SSL
   ssl = on
   ssl_cert_file = 'server.crt'
   ssl_key_file = 'server.key'
   ```

4. **定期备份**
   ```bash
   # 备份数据库
   pg_dump -U yfguo npdb > npdb_backup_$(date +%Y%m%d).sql
   ```

---

## 配置文件位置

```
PostgreSQL数据目录: /home/yfguo/postgres_data/
├── postgresql.conf    主配置文件
├── pg_hba.conf       访问控制配置
├── pg_ident.conf     用户映射配置
└── logfile           日志文件
```

---

## 联系信息

- 服务器IP: 192.168.1.6
- 数据库: npdb
- 用户: yfguo
- 端口: 5432

---

**配置完成时间**: 2026-01-29
**PostgreSQL版本**: 16.3
**数据库表数量**: 9张表 + 4个视图
