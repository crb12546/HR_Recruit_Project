"""验证服务集成状态"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from app.services.ocr import OCRService
from app.services.gpt import GPTService
from app.services.storage import StorageService
from app.services.mock_ocr import MockOCRService
from app.services.mock_gpt import MockGPTService
from app.services.mock_storage import MockStorageService

def verify_ocr_service():
    """验证OCR服务"""
    print("正在验证OCR服务...")
    try:
        if os.getenv("ENV") == "test":
            ocr = MockOCRService()
        else:
            ocr = OCRService()
        
        # 测试文本提取
        test_content = "测试简历内容".encode('utf-8')
        result = ocr.extract_text(test_content)
        print(f"OCR服务测试结果: {result}")
        return True
    except Exception as e:
        print(f"OCR服务验证失败: {str(e)}")
        return False

def verify_gpt_service():
    """验证GPT服务"""
    print("正在验证GPT服务...")
    try:
        if os.getenv("ENV") == "test":
            gpt = MockGPTService()
        else:
            gpt = GPTService()
        
        # 测试标签提取
        test_text = "熟练掌握Python, FastAPI, Vue.js等技术栈"
        tags = gpt.extract_resume_tags(test_text)
        print(f"GPT服务测试结果: {tags}")
        return True
    except Exception as e:
        print(f"GPT服务验证失败: {str(e)}")
        return False

def verify_storage_service():
    """验证存储服务"""
    print("正在验证存储服务...")
    try:
        if os.getenv("ENV") == "test":
            storage = MockStorageService()
        else:
            storage = StorageService()
        
        # 测试文件上传
        test_content = "测试文件内容".encode('utf-8')
        file_url = storage.upload_file(test_content, "test.txt")
        print(f"存储服务测试结果: {file_url}")
        return True
    except Exception as e:
        print(f"存储服务验证失败: {str(e)}")
        return False

def main():
    """主函数"""
    services = [
        ("OCR服务", verify_ocr_service),
        ("GPT服务", verify_gpt_service),
        ("存储服务", verify_storage_service)
    ]
    
    all_passed = True
    for name, verify_func in services:
        print(f"\n开始验证{name}...")
        if verify_func():
            print(f"{name}验证通过 ✓")
        else:
            print(f"{name}验证失败 ✗")
            all_passed = False
    
    if all_passed:
        print("\n所有服务验证通过 ✓")
        sys.exit(0)
    else:
        print("\n部分服务验证失败 ✗")
        sys.exit(1)

if __name__ == "__main__":
    main()
