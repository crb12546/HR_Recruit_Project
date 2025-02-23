from typing import List, Dict
from sqlalchemy.orm import Session
from ..models.tag import Tag
from ..models.resume import Resume
from .gpt import GPTService

class TagService:
    def __init__(self, db: Session):
        self.db = db
        self.gpt = GPTService()

    def generate_resume_tags(self, resume: Resume) -> List[Dict[str, str]]:
        """
        为简历生成标签
        
        Args:
            resume: 简历对象
            
        Returns:
            List[Dict[str, str]]: 标签列表
        """
        if not resume.content:
            return []
            
        # 使用GPT-4生成标签
        tags = self.gpt.extract_resume_tags(resume.content)
        
        # 保存标签到数据库
        db_tags = []
        for tag_data in tags:
            tag = self.get_or_create_tag(tag_data["name"])
            if tag not in resume.tags:
                resume.tags.append(tag)
            db_tags.append(tag)
            
        self.db.commit()
        return [tag.to_dict() for tag in db_tags]

    def get_or_create_tag(self, name: str, category: str = "技能") -> Tag:
        """
        获取或创建标签
        
        Args:
            name: 标签名称
            category: 标签类别，默认为"技能"
            
        Returns:
            Tag: 标签对象
        """
        tag = self.db.query(Tag).filter(Tag.name == name).first()
        if not tag:
            tag = Tag(name=name, category=category)
            self.db.add(tag)
            self.db.commit()
            self.db.refresh(tag)
        return tag

    def get_tags_by_category(self, category: str) -> List[Tag]:
        """
        按类别获取标签
        
        Args:
            category: 标签类别
            
        Returns:
            List[Tag]: 标签列表
        """
        return self.db.query(Tag).filter(Tag.category == category).all()

    def merge_similar_tags(self, tag1: Tag, tag2: Tag) -> Tag:
        """
        合并相似的标签
        
        Args:
            tag1: 要保留的标签
            tag2: 要合并的标签
            
        Returns:
            Tag: 合并后的标签
        """
        # 将tag2的所有关联转移到tag1
        for resume in tag2.resumes:
            if tag1 not in resume.tags:
                resume.tags.append(tag1)
            resume.tags.remove(tag2)
            
        for job in tag2.jobs:
            if tag1 not in job.tags:
                job.tags.append(tag1)
            job.tags.remove(tag2)
            
        # 删除tag2
        self.db.delete(tag2)
        self.db.commit()
        return tag1
