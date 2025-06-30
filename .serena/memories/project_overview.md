# MaxKB 项目概述

## 项目简介
MaxKB = Max Knowledge Brain，是一个基于RAG（检索增强生成）技术的企业级AI助手平台。该项目旨在为企业提供智能客服、内部知识库、学术研究和教育等场景的AI解决方案。

## 项目目的
- **RAG管道**: 支持直接上传文档/自动爬取在线文档，具备自动文本分割、向量化功能，有效减少大模型幻觉，提供优质的智能问答交互体验
- **Agent工作流**: 配备强大的工作流引擎、函数库和MCP工具使用，能够编排AI流程以满足复杂业务场景需求
- **无缝集成**: 促进零代码快速集成到第三方业务系统，快速为现有系统配备智能问答能力，提升用户满意度
- **模型无关**: 支持各种大型模型，包括私有模型（如DeepSeek、Llama、Qwen等）和公共模型（如OpenAI、Claude、Gemini等）
- **多模态**: 原生支持输入输出文本、图像、音频和视频

## 技术栈描述

### 后端技术栈
- **核心框架**: Django 4.2.20 (Python Web框架)
- **Python版本**: Python 3.11
- **数据库**: PostgreSQL + pgvector (支持向量存储)
- **LLM框架**: LangChain 0.3.23
- **任务队列**: Celery + django-celery-beat
- **API文档**: drf-yasg (Swagger集成)
- **嵌入模型**: sentence-transformers, torch
- **多语言支持**: jieba (中文分词)
- **文档处理**: PyMuPDF, python-docx, xlwt, openpyxl
- **图像处理**: Pillow, rapidocr-onnxruntime
- **模型集成**: 支持OpenAI、Anthropic、Google Gemini、DeepSeek、阿里云、腾讯云等多种模型提供商

### 前端技术栈
- **核心框架**: Vue.js 3.3.4
- **构建工具**: Vite
- **UI组件库**: Element Plus 2.9.1
- **类型检查**: TypeScript
- **状态管理**: Pinia 2.1.6
- **工具库**: Lodash, Axios, moment
- **代码编辑器**: CodeMirror 6.0.1
- **图表库**: ECharts 5.5.0
- **Markdown编辑**: md-editor-v3 4.16.7
- **工作流设计**: LogicFlow 1.2.27

## 主要模块结构

### 应用模块 (apps/)
1. **application/**: 核心应用管理模块
   - chat_pipeline/: 聊天管道处理
   - flow/: 工作流引擎
   - models/: 数据模型定义
   - serializers/: API序列化器
   - views/: 视图控制器

2. **dataset/**: 数据集管理模块
   - 文档上传、处理、分割
   - 段落和问题管理
   - 图像和文件处理

3. **embedding/**: 向量嵌入模块
   - 文本向量化处理
   - 向量存储和检索

4. **setting/**: 系统设置模块
   - 模型提供商配置
   - 系统参数设置
   - 用户权限管理

5. **function_lib/**: 功能库模块
   - 自定义函数管理
   - Python代码执行环境

6. **users/**: 用户管理模块
   - 用户认证和授权
   - 团队管理

7. **common/**: 公共工具模块
   - 认证处理
   - 缓存管理
   - 中间件
   - 工具函数

## 关键特性
- **多模型支持**: 集成20+主流LLM提供商
- **RAG引擎**: 自动文档处理和向量化
- **工作流设计**: 可视化工作流编排
- **MCP工具集成**: 支持Model Context Protocol
- **多语言支持**: 中英文界面切换
- **Docker部署**: 容器化部署支持
- **API接口**: RESTful API和OpenAI兼容接口
- **权限控制**: 细粒度权限管理
- **实时通信**: WebSocket支持