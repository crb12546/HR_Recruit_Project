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
        elif any(line.startswith(section) for section in ['基本信息', '教育背景', '实习经验', '项目经验', '专业技能', '获奖情况', '自我评价']):
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

# 应届毕业生简历内容
content = """个人简历

基本信息
姓名：刘思远
性别：男
年龄：23岁
电话：132xxxx7890
邮箱：liusy@example.com
现居地：北京市海淀区

教育背景
2020-2024  北京理工大学
计算机科学与技术 | 本科
• GPA：3.8/4.0（专业前5%）
• 核心课程：数据结构、算法分析、操作系统、计算机网络、数据库系统、Python程序设计

实习经验
2023.07-2023.09  字节跳动
后端开发实习生
• 参与抖音后端服务开发，使用Python和FastAPI
• 开发用户行为数据分析模块
• 编写单元测试，提升代码覆盖率

2023.03-2023.06  美团
Python开发实习生
• 参与外卖配送系统后端开发
• 实现配送路径优化算法
• 编写技术文档和接口文档

项目经验
校园二手交易平台（2023）
• 独立完成后端开发，使用Python和FastAPI
• 实现用户认证、商品管理、订单处理等功能
• 使用Redis实现商品缓存，提升访问速度
• GitHub获得50+星标

智能图书管理系统（2022）
• 团队项目负责人，带领4人团队
• 使用Python开发后端API
• 实现图书借还、库存管理等功能
• 获得校级优秀项目奖

专业技能
• 编程语言：Python, Java, C++
• Web框架：FastAPI, Django, Flask
• 数据库：MySQL, Redis, MongoDB
• 开发工具：Git, Docker, Linux
• 英语能力：CET-6 (580分)

获奖情况
• 2023年全国大学生软件创新大赛二等奖
• 2023年校级优秀学生
• 2022年美团黑客马拉松最佳创意奖
• 2022年校级编程竞赛一等奖

自我评价
• 扎实的计算机基础知识，热爱编程
• 具有实际项目开发和实习经验
• 良好的学习能力和团队协作精神
• 对后端开发充满热情，期待在工作中快速成长"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'fresh_graduate.pdf'), content)
