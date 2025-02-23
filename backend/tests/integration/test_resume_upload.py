import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
from sqlalchemy.orm import Session

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    # 创建测试数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 清理测试数据
    Base.metadata.drop_all(bind=engine)

def test_upload_pdf_resume(test_db):
    """测试上传PDF格式简历"""
    # 读取测试简历文件
    file_path = os.path.join(
        os.path.dirname(__file__),
        "../fixtures/resumes/senior_python_engineer.pdf"
    )
    with open(file_path, "rb") as f:
        files = {"file": ("高级Python工程师.pdf", f, "application/pdf")}
        response = client.post("/api/v1/resumes/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "tags" in data
    assert "talent_portrait" in data["resume"]

def test_upload_word_resume(test_db):
    """测试上传Word格式简历"""
    file_path = os.path.join(
        os.path.dirname(__file__),
        "../fixtures/resumes/fullstack_expert.docx"
    )
    with open(file_path, "rb") as f:
        files = {"file": ("全栈专家.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        response = client.post("/api/v1/resumes/upload", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "tags" in data
    assert "talent_portrait" in data["resume"]

def test_upload_invalid_file_type(test_db):
    """测试上传不支持的文件格式"""
    content = b"invalid file content"
    files = {"file": ("test.txt", content, "text/plain")}
    response = client.post("/api/v1/resumes/upload", files=files)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "不支持的文件格式"

def test_upload_large_file(test_db):
    """测试上传超大文件"""
    # 创建一个超过100MB的文件内容
    content = b"x" * (101 * 1024 * 1024)
    files = {"file": ("large.pdf", content, "application/pdf")}
    response = client.post("/api/v1/resumes/upload", files=files)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "文件大小不能超过100MB"

def test_batch_upload_resumes(test_db):
    """测试批量上传简历"""
    # 准备多个测试文件
    files = []
    test_files = [
        ("senior_python_engineer.pdf", "application/pdf"),
        ("fullstack_expert.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("data_engineer.pdf", "application/pdf")
    ]
    
    for filename, content_type in test_files:
        file_path = os.path.join(
            os.path.dirname(__file__),
            f"../fixtures/resumes/{filename}"
        )
        with open(file_path, "rb") as f:
            files.append(("files", (filename, f, content_type)))
    
    response = client.post("/api/v1/resumes/batch-upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert len(data["resumes"]) == len(test_files)
    
    # 验证每个简历都有标签和人才画像
    for resume in data["resumes"]:
        assert "tags" in resume
        assert "talent_portrait" in resume

def test_resume_parsing_error(test_db):
    """测试简历解析失败的情况"""
    # 创建一个损坏的PDF文件
    content = b"%PDF-1.7\x0d\x0ainvalid pdf content"
    files = {"file": ("corrupt.pdf", content, "application/pdf")}
    response = client.post("/api/v1/resumes/upload", files=files)
    
    assert response.status_code == 500
    assert "简历解析失败" in response.json()["detail"]
