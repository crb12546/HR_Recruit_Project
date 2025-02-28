"""标签服务"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.tag import Tag
from app.models.resume import Resume
from app.services.gpt import GPTService

class TagService:
    """标签服务实现"""
    
    def __init__(self, db: Session):
        self.db = db
        self.gpt_service = GPTService()
    
    def generate_resume_tags(self, resume: Resume) -> List[Dict[str, str]]:
        """生成简历标签"""
        # 使用GPT服务提取标签
        tag_dicts = self.gpt_service.extract_resume_tags(resume.ocr_content)
        
        # 处理标签，确保数据库中存在
        result_tags = []
        for tag_dict in tag_dicts:
            tag_name = tag_dict["name"]
            # 查找或创建标签
            tag = self.db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                self.db.add(tag)
                self.db.flush()  # 获取ID但不提交事务
            
            result_tags.append({"id": tag.id, "name": tag.name})
        
        return result_tags
    
    def get_all_tags(self) -> List[Dict[str, Any]]:
        """获取所有标签"""
        tags = self.db.query(Tag).all()
        return [tag.to_dict() for tag in tags]
    
    def get_tag_by_id(self, tag_id: int) -> Dict[str, Any]:
        """根据ID获取标签"""
        tag = self.db.query(Tag).filter(Tag.id == tag_id).first()
        if not tag:
            return None
        return tag.to_dict()
