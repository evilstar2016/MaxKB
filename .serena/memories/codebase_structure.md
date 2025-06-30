# MaxKB 代码库结构分析

## 项目根目录结构
```
MaxKB/
├── apps/                    # Django应用目录
├── ui/                      # Vue.js前端项目
├── installer/               # Docker部署配置
├── locales/                 # 国际化语言文件
├── main.py                  # 主入口文件
├── pyproject.toml          # Python项目配置
├── config_example.yml      # 配置文件模板
└── README.md               # 项目文档
```

## 后端应用架构 (apps/)

### 核心应用模块
1. **smartdoc/** - Django项目配置
   - settings/: 环境配置文件
   - urls.py: 路由配置
   - wsgi.py/asgi.py: WSGI/ASGI应用

2. **application/** - 应用管理核心
   - chat_pipeline/: 对话管道处理框架
   - flow/: 工作流引擎实现
   - migrations/: 数据库迁移文件
   - serializers/: DRF序列化器
   - views/: API视图控制器

3. **dataset/** - 知识库数据管理
   - models/: 数据集、文档、段落模型
   - serializers/: 数据处理序列化器
   - views/: 数据集CRUD操作
   - task/: 异步任务处理

4. **embedding/** - 向量嵌入系统
   - vector/: 向量存储实现
   - task/: 嵌入任务处理
   - models/: 嵌入相关模型

5. **setting/** - 系统配置管理
   - models_provider/: 模型提供商接口
   - migrations/: 设置相关迁移
   - serializers/: 配置序列化器

6. **function_lib/** - 功能函数库
   - 自定义函数管理
   - Python代码执行沙箱

7. **users/** - 用户权限系统
   - 用户认证和授权
   - 团队成员管理

8. **common/** - 公共工具模块
   - auth/: 认证处理
   - cache/: 缓存系统
   - chunk/: 文本分块处理
   - handle/: 文件处理器
   - util/: 工具函数集

## 前端项目架构 (ui/)

### Vue.js项目结构
```
ui/
├── src/
│   ├── api/                # API接口定义
│   ├── components/         # 可复用组件
│   ├── views/              # 页面视图组件
│   ├── stores/             # Pinia状态管理
│   ├── router/             # Vue Router路由
│   ├── utils/              # 工具函数
│   ├── styles/             # 样式文件
│   └── workflow/           # 工作流相关组件
├── public/                 # 静态资源
├── package.json           # NPM依赖配置
└── vite.config.ts         # Vite构建配置
```

## 数据库设计
- **PostgreSQL**: 主数据库，存储应用数据
- **pgvector扩展**: 向量数据存储和相似度搜索
- **表结构**: 通过Django ORM管理，包含：
  - 应用(Application)表
  - 数据集(Dataset)表
  - 文档(Document)表
  - 段落(Paragraph)表
  - 嵌入(Embedding)表
  - 用户(User)表
  - 模型(Model)表

## 关键设计模式

### 1. 管道模式 (Pipeline Pattern)
- chat_pipeline/: 聊天处理管道
- step/: 各个处理步骤实现
- 支持步骤组合和扩展

### 2. 工厂模式 (Factory Pattern)
- models_provider/: 模型提供商工厂
- 支持多种LLM提供商的统一接口

### 3. 策略模式 (Strategy Pattern)
- handle/: 不同文件类型处理策略
- chunk/: 不同文本分块策略

### 4. 观察者模式 (Observer Pattern)
- event/: 事件监听和处理
- task/: 异步任务通知

## 模块间依赖关系
- application → dataset (数据集关联)
- application → setting (模型配置)
- embedding → dataset (向量化处理)
- function_lib → common (工具函数)
- 所有模块 → users (用户认证)

## 配置管理
- config_example.yml: 配置模板
- smartdoc/conf.py: 配置管理器
- 支持环境变量和文件配置