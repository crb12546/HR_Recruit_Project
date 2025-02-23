<template>
  <div class="resume-upload">
    <el-upload
      class="upload-demo"
      action="/api/v1/resumes/upload"
      :on-success="handleSuccess"
      :before-upload="beforeUpload"
      :on-error="handleError"
      accept=".pdf,.doc,.docx,.xls,.xlsx"
    >
      <el-button type="primary">上传简历</el-button>
      <template #tip>
        <div class="el-upload__tip">支持PDF、Word、Excel格式，最大100MB</div>
      </template>
    </el-upload>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'

const emit = defineEmits(['upload-success'])

const beforeUpload = (file) => {
  const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
  if (!validTypes.includes(file.type)) {
    ElMessage.error('只支持PDF、Word和Excel格式的文件')
    return false
  }
  return true
}

const handleSuccess = (response) => {
  ElMessage.success('简历上传成功')
  emit('upload-success', response)
}

const handleError = () => {
  ElMessage.error('上传失败，请重试')
}
</script>
