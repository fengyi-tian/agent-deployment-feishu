# Ollama + Dify 本地部署指南

> **适用于面试的知识点与实操命令汇总**

---

## 一、Ollama — 本地大模型运行工具

### 1.1 什么是 Ollama

Ollama 是一个轻量级的大模型本地运行框架，支持一键下载和运行各种开源大模型（Qwen、LLaMA、ChatGLM、DeepSeek 等）。

**核心优势：**
- 一行命令安装，一行命令跑模型
- 自带 REST API，方便集成
- 支持 GPU 和 CPU 运行
- 模型管理简单（下载/删除/切换）

### 1.2 安装 Ollama

```bash
# 一键安装（Linux / macOS）
curl -fsSL https://ollama.com/install.sh | sh

# macOS 也可以用 Homebrew
brew install ollama
```

### 1.3 常用命令

```bash
# 启动 Ollama 服务
ollama serve

# 拉取模型（以 Qwen2.5 7B 为例）
ollama pull qwen2.5:7b

# 运行模型（交互式对话）
ollama run qwen2.5:7b

# 列出已下载的模型
ollama list

# 删除模型
ollama rm qwen2.5:7b

# 通过 API 调用（curl）
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "你好，请介绍一下自己"
}'
```

### 1.4 推荐模型

| 模型 | 大小 | 特点 | 适用场景 |
|------|------|------|---------|
| `qwen2.5:7b` | ~4GB | 阿里通义千问，中文优秀 | 日常对话、中文任务 |
| `qwen2.5:1.5b` | ~1GB | 轻量版 | 资源有限的机器 |
| `llama3.2:3b` | ~2GB | Meta 出品，英文好 | 英文任务 |
| `deepseek-r1:7b` | ~4.5GB | 推理能力强 | 逻辑推理、代码 |
| `glm4:9b` | ~5GB | 智谱 ChatGLM | 中文综合任务 |

### 1.5 面试常问题

> **Q: Ollama 和普通模型推理有什么区别？**
> A: Ollama 封装了模型下载、量化、推理、API 暴露的全流程，开发者只需 `ollama run` 就能用，不用关心底层环境配置。

> **Q: 服务器没有 GPU 能跑吗？**
> A: 可以。Ollama 支持纯 CPU 推理，只是速度较慢。生产环境推荐 GPU 加速。

---

## 二、Dify — 低代码 AI 应用平台

### 2.1 什么是 Dify

Dify 是一个开源的 LLM 应用开发平台，提供了可视化的工作流编排、RAG 知识库、 Agent 构建等功能。

**核心功能：**
- 可视化 Prompt 编排
- RAG（检索增强生成）知识库
- 多模型支持（OpenAI、Ollama、Qwen 等）
- API 发布
- Chatflow / Workflow 两种模式

### 2.2 Docker 部署

```bash
# 前提：安装 Docker 和 Docker Compose

# 克隆 Dify 项目
git clone https://github.com/langgenius/dify.git
cd dify/docker

# 配置环境变量
cp .env.example .env

# 启动所有服务（首次会拉取镜像）
docker compose up -d

# 查看运行状态
docker compose ps

# 停止
docker compose down
```

### 2.3 访问 Dify

启动后浏览器访问：`http://localhost:3001`

首次使用需注册管理员账号。

### 2.4 连接 Ollama 到 Dify

在 Dify 中：
1. 进入 **设置 → 模型供应商**
2. 找到 **Ollama**，点击"添加模型"
3. 填写：
   - **模型名称：** `qwen2.5:7b`
   - **服务器 URL：** `http://<你的服务器IP>:11434`
4. 保存后即可在应用中使用本地模型

### 2.5 创建第一个 AI 应用

1. 点击 **"创建应用"**
2. 选择 **"对话型应用"**
3. 在 Prompt 编辑器中写系统提示词
4. 选择模型（刚配置的 Ollama 模型）
5. 发布 → 获得 API 或直接在线体验

### 2.6 面试常问题

> **Q: Dify 和 LangChain 有什么区别？**
> A: LangChain 是一个开发框架，需要写代码；Dify 是可视化平台，拖拽配置即可。Dify 底层也可以集成 LangChain。

> **Q: RAG 是什么？**
> A: Retrieval-Augmented Generation（检索增强生成），把外部知识文档切分、向量化存入数据库，用户提问时先检索相关文档片段，再让模型基于这些内容回答，解决大模型"不知道"的问题。

---

## 三、完整技术栈总结

### 3.1 架构图

```
用户（飞书/钉钉/企微）
       ↓
   OpenClaw（Agent 框架）
       ↓
   Dify（应用编排平台）
       ↓
   Ollama（模型运行时）
       ↓
   Qwen/ChatGLM/DeepSeek（开源大模型）
```

### 3.2 各层职责

| 层 | 工具 | 职责 |
|----|------|------|
| IM 接入层 | OpenClaw + 插件 | 连接飞书/钉钉/企微 |
| Agent 层 | OpenClaw | 对话管理、工具调用 |
| 应用编排层 | Dify | Prompt 管理、RAG 知识库、工作流 |
| 模型运行时 | Ollama | 模型推理、API 暴露 |
| 基础模型 | Qwen/LLaMA/GLM | 实际的语言理解与生成 |

### 3.3 一句话总结

> **OpenClaw 做 IM 接入和 Agent 调度，Dify 做应用编排和知识管理，Ollama 做模型推理，三层协同构成完整的企业级 AI 应用链路。**

---

## 四、在家自己练的环境要求

| 工具 | 最低配置 | 推荐配置 |
|------|---------|---------|
| OpenClaw | 2C4G | 4C8G |
| Dify | 4C8G + 20GB 磁盘 | 8C16G |
| Ollama (7B 模型) | 8GB 内存（CPU） | 4GB VRAM（GPU） |
| Ollama (1.5B 模型) | 4GB 内存 | 2GB VRAM |

建议：先用个人电脑（Mac/Win/Linux）本地跑轻量模型（1.5B/3B）练手，熟悉了再上服务器。
