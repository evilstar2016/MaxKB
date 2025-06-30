# MaxKB 关键接口定义

## 核心API接口架构

### 1. 应用管理接口 (Application APIs)
- **基础路径**: `/api/application/`
- **主要接口**:
  - `GET /api/application/` - 获取应用列表
  - `POST /api/application/` - 创建新应用
  - `GET /api/application/{id}/` - 获取应用详情
  - `PUT /api/application/{id}/` - 更新应用配置
  - `DELETE /api/application/{id}/` - 删除应用

### 2. 聊天对话接口 (Chat APIs)
- **基础路径**: `/api/application/{app_id}/chat/`
- **主要接口**:
  - `POST /api/application/{app_id}/chat/` - 发起对话
  - `GET /api/application/{app_id}/chat/{chat_id}/` - 获取对话历史
  - **OpenAI兼容接口**: `/api/application/{app_id}/chat/completions`
  - **流式响应**: 支持Server-Sent Events (SSE)

### 3. 数据集管理接口 (Dataset APIs)
- **基础路径**: `/api/dataset/`
- **主要接口**:
  - `GET /api/dataset/` - 获取数据集列表
  - `POST /api/dataset/` - 创建数据集
  - `POST /api/dataset/{id}/document/` - 上传文档
  - `GET /api/dataset/{id}/document/` - 获取文档列表
  - `POST /api/dataset/{id}/sync/` - 同步Web文档

### 4. 模型管理接口 (Model APIs)
- **基础路径**: `/api/setting/model/`
- **主要接口**:
  - `GET /api/setting/model/` - 获取模型列表
  - `POST /api/setting/model/` - 添加模型
  - `PUT /api/setting/model/{id}/` - 更新模型配置
  - `POST /api/setting/model/{id}/valid/` - 验证模型连接

### 5. 用户认证接口 (Auth APIs)
- **基础路径**: `/api/user/`
- **主要接口**:
  - `POST /api/user/login/` - 用户登录
  - `POST /api/user/logout/` - 用户登出
  - `GET /api/user/profile/` - 获取用户信息
  - `POST /api/user/register/` - 用户注册

## 内部接口设计

### 1. 聊天管道接口 (Chat Pipeline Interface)
```python
class IBaseChatPipelineStep:
    def execute(self, chat_info, **kwargs):
        """执行管道步骤"""
        pass
    
    def get_details(self, **kwargs):
        """获取步骤详情"""
        pass
```

### 2. 模型提供商接口 (Model Provider Interface)
```python
class IModelProvider:
    def get_model_info_list(self):
        """获取支持的模型列表"""
        pass
    
    def get_model_credential(self, model_type):
        """获取模型凭证配置"""
        pass
    
    def is_valid_credential(self, credential):
        """验证凭证有效性"""
        pass
```

### 3. 向量存储接口 (Vector Store Interface)
```python
class BaseVectorStore:
    def save(self, text, source_id, dataset_id):
        """保存向量数据"""
        pass
    
    def query(self, text, dataset_id_list, **kwargs):
        """查询相似向量"""
        pass
    
    def delete_by_source_id(self, source_id):
        """删除向量数据"""
        pass
```

### 4. 文件处理接口 (File Handler Interface)
```python
class BaseSplitHandle:
    def handle(self, file):
        """处理文件并分割成段落"""
        pass
    
    def support(self, file_type):
        """检查是否支持该文件类型"""
        pass
```

### 5. 工作流节点接口 (Workflow Node Interface)
```python
class INode:
    def run(self, node_params, **kwargs):
        """执行节点逻辑"""
        pass
    
    def get_node_params_serializer_class(self):
        """获取节点参数序列化器"""
        pass
```

## API认证机制

### 1. Token认证
- **用户Token**: JWT格式，用于用户身份验证
- **应用API Key**: 用于第三方应用集成
- **访问令牌**: 临时访问令牌

### 2. 权限控制
- **角色权限**: Admin、User等角色
- **操作权限**: READ, WRITE, DELETE等
- **资源权限**: 基于资源所有权的访问控制

## 数据格式规范

### 1. 统一响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {...},
  "success": true
}
```

### 2. 分页响应格式
```json
{
  "current": 1,
  "size": 20,
  "total": 100,
  "records": [...]
}
```

### 3. 流式响应格式 (SSE)
```
data: {"type": "message", "content": "..."}
data: {"type": "end", "message_id": "..."}
```

## WebSocket接口
- **连接路径**: `/ws/chat/{chat_id}/`
- **消息类型**: text_message, image_message, file_message
- **实时通信**: 支持实时对话和状态更新