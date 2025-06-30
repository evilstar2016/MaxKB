# MaxKB 构建系统分析

## 后端构建系统

### 1. Python项目管理 (Poetry)
- **配置文件**: `pyproject.toml`
- **包管理器**: Poetry 1.8.5
- **Python版本**: >=3.11,<3.12
- **依赖管理**: 
  - 生产依赖和开发依赖分离
  - 版本锁定确保构建一致性

### 2. Django应用配置
- **框架版本**: Django 4.2.20
- **主要依赖**:
  - `djangorestframework`: API框架
  - `drf-yasg`: Swagger文档生成
  - `django-filter`: 查询过滤
  - `django-celery-beat`: 任务调度

### 3. 机器学习依赖
- **深度学习**: torch 2.6.0 (CPU版本)
- **嵌入模型**: sentence-transformers 4.0.2
- **向量搜索**: 集成pgvector
- **文本处理**: jieba 0.42.1 (中文分词)

## 前端构建系统

### 1. 构建工具链
- **构建工具**: Vite (现代化构建工具)
- **包管理器**: NPM
- **Node.js版本**: 18-alpine3.18
- **TypeScript**: 完整类型支持

### 2. 构建脚本
```json
{
  "dev": "vite",                    // 开发服务器
  "build": "run-p type-check build-only",  // 生产构建
  "build-only": "vite build",       // 仅构建
  "type-check": "vue-tsc --noEmit",  // 类型检查
  "preview": "vite preview"         // 预览构建结果
}
```

### 3. 构建优化
- **内存优化**: `--max_old_space_size=4096`
- **代码分割**: Vite自动代码分割
- **静态资源**: 自动压缩和版本控制

## Docker构建系统

### 1. 多阶段构建
```dockerfile
# 阶段1: 向量模型基础镜像
FROM ghcr.io/1panel-dev/maxkb-vector-model:v1.0.1 AS vector-model

# 阶段2: 前端构建
FROM node:18-alpine3.18 AS web-build
# 构建Vue.js应用

# 阶段3: Python环境构建
FROM ghcr.io/1panel-dev/maxkb-python-pg:python3.11-pg15.8 AS stage-build
# 安装Python依赖

# 阶段4: 最终运行镜像
FROM ghcr.io/1panel-dev/maxkb-python-pg:python3.11-pg15.8
# 组合所有组件
```

### 2. 基础镜像选择
- **Python基础**: `maxkb-python-pg:python3.11-pg15.8`
- **包含**: Python 3.11 + PostgreSQL 15.8 + pgvector
- **向量模型**: 预装嵌入模型镜像

### 3. 构建优化策略
- **层缓存**: 优化Docker层顺序
- **多架构支持**: x86_64和ARM64
- **体积优化**: 清理不必要文件

## 开发环境配置

### 1. 本地开发
- **后端**: Python虚拟环境 + Poetry
- **前端**: Node.js + Vite开发服务器
- **数据库**: PostgreSQL + pgvector扩展
- **缓存**: Redis (可选)

### 2. 环境变量配置
```yaml
# config.yml
DB_NAME: maxkb
DB_HOST: localhost
DB_PORT: 5432
DB_USER: root
DB_PASSWORD: xxxxxxx
DEBUG: false
TIME_ZONE: Asia/Shanghai
```

### 3. 开发工具
- **代码质量**: ESLint + Prettier (前端)
- **类型检查**: TypeScript + vue-tsc
- **API文档**: Swagger UI自动生成
- **测试**: Vitest (前端单元测试)

## 部署构建流程

### 1. CI/CD管道
- **代码检查**: Lint和类型检查
- **依赖安装**: Poetry install + npm install
- **应用构建**: Django collectstatic + Vite build
- **Docker构建**: 多阶段Docker构建
- **测试验证**: 单元测试和集成测试

### 2. 生产环境优化
- **静态文件**: CDN分发优化
- **数据库**: 连接池和索引优化
- **缓存策略**: Redis缓存层
- **负载均衡**: 支持多实例部署

### 3. 构建产物
- **后端**: Django应用 + Python依赖
- **前端**: 静态资源文件 (HTML/CSS/JS)
- **模型**: 预训练嵌入模型
- **配置**: 环境配置和启动脚本

## 依赖管理策略

### 1. 版本锁定
- **Python**: pyproject.toml锁定具体版本
- **Node.js**: package-lock.json锁定依赖树
- **Docker**: 使用具体标签而非latest

### 2. 安全更新
- **定期扫描**: 依赖安全漏洞检查
- **版本升级**: 渐进式依赖更新
- **兼容性测试**: 确保升级后功能正常

### 3. 构建缓存
- **Docker层缓存**: 优化构建速度
- **NPM缓存**: 加速前端依赖安装
- **Poetry缓存**: 复用Python包安装