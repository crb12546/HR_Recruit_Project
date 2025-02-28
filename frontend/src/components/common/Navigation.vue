<template>
  <div class="navigation">
    <div class="nav-header">
      <h1>HR招聘系统</h1>
    </div>
    <div class="nav-menu">
      <div 
        class="nav-item" 
        :class="{ active: activeModule === 'resume' }"
        @click="navigateTo('resume')">
        简历管理
      </div>
      <div 
        class="nav-item" 
        :class="{ active: activeModule === 'job' }"
        @click="navigateTo('job')">
        职位管理
      </div>
      <div 
        class="nav-item" 
        :class="{ active: activeModule === 'interview' }"
        @click="navigateTo('interview')">
        面试管理
      </div>
      <div 
        class="nav-item" 
        :class="{ active: activeModule === 'onboarding' }"
        @click="navigateTo('onboarding')">
        入职管理
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Navigation',
  data() {
    return {
      activeModule: 'resume'
    }
  },
  created() {
    // 初始化时根据URL哈希设置活动模块
    this.setActiveModuleFromHash();
    
    // 监听哈希变化
    window.addEventListener('hashchange', this.setActiveModuleFromHash);
  },
  beforeUnmount() {
    // 移除事件监听器
    window.removeEventListener('hashchange', this.setActiveModuleFromHash);
  },
  methods: {
    navigateTo(module) {
      // 更新URL哈希
      window.location.hash = module;
      this.activeModule = module;
    },
    setActiveModuleFromHash() {
      // 从URL哈希获取当前模块
      const hash = window.location.hash.substring(1);
      if (hash && ['resume', 'job', 'interview', 'onboarding'].includes(hash)) {
        this.activeModule = hash;
      } else {
        // 默认为简历管理
        this.activeModule = 'resume';
      }
    }
  }
}
</script>

<style scoped>
.navigation {
  width: 100%;
  background-color: #409EFF;
  color: white;
}

.nav-header {
  padding: 20px;
  text-align: center;
}

.nav-header h1 {
  margin: 0;
  font-size: 24px;
}

.nav-menu {
  display: flex;
  justify-content: center;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}

.nav-item {
  padding: 15px 20px;
  cursor: pointer;
  color: #606266;
  font-size: 16px;
  transition: all 0.3s;
}

.nav-item:hover {
  color: #409EFF;
  background-color: #ecf5ff;
}

.nav-item.active {
  color: #409EFF;
  font-weight: bold;
  border-bottom: 2px solid #409EFF;
}

@media (max-width: 768px) {
  .nav-menu {
    flex-direction: column;
  }
  
  .nav-item {
    text-align: center;
    border-bottom: 1px solid #e4e7ed;
  }
  
  .nav-item.active {
    border-bottom: 1px solid #e4e7ed;
    border-left: 4px solid #409EFF;
  }
}
</style>
