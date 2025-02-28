<template>
  <div class="resume-list">
    <h2>简历管理</h2>
    
    <div v-for="resume in resumes" :key="resume.id" class="resume-item">
      <h3>
        <a @click="viewResumeDetail(resume.id)">{{ resume.name }}</a>
      </h3>
      <div class="resume-info">
        <p>电话: {{ resume.phone }}</p>
        <p>邮箱: {{ resume.email }}</p>
        <p>教育背景: {{ resume.education }}</p>
        <p>技能: {{ resume.skills }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResumeList',
  data() {
    return {
      resumes: []
    }
  },
  created() {
    // 模拟从API获取数据
    this.fetchResumes();
  },
  methods: {
    async fetchResumes() {
      try {
        // 使用演示数据
        this.resumes = [
          {
            id: 1,
            name: '张三',
            phone: '13800138000',
            email: 'zhangsan@example.com',
            education: '北京大学 计算机科学 硕士',
            skills: 'Python, Java, Docker, Kubernetes'
          },
          {
            id: 2,
            name: '李四',
            phone: '13900139000',
            email: 'lisi@example.com',
            education: '清华大学 软件工程 本科',
            skills: '产品设计, 用户研究, 数据分析'
          },
          {
            id: 3,
            name: '王五',
            phone: '13700137000',
            email: 'wangwu@example.com',
            education: '上海交通大学 人工智能 博士',
            skills: '机器学习, 深度学习, 自然语言处理, 计算机视觉'
          }
        ];
      } catch (error) {
        console.error('获取简历列表失败:', error);
      }
    },
    viewResumeDetail(id) {
      console.log('查看简历详情:', id);
      // 实际应用中可以跳转到简历详情页
    }
  }
}
</script>

<style scoped>
.resume-list {
  padding: 20px;
}

.resume-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.resume-item:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
}

.resume-item h3 {
  margin-top: 0;
  color: #409EFF;
  cursor: pointer;
}

.resume-info {
  color: #606266;
}

.resume-info p {
  margin: 5px 0;
}
</style>
