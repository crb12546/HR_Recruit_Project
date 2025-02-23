from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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

# 资深Python后端工程师简历内容
content = """个人简历

基本信息
姓名：张志远
性别：男
年龄：32岁
电话：138xxxx6789
邮箱：zhangzy@example.com
现居地：上海市浦东新区

教育背景
2011-2015  上海交通大学
计算机科学与技术 | 本科

工作经验
2020-至今  字节跳动
高级后端工程师
• 负责抖音电商核心支付系统的微服务架构设计和开发
• 带领10人团队完成支付系统重构，将系统QPS提升300%
• 设计并实现分布式事务解决方案，确保交易一致性
• 优化订单系统性能，将订单处理延迟降低40%

2017-2020  阿里巴巴
资深Python开发工程师
• 参与淘宝直播后端系统开发，支持日均千万级直播场次
• 设计实现直播间商品推荐系统，提升转化率30%
• 负责系统监控平台开发，实现故障自动检测和告警

2015-2017  腾讯
Python开发工程师
• 参与QQ音乐推荐系统开发
• 实现用户行为分析系统，处理日均TB级数据
• 开发自动化测试框架，提升测试效率50%

专业技能
• 编程语言：Python (8年经验)，Go，Java
• 框架：FastAPI，Django，Flask，gRPC
• 数据库：MySQL，MongoDB，Redis，Elasticsearch
• 中间件：RabbitMQ，Kafka，ZooKeeper
• 云服务：阿里云，AWS，Kubernetes，Docker
• 开发工具：Git，Jenkins，Prometheus，ELK

项目经验
抖音电商支付系统重构（2021-2022）
• 主导设计新一代支付系统微服务架构
• 实现分布式事务管理，确保跨服务数据一致性
• 设计高可用方案，实现99.999%系统可用性
• 日均处理订单量超过1000万笔

淘宝直播推荐系统（2018-2020）
• 设计实时推荐算法，支持千万级用户同时在线
• 实现A/B测试平台，验证算法效果
• 优化推荐准确率，提升用户停留时间20%

证书
• 阿里云高级架构师认证
• AWS解决方案架构师认证
• 项目管理专业人士认证（PMP）

自我评价
• 具有丰富的大型互联网公司工作经验
• 精通微服务架构设计和分布式系统开发
• 良好的团队管理和技术方案设计能力
• 持续学习新技术，保持技术敏锐度"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'senior_python_engineer.pdf'), content)
