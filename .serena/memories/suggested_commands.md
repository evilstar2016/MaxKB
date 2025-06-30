# MaxKB 项目开发建议命令

## 环境准备命令

### 1. Python环境配置
```bash
# 创建Python虚拟环境
python3.11 -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 激活虚拟环境 (Linux/macOS)
source venv/bin/activate

# 安装Poetry
pip install poetry==1.8.5

# 安装项目依赖
poetry install

# 配置Poetry不创建虚拟环境(如果已在虚拟环境中)
poetry config virtualenvs.create false
```

### 2. 前端环境配置
```bash
# 进入前端目录
cd ui

# 安装Node.js依赖
npm install

# 安装特定版本的依赖
npm ci

# 更新依赖
npm update
```

### 3. 数据库配置
```bash
# 创建PostgreSQL数据库
createdb maxkb

# 安装pgvector扩展
psql -d maxkb -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 运行数据库迁移
python apps/manage.py migrate

# 创建超级用户
python apps/manage.py createsuperuser
```

## 开发运行命令

### 1. 后端开发服务器
```bash
# 启动Django开发服务器
python main.py start --services all

# 仅启动web服务
python main.py start --services gunicorn

# 启动Celery worker
python main.py start --services celery

# 使用Django manage.py
cd apps && python manage.py runserver

# 收集静态文件
python main.py collectstatic

# 数据库迁移
python main.py migrate
```

### 2. 前端开发服务器
```bash
# 启动Vite开发服务器
cd ui && npm run dev

# 构建生产版本
cd ui && npm run build

# 预览构建结果
cd ui && npm run preview

# 类型检查
cd ui && npm run type-check

# 代码格式化
cd ui && npm run format

# ESLint检查
cd ui && npm run lint
```

### 3. Docker开发环境
```bash
# 构建Docker镜像
docker build -t maxkb:dev -f installer/Dockerfile .

# 运行Docker容器
docker run -d --name maxkb-dev -p 8080:8080 \
  -v ~/.maxkb:/var/lib/postgresql/data \
  -v ~/.python-packages:/opt/maxkb/app/sandbox/python-packages \
  maxkb:dev

# 查看容器日志
docker logs -f maxkb-dev

# 进入容器调试
docker exec -it maxkb-dev bash
```

## 测试和质量控制

### 1. 后端测试
```bash
# 运行Django测试
cd apps && python manage.py test

# 运行特定应用测试
cd apps && python manage.py test application

# 代码覆盖率测试
cd apps && coverage run manage.py test
cd apps && coverage report
```

### 2. 前端测试
```bash
# 运行单元测试
cd ui && npm run test:unit

# 运行测试并观察文件变化
cd ui && npm run test:unit -- --watch

# 运行测试覆盖率
cd ui && npm run test:unit -- --coverage
```

### 3. 代码质量检查
```bash
# Python代码格式化 (如果使用black)
black apps/

# Python代码检查 (如果使用flake8)
flake8 apps/

# 前端代码格式化
cd ui && npm run format

# 前端代码检查
cd ui && npm run lint
```

## 数据库管理命令

### 1. 迁移管理
```bash
# 创建迁移文件
cd apps && python manage.py makemigrations

# 应用迁移
cd apps && python manage.py migrate

# 查看迁移状态
cd apps && python manage.py showmigrations

# 回滚迁移
cd apps && python manage.py migrate application 0001

# 生成SQL语句
cd apps && python manage.py sqlmigrate application 0001
```

### 2. 数据管理
```bash
# 导出数据
cd apps && python manage.py dumpdata > backup.json

# 导入数据
cd apps && python manage.py loaddata backup.json

# 清空数据库
cd apps && python manage.py flush

# 重置数据库
cd apps && python manage.py reset_db
```

## 部署和生产命令

### 1. 生产构建
```bash
# 构建前端
cd ui && npm run build

# 收集静态文件
python main.py collectstatic --noinput

# 压缩静态文件
python main.py compress

# 检查部署配置
cd apps && python manage.py check --deploy
```

### 2. 服务管理
```bash
# 启动所有服务
python main.py start --services all

# 停止服务
python main.py stop

# 重启服务
python main.py restart

# 查看服务状态
python main.py status

# 后台运行
python main.py start --services all --daemon
```

### 3. 日志和监控
```bash
# 查看应用日志
tail -f logs/maxkb.log

# 查看Celery日志
tail -f logs/celery.log

# 查看错误日志
tail -f logs/error.log

# 查看访问日志
tail -f logs/access.log
```

## 常用工具命令

### 1. Windows系统命令
```cmd
# 查看端口占用
netstat -ano | findstr :8080

# 杀死进程
taskkill /F /PID <进程ID>

# 查看Python进程
wmic process where "name='python.exe'" get ProcessId,CommandLine

# 设置环境变量
set DJANGO_SETTINGS_MODULE=smartdoc.settings
```

### 2. Git版本控制
```bash
# 克隆项目
git clone https://github.com/1Panel-dev/MaxKB.git

# 查看状态
git status

# 提交更改
git add .
git commit -m "feat: add new feature"

# 推送到远程
git push origin main

# 拉取最新代码
git pull origin main
```

### 3. 性能分析
```bash
# 查看Django SQL查询
cd apps && python manage.py shell
>>> from django.db import connection
>>> print(connection.queries)

# 性能分析
cd apps && python manage.py runprofileserver

# 内存使用分析
cd apps && python -m memory_profiler manage.py runserver
```