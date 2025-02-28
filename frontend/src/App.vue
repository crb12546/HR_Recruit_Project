<template>
  <div id="app">
    <Navigation />
    <div class="content-container">
      <component :is="currentModule"></component>
    </div>
  </div>
</template>

<script>
import Navigation from './components/common/Navigation.vue';
import ResumeList from './components/resume/ResumeList.vue';
import JobList from './components/job/JobList.vue';
import InterviewList from './components/interview/InterviewList.vue';
import OnboardingList from './components/onboarding/OnboardingList.vue';

export default {
  name: 'App',
  components: {
    Navigation,
    ResumeList,
    JobList,
    InterviewList,
    OnboardingList
  },
  data() {
    return {
      currentModule: 'ResumeList'
    }
  },
  created() {
    // 初始化时根据URL哈希设置当前模块
    this.setModuleFromHash();
    
    // 监听哈希变化
    window.addEventListener('hashchange', this.setModuleFromHash);
  },
  beforeDestroy() {  // Vue 2中使用beforeDestroy而不是beforeUnmount
    // 移除事件监听器
    window.removeEventListener('hashchange', this.setModuleFromHash);
  },
  methods: {
    setModuleFromHash() {
      // 从URL哈希获取当前模块
      const hash = window.location.hash.substring(1) || 'resume';
      console.log('Hash changed to:', hash);
      console.log('Setting currentModule based on hash');
      
      switch(hash) {
        case 'job':
          this.currentModule = 'JobList';
          break;
        case 'interview':
          this.currentModule = 'InterviewList';
          break;
        case 'onboarding':
          this.currentModule = 'OnboardingList';
          break;
        case 'resume':
        default:
          this.currentModule = 'ResumeList';
          break;
      }
      console.log('Current module set to:', this.currentModule);
    }
  }
}
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 0;
}

.content-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

@media (max-width: 1240px) {
  .content-container {
    margin: 20px;
  }
}

@media (max-width: 768px) {
  .content-container {
    margin: 10px;
    padding: 10px;
  }
}
</style>
