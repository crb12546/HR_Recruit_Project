<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <template #header>
            <div class="card-header">
              <h2>欢迎使用智能招聘系统</h2>
            </div>
          </template>
          <div class="card-content">
            <p>本系统提供以下功能：</p>
            <el-row
              :gutter="20"
              class="feature-list"
            >
              <el-col :span="8">
                <el-card
                  shadow="hover"
                  @click="$router.push('/resume')"
                >
                  <template #header>
                    <div class="feature-header">
                      <el-icon><Document /></el-icon>
                      <span>简历管理</span>
                    </div>
                  </template>
                  <div class="feature-content">
                    <p>- 简历上传与解析</p>
                    <p>- 人才画像生成</p>
                    <p>- 智能标签管理</p>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card shadow="hover">
                  <template #header>
                    <div class="feature-header">
                      <el-icon><User /></el-icon>
                      <span>职位管理</span>
                    </div>
                  </template>
                  <div class="feature-content">
                    <p>- 发布招聘需求</p>
                    <p>- 智能匹配候选人</p>
                    <p>- 职位状态跟踪</p>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card shadow="hover">
                  <template #header>
                    <div class="feature-header">
                      <el-icon><Calendar /></el-icon>
                      <span>面试管理</span>
                    </div>
                  </template>
                  <div class="feature-content">
                    <p>- 面试安排</p>
                    <p>- 面试反馈</p>
                    <p>- 入职跟踪</p>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { Document, User, Calendar } from '@element-plus/icons-vue'
</script>

<style scoped>
.home {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h2 {
  margin: 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

.card-content {
  padding: 20px 0;
}

.feature-list {
  margin-top: 20px;
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 500;
}

.el-icon {
  font-size: 20px;
}

.feature-content {
  color: var(--el-text-color-regular);
  line-height: 1.8;
}

.el-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.el-card:hover {
  transform: translateY(-5px);
}
</style>
