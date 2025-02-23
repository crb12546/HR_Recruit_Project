from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
import os

def create_resume(filename, content):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # 设置中文字体
    c.setFont("Helvetica", 12)
    
    # 写入内容
    y = height - inch
    for line in content.split('\n'):
        if not line.strip():
            y -= 12
            continue
        if line.startswith('个人简历'):
            c.setFont("Helvetica-Bold", 18)
            c.drawString(width/2 - 50, y, line)
            c.setFont("Helvetica", 12)
        elif any(line.startswith(section) for section in ['基本信息', '教育背景', '工作经验', '专业技能', '项目经验', '证书', '自我评价']):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(inch, y, line)
            c.setFont("Helvetica", 12)
        else:
            c.drawString(inch, y, line)
        y -= 14
        if y < inch:
            c.showPage()
            y = height - inch
    
    c.save()

# 数据工程师简历内容
content = """个人简历

基本信息
姓名：吴海峰
性别：男
年龄：32岁
电话：136xxxx9012
邮箱：wuhf@example.com
现居地：上海市浦东新区

教育背景
2011-2015  复旦大学
统计学 | 本科
2015-2017  同济大学
数据科学 | 硕士

工作经验
2021-至今  阿里云
高级数据工程师
• 负责数据仓库架构设计和优化
• 使用Python和Spark开发数据处理管道
• 优化数据处理性能，提升效率200%
• 指导团队进行ETL开发

2017-2021  携程旅行网
数据工程师
• 设计实现用户行为分析平台
• 开发实时数据处理系统
• 构建机器学习特征工程流水线
• 优化数据warehouse架构

专业技能
• 编程语言：Python (6年)，Scala，SQL
• 大数据技术：Spark，Hadoop，Hive
• 数据仓库：Snowflake，Redshift
• 流处理：Kafka，Flink，Storm
• 数据库：PostgreSQL，MongoDB
• 云平台：阿里云，AWS

项目经验
阿里云数据湖平台（2022-2023）
• 设计实现数据湖架构
• 开发Python/Spark数据处理框架
• 实现实时和批处理双模式
• 日处理数据量达到PB级

携程用户画像系统（2019-2021）
• 设计用户特征工程框架
• 开发实时特征计算系统
• 构建用户行为分析模型
• 支持千万级用户分析

证书
• 阿里云数据分析专家认证
• AWS高级数据工程师认证
• Databricks Spark开发者认证
• CFA二级

自我评价
• 6年数据工程开发经验
• 精通大数据处理和分析
• 具有大规模数据架构设计经验
• 良好的问题分析和解决能力"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'data_engineer.pdf'), content)
