<template>
  <div class="onboarding-view">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="员工信息" name="employee">
        <employee-form />
      </el-tab-pane>
      <el-tab-pane label="考勤管理" name="attendance">
        <attendance-record />
      </el-tab-pane>
      <el-tab-pane label="档案管理" name="documents">
        <document-upload />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import EmployeeForm from '@/components/onboarding/EmployeeForm.vue'
import AttendanceRecord from '@/components/onboarding/AttendanceRecord.vue'
import DocumentUpload from '@/components/onboarding/DocumentUpload.vue'

const activeTab = ref('employee')
</script>

<style scoped>
.onboarding-view {
  padding: 20px;
}
</style>
