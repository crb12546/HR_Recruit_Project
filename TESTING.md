# HR招聘系统测试环境

本文档描述了HR招聘系统的测试环境配置和使用方法。

## 测试环境架构

测试环境使用Docker Compose搭建，包含以下服务：

1. **数据库服务 (db)**：MySQL 8.0数据库，用于存储测试数据
2. **后端服务 (backend)**：Python FastAPI应用，运行在测试模式下
3. **前端服务 (frontend)**：Vue.js应用，运行在测试模式下

## 模拟服务

测试环境使用模拟服务替代实际的外部服务：

1. **OCR模拟服务**：替代阿里云OCR服务，用于文本提取
2. **存储模拟服务**：替代阿里云OSS存储服务，用于文件存储
3. **GPT模拟服务**：替代GPT-4服务，用于智能处理

## 测试数据

测试环境使用预定义的模拟数据：

1. **简历数据**：预定义的候选人简历
2. **职位数据**：预定义的招聘职位
3. **面试数据**：预定义的面试记录
4. **入职数据**：预定义的入职记录

## 运行测试

使用提供的脚本运行测试：

```bash
# 运行所有测试
./run_tests.sh

# 只运行单元测试
./run_tests.sh --tests=unit

# 只运行集成测试
./run_tests.sh --tests=integration

# 只运行端到端测试
./run_tests.sh --tests=e2e

# 只运行独立测试
./run_tests.sh --tests=standalone

# 运行特定测试文件
./run_tests.sh --tests=tests/unit/test_resume_management.py

# 不重新构建容器
./run_tests.sh --no-build

# 测试完成后不清理容器
./run_tests.sh --no-clean
```

## 测试环境配置

测试环境使用以下环境变量：

- `TESTING=True`：启用测试模式
- `MOCK_SERVICES=True`：使用模拟服务
- `DATABASE_URL`：数据库连接URL

## 添加新测试

在添加新测试时，请遵循以下规则：

1. 单元测试放在 `backend/tests/unit/` 目录下
2. 集成测试放在 `backend/tests/integration/` 目录下
3. 端到端测试放在 `backend/tests/e2e/` 目录下
4. 独立测试放在 `backend/tests/standalone/` 目录下
5. 测试文件名应以 `test_` 开头
6. 测试函数名应以 `test_` 开头

## 测试环境维护

定期维护测试环境：

1. 更新模拟数据
2. 清理测试数据库
3. 更新Docker镜像
