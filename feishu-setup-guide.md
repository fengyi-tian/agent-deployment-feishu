# 飞书（Feishu）接入 OpenClaw 部署指南

> **作者：** 田田  
> **日期：** 2026-05-21  
> **环境：** OpenClaw 2026.5.19 / Linux

---

## 一、概述

本文档记录了将 OpenClaw AI Agent 接入飞书（Feishu/Lark）IM 平台的完整步骤，包含插件安装、飞书开放平台配置、权限开通、事件订阅及用户授权等环节。

---

## 二、环境准备

```bash
# 检查 OpenClaw 版本
openclaw --version

# 检查网关运行状态
openclaw gateway status
```

确保 OpenClaw 已正确安装并运行。

---

## 三、安装飞书插件

```bash
# 安装飞书官方插件
openclaw plugins install "@openclaw/feishu"

# 重启网关加载插件
openclaw gateway restart
```

---

## 四、飞书开放平台配置

### 4.1 创建应用

1. 登录 [飞书开放平台](https://open.feishu.cn)
2. 点击 **「创建企业自建应用」**，填写应用名称（如"小宝"）
3. 进入应用详情页

### 4.2 获取凭证

进入 **「凭证与基础信息」**：
- 复制 **App ID**（格式：`cli_xxx`）
- 复制 **App Secret**

### 4.3 配置到 OpenClaw

```bash
openclaw config set channels.feishu.appId "你的App ID"
openclaw config set channels.feishu.appSecret "你的App Secret"
```

### 4.4 开启机器人能力

左侧菜单 → **「应用功能」** → **「机器人」** → 开启开关并保存

### 4.5 配置权限

左侧菜单 → **「权限管理」** → **「开通权限」**，搜索并添加以下权限：

| 权限 | 用途 |
|------|------|
| `im:message` | 收发消息 |
| `im:message:send_as_bot` | 以机器人身份发消息 |
| `im:message:P2P_msg` | 私聊消息 |
| `im:resource` | 图片/文件资源 |

### 4.6 配置事件订阅

左侧菜单 → **「事件与回调」** → **「添加事件」**：
- 搜索 `im.message.receive_v1` 并添加
- 订阅方式选择 **WebSocket**（默认）

### 4.7 发布应用

左侧菜单 → **「版本管理与发布」**：
1. 点击 **「创建版本」**
2. 填写版本号（如 `1.0.0`）和更新说明
3. 保存并 **「申请发布」**
4. 等待审核通过

---

## 五、重启并验证连接

```bash
# 重启网关
openclaw gateway restart

# 查看日志确认连接状态
openclaw logs --limit 50
```

成功标志：
```
feishu[default]: WebSocket client started
feishu[default]: bot open_id recovered: ou_xxx
```

---

## 六、用户授权

在飞书 App 中搜索机器人并发送消息，机器人会返回配对码：

```
Pairing code: HHXXXXXJ
```

管理员在命令行批准：

```bash
openclaw pairing approve feishu HHXXXXXJ
```

批准后即可正常对话。

---

## 七、验证效果

在飞书 App 中：
1. 搜索机器人名称
2. 发送消息（如"你好"）
3. 机器人回复 → ✅ 接入成功

---

## 八、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 搜不到机器人 | 应用未发布或未过审 | 检查版本管理中的发布状态 |
| 回复 "access not configured" | 未授权当前用户 | 执行 `openclaw pairing approve` |
| WebSocket 连接失败 | 事件订阅方式不对 | 确认选择 WebSocket 模式 |
| 权限报错 | 权限未开通或未生效 | 在开放平台确认权限已开通 |

---

## 九、总结

通过以上步骤，即可将 OpenClaw AI Agent 成功接入飞书平台，实现 IM 智能对话功能。该方案适用于个人学习及企业场景部署。

---

*更多关于 OpenClaw 的信息请参考 [OpenClaw 文档](https://docs.openclaw.ai)*
