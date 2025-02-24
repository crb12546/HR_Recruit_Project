<template>
  <el-config-provider :locale="zhCn">
    <div class="app">
      <el-container>
        <el-header>
          <el-menu
            mode="horizontal"
            router
          >
            <el-menu-item index="/">
              首页
            </el-menu-item>
            <el-menu-item index="/resume">
              简历管理
            </el-menu-item>
          </el-menu>
        </el-header>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
</script>

<style>
.app {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-header {
  padding: 0;
  border-bottom: 1px solid var(--el-border-color-light);
}

.el-main {
  padding: 20px;
  background-color: var(--el-bg-color-page);
}
</style>
