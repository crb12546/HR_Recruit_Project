from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any, Optional
import logging

from ..database import get_db
from ..models.resume import Resume
from ..models.tag import Tag
from ..services.service_factory import get_ocr_service, get_storage_service, get_gpt_service
from ..services.tag import create_or_get_tags
from ..utils.db_utils import safe_commit

router = APIRouter(prefix="/api/v1/resumes", tags=["resumes"])

logger = logging.getLogger("hr_recruitment")

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    candidate_name: str = Form(...),
    db: Session = Depends(get_db)
):
    """上传简历文件并解析"""
    logger.info(f"上传简历: {candidate_name}, 文件: {file.filename}")
    
    try:
        # 验证文件类型
        allowed_extensions = ["pdf", "doc", "docx", "jpg", "jpeg", "png"]
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件类型: {file_extension}，支持的类型: {', '.join(allowed_extensions)}"
            )
        
        # 获取服务实例
        storage_service = get_storage_service()
        ocr_service = get_ocr_service()
        gpt_service = get_gpt_service()
        
        # 上传文件到存储服务
        file_content = await file.read()
        file_url = storage_service.upload_file(file_content, file.filename)
        file_type = file_extension
        
        # 使用OCR服务提取文本
        ocr_content = ocr_service.extract_text_from_file(file_url)
        if not ocr_content:
            logger.warning(f"OCR提取文本为空: {file.filename}")
            ocr_content = "无法提取文本内容"
        
        # 使用GPT服务解析简历内容
        parsed_content = gpt_service.parse_resume(ocr_content)
        
        # 生成人才画像
        talent_portrait = gpt_service.generate_talent_portrait(parsed_content)
        
        # 创建简历记录
        resume = Resume(
            candidate_name=candidate_name,
            file_url=file_url,
            file_type=file_type,
            ocr_content=ocr_content,
            parsed_content=parsed_content,
            talent_portrait=talent_portrait
        )
        
        # 提取技能标签并关联
        if parsed_content and "skills" in parsed_content:
            skills = parsed_content["skills"]
            tags = create_or_get_tags(db, skills)
            resume.tags = tags
        
        # 保存到数据库
        db.add(resume)
        if not safe_commit(db, "保存简历失败"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="数据库保存失败"
            )
        
        db.refresh(resume)
        
        # 记录成功创建
        logger.info(f"成功上传简历: ID={resume.id}, 候选人={resume.candidate_name}")
        
        return {
            "message": "简历上传成功",
            "resume_id": resume.id,
            "candidate_name": resume.candidate_name,
            "file_url": resume.file_url,
            "tags": [tag.name for tag in resume.tags]
        }
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"简历上传失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"简历上传失败: {str(e)}"
        )

@router.get("", response_model=Dict[str, Any])
def get_resumes(request: Request, db: Session = Depends(get_db)):
    """获取所有简历列表"""
    logger.info("获取简历列表")
    
    try:
        resumes = db.query(Resume).all()
        return {
            "total": len(resumes),
            "resumes": [resume.to_dict() for resume in resumes]
        }
    except SQLAlchemyError as e:
        logger.error(f"获取简历列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库查询失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取简历列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取简历列表失败: {str(e)}"
        )

@router.get("/{resume_id}", response_model=Dict[str, Any])
def get_resume(resume_id: int, request: Request, db: Session = Depends(get_db)):
    """获取简历详情"""
    logger.info(f"获取简历详情: {resume_id}")
    
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"简历不存在: {resume_id}"
            )
        
        return resume.to_dict()
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"获取简历详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库查询失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"获取简历详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取简历详情失败: {str(e)}"
        )

@router.delete("/{resume_id}", status_code=status.HTTP_200_OK)
def delete_resume(resume_id: int, request: Request, db: Session = Depends(get_db)):
    """删除简历"""
    logger.info(f"删除简历: {resume_id}")
    
    try:
        # 查询简历
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"简历不存在: {resume_id}"
            )
        
        # 删除存储中的文件
        try:
            storage_service = get_storage_service()
            storage_service.delete_file(resume.file_url)
        except Exception as e:
            logger.warning(f"删除文件失败: {str(e)}")
        
        # 删除数据库记录
        db.delete(resume)
        if not safe_commit(db, "删除简历失败"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="数据库操作失败"
            )
        
        logger.info(f"成功删除简历: ID={resume_id}")
        
        return {"message": "简历删除成功"}
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"删除简历失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"删除简历失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除简历失败: {str(e)}"
        )
