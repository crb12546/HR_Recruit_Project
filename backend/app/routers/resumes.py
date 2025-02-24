"""简历管理路由"""
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.resume import Resume
from app.models.tag import Tag
from app.services.ocr import OCRService
from app.services.gpt import GPTService
from app.services.tag import TagService
from app.services.storage import StorageService

router = APIRouter(prefix="/api/v1/resumes", tags=["resumes"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传单个简历文件"""
    try:
        content = await file.read()
        if len(content) > 100 * 1024 * 1024:  # 100MB
            raise HTTPException(status_code=400, detail="文件大小不能超过100MB")
            
        # 初始化服务
        storage_service = StorageService()
        ocr_service = OCRService()
        gpt_service = GPTService()
        tag_service = TagService(db)
        
        # 上传文件到OSS
        file_url = storage_service.upload_file(
            content,
            f"resumes/{file.filename}"
        )
        
        # OCR提取文本
        ocr_text = ocr_service.extract_text(content)
        
        # 生成人才画像和提取候选人姓名
        talent_portrait = gpt_service.generate_talent_portrait(ocr_text)
        candidate_name = gpt_service.extract_candidate_name(ocr_text)
        
        # 规范化文件类型
        file_type_map = {
            "application/pdf": "pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "application/msword": "doc",
            "text/plain": "txt",
            "application/vnd.ms-excel": "xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
            "application/octet-stream": "docx"  # 处理某些客户端发送的MIME类型
        }
        
        # 从文件名获取扩展名作为备选
        file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        ext_type_map = {
            'pdf': 'pdf',
            'docx': 'docx',
            'doc': 'doc',
            'txt': 'txt',
            'xls': 'xls',
            'xlsx': 'xlsx'
        }
        
        # 优先使用MIME类型，如果无法识别则使用文件扩展名
        file_type = file_type_map.get(file.content_type) or ext_type_map.get(file_ext)
        if not file_type:
            raise HTTPException(status_code=400, detail="不支持的文件格式")
            
        # 创建简历记录
        resume = Resume(
            candidate_name=candidate_name,
            file_url=file_url,
            file_type=file_type,
            ocr_content=ocr_text,
            talent_portrait=talent_portrait
        )
        
        # 生成标签
        tags = tag_service.generate_resume_tags(resume)
        
        # 保存到数据库
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        # 构建响应
        result = {
            "id": resume.id,
            "file_url": file_url,
            "file_type": file_type,
            "talent_portrait": talent_portrait,
            "candidate_name": candidate_name,
            "ocr_content": ocr_text,
            "tags": tags
        }
        
        return result
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"简历处理失败: {str(e)}"
        )

@router.post("/{resume_id}/parse")
async def parse_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """解析简历内容"""
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(status_code=404, detail="简历不存在")
            
        # 初始化服务
        gpt_service = GPTService()
        tag_service = TagService(db)
        
        # 生成标签
        tags = tag_service.generate_resume_tags(resume)
        
        # 更新简历
        resume.tags = [Tag(**tag) for tag in tags]
        db.commit()
        db.refresh(resume)
        
        return resume.to_dict()
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"简历解析失败: {str(e)}"
        )
