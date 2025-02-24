# HR Recruitment Project

这是一个人力资源招聘管理系统项目。该系统旨在简化招聘流程，提高人才筛选效率。

## 环境配置

项目需要配置以下环境变量：

### 数据库配置
- `SQLALCHEMY_DATABASE_URL`: 数据库连接URL

### 阿里云配置
- `ALIYUN_ACCESS_KEY_ID`: 阿里云访问密钥ID
- `ALIYUN_ACCESS_KEY_SECRET`: 阿里云访问密钥密码
- `ALIYUN_OSS_BUCKET`: OSS存储桶名称
- `ALIYUN_OSS_ENDPOINT`: OSS服务端点
- `ALIYUN_REGION`: 阿里云地区

### OpenAI配置
- `OPENAI_API_KEY`: OpenAI API密钥

### 环境设置
- `ENV`: 运行环境 (development/test/production)
- `MOCK_SERVICES`: 是否使用模拟服务 (true/false)

请确保在运行项目前正确配置这些环境变量。

## 环境配置要求

项目运行需要配置以下环境变量：

### 数据库配置
- `DB_HOST`: 数据库主机地址
- `DB_PORT`: 数据库端口
- `DB_NAME`: 数据库名称
- `DB_USER`: 数据库用户名
- `DB_PASSWORD`: 数据库密码

### 阿里云配置
- `ALIYUN_ACCESS_KEY_ID`: 阿里云访问密钥ID
- `ALIYUN_ACCESS_KEY_SECRET`: 阿里云访问密钥密码
- `ALIYUN_OSS_BUCKET`: OSS存储桶名称
- `ALIYUN_OSS_ENDPOINT`: OSS服务端点
- `ALIYUN_REGION`: 阿里云地区

### OpenAI配置
- `OPENAI_API_KEY`: OpenAI API密钥

### 环境设置
- `ENV`: 运行环境 (development/test/production)
- `MOCK_SERVICES`: 是否使用模拟服务 (true/false)

请确保在运行项目前正确配置这些环境变量。不要将包含实际密钥的环境文件提交到代码仓库中。
