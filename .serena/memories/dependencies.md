# MaxKB 依赖关系图谱

## 核心架构依赖

### 1. 技术栈依赖层次
```
前端层 (Vue.js 3.x)
├── Element Plus (UI组件)
├── Vite (构建工具)
├── TypeScript (类型系统)
└── Pinia (状态管理)

API层 (Django REST Framework)
├── Django 4.2.20 (Web框架)
├── drf-yasg (API文档)
└── django-filter (查询过滤)

业务逻辑层
├── LangChain 0.3.23 (LLM框架)
├── LangGraph 0.3.27 (工作流)
└── MCP 1.8.0 (模型协议)

数据存储层
├── PostgreSQL (关系数据库)
├── pgvector (向量扩展)
└── Redis (缓存，可选)

基础设施层
├── Celery (任务队列)
├── Docker (容器化)
└── Nginx (反向代理，可选)
```

## Python后端依赖分析

### 1. 核心框架依赖
- **Django生态系统**:
  - `django==4.2.20`: Web框架核心
  - `djangorestframework==3.16.0`: REST API框架
  - `django-filter==23.2`: 查询过滤
  - `django-apscheduler==0.6.2`: 任务调度
  - `django-celery-beat`: Celery集成

### 2. LLM和AI依赖
- **LangChain生态**:
  - `langchain==0.3.23`: 核心框架
  - `langchain-openai==0.3.12`: OpenAI集成
  - `langchain-anthropic==0.3.12`: Anthropic集成
  - `langchain-community==0.3.21`: 社区模型
  - `langchain-mcp-adapters==0.0.11`: MCP适配器
  - `langgraph==0.3.27`: 工作流图

### 3. 机器学习依赖
- **深度学习框架**:
  - `torch==2.6.0`: PyTorch核心
  - `sentence-transformers==4.0.2`: 句子嵌入
  - `transformers`: Hugging Face模型库
  
### 4. 数据库相关
- **PostgreSQL生态**:
  - `psycopg2-binary==2.9.10`: PostgreSQL驱动
  - pgvector扩展: 向量数据库功能

### 5. 文档处理依赖
- **文件格式支持**:
  - `pymupdf==1.24.9`: PDF处理
  - `python-docx==1.1.2`: Word文档
  - `openpyxl==3.1.5`: Excel处理
  - `xlwt==1.3.0`: Excel写入
  - `beautifulsoup4==4.13.3`: HTML解析

### 6. 第三方模型SDK
- **国内厂商**:
  - `qianfan==0.3.18`: 百度千帆
  - `dashscope==1.23.1`: 阿里云灵积
  - `zhipuai==2.1.5.20250410`: 智谱AI
  
- **国际厂商**:
  - `openai==1.72.0`: OpenAI官方SDK
  - `anthropic`: Claude模型

## 前端依赖分析

### 1. 核心框架
- **Vue.js生态**:
  - `vue==3.3.4`: 核心框架
  - `@vue/runtime-core`: 运行时核心
  - `vue-router`: 路由管理
  - `pinia==2.1.6`: 状态管理

### 2. 构建工具链
- **开发工具**:
  - `vite`: 现代构建工具
  - `@vitejs/plugin-vue`: Vue插件
  - `typescript`: TypeScript支持
  - `vue-tsc`: Vue类型检查

### 3. UI组件和样式
- **组件库**:
  - `element-plus==2.9.1`: 主要UI库
  - `@element-plus/icons-vue`: 图标库
  - `use-element-plus-theme`: 主题定制

### 4. 功能性依赖
- **编辑器和工具**:
  - `codemirror==6.0.1`: 代码编辑器
  - `md-editor-v3==4.16.7`: Markdown编辑器
  - `@logicflow/core==1.2.27`: 工作流设计器
  - `echarts==5.5.0`: 图表库

### 5. 工具库
- **通用工具**:
  - `lodash==4.17.21`: 工具函数库
  - `axios==1.8.3`: HTTP客户端
  - `moment==2.30.1`: 日期处理
  - `mitt==3.0.0`: 事件总线

## 模块间依赖关系

### 1. Django应用依赖
```
users (用户管理)
├── 被所有模块依赖 (用户认证)
└── 无外部应用依赖

common (公共工具)
├── 被所有模块依赖 (工具函数)
└── 依赖: users

setting (系统设置)
├── 被依赖: application, dataset
└── 依赖: users, common

dataset (数据集)
├── 被依赖: application, embedding
└── 依赖: users, common, setting

embedding (向量嵌入)
├── 被依赖: application
└── 依赖: dataset, setting, common

application (应用核心)
├── 系统顶层模块
└── 依赖: dataset, embedding, setting, users, common

function_lib (功能库)
├── 被依赖: application
└── 依赖: users, common
```

### 2. 外部服务依赖
- **必需服务**:
  - PostgreSQL数据库 (必需)
  - pgvector扩展 (向量搜索)

- **可选服务**:
  - Redis (缓存和会话)
  - Celery Worker (异步任务)
  - Nginx (反向代理)

### 3. 运行时依赖
- **Python环境**: 3.11+
- **Node.js环境**: 18+ (构建时)
- **系统依赖**: 
  - libpq-dev (PostgreSQL客户端)
  - 系统级别的图像/PDF处理库

## 版本兼容性矩阵

### 1. 核心依赖版本
| 组件 | 版本 | 兼容性说明 |
|------|------|------------|
| Python | 3.11.x | 严格版本要求 |
| Django | 4.2.20 | LTS版本，稳定 |
| Vue.js | 3.3.4 | 组合式API |
| PostgreSQL | 15.8+ | 需要pgvector支持 |
| Node.js | 18+ | 构建时需要 |

### 2. 依赖更新策略
- **安全更新**: 及时更新补丁版本
- **次要版本**: 定期评估和测试
- **主要版本**: 谨慎升级，充分测试
- **锁定策略**: 生产环境锁定具体版本