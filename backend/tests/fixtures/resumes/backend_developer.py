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

# 后端开发工程师简历内容
content = """个人简历

基本信息
姓名：赵伟东
性别：男
年龄：30岁
电话：139xxxx2345
邮箱：zhaowed@example.com
现居地：广州市天河区

教育背景
2013-2017  华南师范大学
软件工程 | 本科

工作经验
2022-至今  京东科技
高级后端开发工程师
• 负责订单系统从Java迁移到Python的重构工作
• 使用Python和FastAPI重写核心微服务
• 优化系统性能，提升吞吐量30%
• 指导团队成员学习Python开发

2017-2022  广州唯品会
Java开发工程师
• 负责商品管理系统后端开发
• 设计实现库存管理模块
• 开发自动化测试框架
• 参与系统架构优化

专业技能
• 编程语言：Java (5年)，Python (2年)
• Java技术栈：Spring Boot，MyBatis，Maven
• Python技术栈：FastAPI，Django，Poetry
• 数据库：MySQL，PostgreSQL，Redis
• 中间件：RabbitMQ，Kafka，ZooKeeper
• 工具链：Git，Jenkins，Docker

项目经验
京东订单系统重构（2022-2023）
• 主导订单系统从Java迁移到Python
• 使用FastAPI重构微服务架构
• 实现分布式事务处理
• 系统性能提升30%

唯品会商品管理系统（2019-2022）
• 设计商品库存管理模块
• 实现秒杀活动支持
• 开发商品数据同步服务
• 日均处理订单100万+

证书
• Oracle认证Java工程师
• Python高级开发工程师认证
• 阿里云解决方案架构师认证

自我评价
• 5年Java开发经验，2年Python开发经验
• 具有大型项目技术栈迁移经验
• 良好的学习能力和技术适应性
• 注重代码质量和系统性能优化"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'backend_developer.pdf'), content)
