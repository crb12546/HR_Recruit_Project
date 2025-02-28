# 端到端测试指南

## 测试环境配置

### 环境变量设置
```bash
export APP_ENV=testing
export SERVICE_MODE=mock
export TESTING=True
```

### 测试数据库
端到端测试使用内存数据库：
```python
DATABASE_URL = "sqlite:///:memory:"
```

## 端到端测试目录结构
```
backend/
  ├── tests/
  │   ├── e2e/
  │   │   ├── test_api_endpoints.py
  │   │   ├── test_recruitment_e2e.py
  │   │   └── ...
  │   └── ...
  └── ...
```

## 运行端到端测试
```bash
cd backend
python -m pytest tests/e2e/
```

## 测试API端点

### API端点测试示例
```python
def test_resume_api_endpoints(client, db, mock_services):
    """测试简历API端点"""
    # 创建测试简历
    resume_data = {
        "candidate_name": "张三",
        "file_url": "https://example.com/resume.pdf",
        "file_type": "pdf"
    }
    
    # 测试创建简历
    response = client.post("/api/v1/resumes", json=resume_data)
    assert response.status_code in [200, 201]
    data = response.json()
    assert "id" in data
    resume_id = data["id"]
    
    # 测试获取简历
    response = client.get(f"/api/v1/resumes/{resume_id}")
    assert response.status_code == 200
    assert response.json()["candidate_name"] == "张三"
    
    # 测试更新简历
    update_data = {"candidate_name": "张三（已更新）"}
    response = client.put(f"/api/v1/resumes/{resume_id}", json=update_data)
    assert response.status_code == 200
    
    # 测试获取简历列表
    response = client.get("/api/v1/resumes")
    assert response.status_code == 200
    assert len(response.json()["resumes"]) >= 1
    
    # 测试删除简历
    response = client.delete(f"/api/v1/resumes/{resume_id}")
    assert response.status_code == 200
    
    # 验证删除成功
    response = client.get(f"/api/v1/resumes/{resume_id}")
    assert response.status_code == 404
```

## 测试完整招聘流程

### 完整招聘流程测试示例
```python
def test_complete_recruitment_workflow(client, db, mock_services):
    """测试完整招聘流程"""
    # 步骤1：上传简历
    resume_data = {
        "candidate_name": "张三",
        "file_url": "https://example.com/resume.pdf",
        "file_type": "pdf"
    }
    response = client.post("/api/v1/resumes", json=resume_data)
    assert response.status_code in [200, 201]
    resume_id = response.json()["id"]
    
    # 步骤2：创建职位需求
    job_data = {
        "position_name": "Python高级工程师",
        "department": "技术部",
        "job_description": "负责后端系统开发和维护",
        "requirements": "5年以上Python开发经验，熟悉FastAPI框架",
        "status": "open"
    }
    response = client.post("/api/v1/jobs", json=job_data)
    assert response.status_code in [200, 201]
    job_id = response.json()["id"]
    
    # 步骤3：匹配简历与职位
    response = client.get(f"/api/v1/jobs/{job_id}/matches")
    assert response.status_code == 200
    matches = response.json()["matches"]
    
    # 步骤4：安排面试
    interview_data = {
        "resume_id": resume_id,
        "job_requirement_id": job_id,
        "interviewer_id": 1,  # 假设已有面试官
        "interview_time": "2023-06-01T10:00:00",
        "interview_type": "技术面试",
        "status": "scheduled"
    }
    response = client.post("/api/v1/interviews", json=interview_data)
    assert response.status_code in [200, 201]
    interview_id = response.json()["id"]
    
    # 步骤5：更新面试状态和反馈
    feedback_data = {
        "status": "completed",
        "feedback": "候选人技术能力强，沟通良好，建议录用",
        "evaluation_score": 85
    }
    response = client.put(f"/api/v1/interviews/{interview_id}", json=feedback_data)
    assert response.status_code == 200
    
    # 步骤6：创建入职流程
    onboarding_data = {
        "resume_id": resume_id,
        "job_requirement_id": job_id,
        "start_date": "2023-07-01",
        "status": "pending"
    }
    response = client.post("/api/v1/onboardings", json=onboarding_data)
    assert response.status_code in [200, 201]
    onboarding_id = response.json()["id"]
    
    # 步骤7：更新入职状态
    update_data = {"status": "completed"}
    response = client.put(f"/api/v1/onboardings/{onboarding_id}", json=update_data)
    assert response.status_code == 200
    
    # 验证整个流程
    response = client.get(f"/api/v1/onboardings/{onboarding_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
```

## 模拟服务

### 模拟服务配置
端到端测试使用模拟服务替代外部依赖：
```python
@pytest.fixture
def mock_services(monkeypatch):
    """提供模拟服务"""
    # 模拟GPT服务
    mock_gpt = MagicMock()
    mock_gpt.parse_resume.return_value = {"name": "张三", "skills": ["Python", "FastAPI"]}
    mock_gpt.generate_talent_portrait.return_value = "张三是一名Python开发工程师"
    mock_gpt.match_job_requirements.return_value = {
        "score": 85,
        "analysis": "候选人符合职位要求",
        "matching_points": ["技术技能匹配", "教育背景符合"],
        "missing_points": ["项目经验不足"]
    }
    
    # 模拟OCR服务
    mock_ocr = MagicMock()
    mock_ocr.extract_text.return_value = "姓名：张三\n技能：Python, FastAPI"
    
    # 模拟存储服务
    mock_storage = MagicMock()
    mock_storage.upload_file.return_value = "https://example.com/resume.pdf"
    
    # 应用模拟服务
    monkeypatch.setattr("app.services.service_factory.get_gpt_service", lambda: mock_gpt)
    monkeypatch.setattr("app.services.service_factory.get_ocr_service", lambda: mock_ocr)
    monkeypatch.setattr("app.services.service_factory.get_storage_service", lambda: mock_storage)
    
    return {
        "gpt": mock_gpt,
        "ocr": mock_ocr,
        "storage": mock_storage
    }
```

## 测试客户端

### 测试客户端配置
```python
@pytest.fixture
def client(app):
    """创建测试客户端"""
    with TestClient(app) as client:
        yield client
```

## 常见问题

### 数据库状态问题
如果测试失败，可能是由于数据库状态不一致。确保每个测试函数都使用独立的数据库会话。

### 模拟服务问题
如果测试失败，检查模拟服务是否正确配置和应用。确保模拟服务返回的数据格式与实际服务一致。

### 异步操作问题
如果测试涉及异步操作，确保正确等待异步操作完成。

## 最佳实践

1. 每个端到端测试应该测试完整的业务流程
2. 使用模拟服务替代外部依赖
3. 确保测试数据库在每次测试前重置
4. 测试应该独立且可重复执行
5. 测试失败时提供详细的错误信息
