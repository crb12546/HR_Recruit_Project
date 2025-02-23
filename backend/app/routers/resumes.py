from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.resume import Resume
from app.services.ocr import OCRService
from app.services.gpt import GPTService
from app.services.tag import TagService

router = APIRouter(prefix="/api/v1/resumes", tags=["resumes"])

@router.post("/{resume_id}/parse")
async def parse_resume(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    解析简历内容，生成标签和人才画像
    
    Args:
        resume_id: 简历ID
        db: 数据库会话
        
    Returns:
        dict: 包含解析结果的字典
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    
    # 初始化服务
    gpt_service = GPTService()
    tag_service = TagService(db)
    
    # 生成人才画像和标签
    resume.talent_portrait = gpt_service.generate_talent_portrait(resume.ocr_content)
    tags = tag_service.generate_resume_tags(resume)
    
    db.commit()
    db.refresh(resume)
    
    return resume.to_dict()

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传并解析简历
    
    Args:
        file: 简历文件
        db: 数据库会话
        
    Returns:
        dict: 包含解析结果的字典
    """
    try:
        # 读取文件内容
        content = await file.read()
        
        # 初始化服务
        ocr_service = OCRService()
        gpt_service = GPTService()
        tag_service = TagService(db)
        
        # OCR提取文本
        ocr_text = ocr_service.extract_text(content)
        
        # 生成人才画像
        talent_portrait = gpt_service.generate_talent_portrait(ocr_text)
        
        # 创建简历记录
        resume = Resume(
            candidate_name="候选人",  # 从OCR结果中提取
            file_url="test_url",  # 实际项目中应该上传到OSS
            file_type=file.content_type,
            ocr_content=ocr_text,
            talent_portrait=talent_portrait
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        # 生成标签
        tags = tag_service.generate_resume_tags(resume)
        
        return resume.to_dict()
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"简历处理失败: {str(e)}"
        )

@router.get("/{resume_id}/tags")
def get_resume_tags(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """
    获取简历标签
    
    Args:
        resume_id: 简历ID
        db: 数据库会话
        
    Returns:
        List[dict]: 标签列表
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
        
    return [tag.to_dict() for tag in resume.tags]

@router.post("/{resume_id}/tags/{tag_id}")
def add_resume_tag(
    resume_id: int,
    tag_id: int,
    db: Session = Depends(get_db)
):
    """
    手动添加简历标签
    
    Args:
        resume_id: 简历ID
        tag_id: 标签ID
        db: 数据库会话
        
    Returns:
        dict: 更新后的简历信息
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
        
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
        
    if tag not in resume.tags:
        resume.tags.append(tag)
        db.commit()
        db.refresh(resume)
        
    return resume.to_dict()
