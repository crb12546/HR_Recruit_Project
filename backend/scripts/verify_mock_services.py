"""验证模拟服务配置"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.mock_gpt import MockGPTService
from app.services.mock_ocr import MockOCRService
from app.services.mock_storage import MockStorageService
from app.services.mock_tag import MockTagService

def verify_mock_services():
    """验证所有模拟服务"""
    print('验证模拟服务配置...')
    
    # 初始化服务
    gpt = MockGPTService()
    ocr = MockOCRService()
    storage = MockStorageService()
    tag = MockTagService()
    print('✓ 所有模拟服务导入成功')

    # 测试GPT服务
    text = '5年Python开发经验'
    portrait = gpt.generate_talent_portrait(text)
    print(f'✓ GPT服务测试成功: {portrait}')

    # 测试OCR服务
    ocr_text = ocr.extract_text(b'test content')
    print(f'✓ OCR服务测试成功: {ocr_text}')

    # 测试存储服务
    file_url = storage.upload_file(b'test content', 'test.pdf')
    print(f'✓ 存储服务测试成功: {file_url}')

    # 测试标签服务
    tags = tag.generate_resume_tags(None)
    print(f'✓ 标签服务测试成功: {tags}')

if __name__ == '__main__':
    verify_mock_services()
