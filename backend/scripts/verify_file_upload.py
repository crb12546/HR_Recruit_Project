"""验证文件上传功能"""
import os
import requests

def test_file_upload():
    """测试文件上传功能"""
    base_url = "http://localhost:8000"
    
    print("测试文件上传功能...")
    
    # 测试TXT文件上传
    with open("backend/tests/fixtures/resumes/senior_python_engineer.txt", "rb") as f:
        response = requests.post(
            f"{base_url}/api/v1/resumes/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )
        print("\nTXT文件上传结果:", response.json())
        
    # 测试DOCX文件上传
    with open("backend/tests/fixtures/resumes/fullstack_expert.docx", "rb") as f:
        response = requests.post(
            f"{base_url}/api/v1/resumes/upload",
            files={"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
        print("\nDOCX文件上传结果:", response.json())
    
    # 测试大文件限制
    print("\n测试大文件限制...")
    with open("/dev/zero", "rb") as f:
        large_content = f.read(101 * 1024 * 1024)  # 101MB
        response = requests.post(
            f"{base_url}/api/v1/resumes/upload",
            files={"file": ("large.pdf", large_content, "application/pdf")}
        )
        print("大文件上传结果:", response.json())

if __name__ == "__main__":
    test_file_upload()
