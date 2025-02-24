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

# 前端开发工程师简历内容
content = """个人简历

基本信息
姓名：陈雨婷
性别：女
年龄：26岁
电话：137xxxx5678
邮箱：chenyt@example.com
现居地：杭州市西湖区

教育背景
2016-2020  浙江大学
数字媒体技术 | 本科

工作经验
2022-至今  网易
高级前端工程师
• 负责网易云音乐Web端核心功能开发
• 使用Vue.js 3.0重构用户中心模块
• 优化首屏加载时间，提升50%
• 开发组件库，提升团队开发效率

2020-2022  阿里巴巴
前端开发工程师
• 参与淘宝直播间前端开发
• 实现直播间商品展示和互动功能
• 开发通用动画组件库

专业技能
• 前端框架：Vue.js (3年)，React，Angular
• 开发工具：TypeScript，Webpack，Vite
• UI框架：Element Plus，Ant Design
• 状态管理：Vuex，Pinia，Redux
• 测试工具：Jest，Vitest
• 版本控制：Git，GitLab

项目经验
网易云音乐用户中心重构（2022-2023）
• 使用Vue.js 3.0 + TypeScript重构
• 实现Composition API最佳实践
• 开发自定义Hooks库
• 首屏加载性能提升50%

淘宝直播间前端开发（2020-2022）
• 开发直播间商品展示模块
• 实现礼物动画特效系统
• 优化直播间实时互动功能
• 日均服务用户超过500万

证书
• 阿里巴巴前端认证工程师
• Vue.js核心开发者认证
• 前端性能优化专家认证

自我评价
• 3年Vue.js开发经验，精通前端开发
• 具有大型项目开发和性能优化经验
• 良好的团队协作和沟通能力
• 对前端新技术保持持续学习"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'frontend_developer.pdf'), content)
