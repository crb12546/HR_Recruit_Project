<template>
  <div class="home">
    <h1>智能招聘系统</h1>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>简历管理</span>
              <el-button type="primary" @click="$router.push('/resume')">进入</el-button>
            </div>
          </template>
          <div class="card-content">
            <p>- 简历上传与解析</p>
            <p>- 人才画像生成</p>
            <p>- 智能标签管理</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-content {
  color: #666;
  line-height: 1.8;
}
</style>
