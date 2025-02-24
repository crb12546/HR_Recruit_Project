<template>
  <div class="resume-view">
    <el-card class="resume-card">
      <template #header>
        <div class="card-header">
          <h2>简历管理</h2>
        </div>
      </template>
      <ResumeUpload />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import ResumeUpload from '@/components/resume/ResumeUpload.vue'
</script>

<style scoped>
.resume-view {
  padding: 20px;
}
.resume-card {
  margin-bottom: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
