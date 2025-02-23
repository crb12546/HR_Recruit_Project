<template>
  <div class="resume-upload">
    <el-upload
      class="upload-demo"
      action="/api/v1/resumes/upload"
      :on-success="handleSuccess"
      :before-upload="beforeUpload"
      :on-error="handleError"
      :on-progress="handleProgress"
      :multiple="true"
      :limit="10"
      accept=".pdf,.doc,.docx,.xls,.xlsx"
      :show-file-list="true"
    >
      <template #trigger>
        <el-button type="primary">选择简历文件</el-button>
      </template>
      <template #tip>
        <div class="el-upload__tip">支持PDF、Word、Excel格式，单个文件不超过100MB</div>
      </template>
    </el-upload>
    
    <el-progress 
      v-if="uploadProgress > 0 && uploadProgress < 100"
      :percentage="uploadProgress"
      :format="percentageFormat"
      class="upload-progress"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import type { UploadProgressEvent } from 'element-plus'

const emit = defineEmits(['upload-success'])
const uploadProgress = ref(0)

const beforeUpload = (file: File) => {
  const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
  const isValidType = validTypes.includes(file.type)
  const isLt100M = file.size / 1024 / 1024 < 100

  if (!isValidType) {
    ElMessage.error('只支持PDF、Word和Excel格式的文件')
    return false
  }
  if (!isLt100M) {
    ElMessage.error('文件大小不能超过100MB')
    return false
  }
  return true
}

const handleProgress = (event: UploadProgressEvent) => {
  uploadProgress.value = Math.round(event.percent)
}

const percentageFormat = (percentage: number) => {
  return percentage === 100 ? '上传完成' : `${percentage}%`
}

const handleSuccess = (response: any) => {
  uploadProgress.value = 100
  ElMessage.success('简历上传成功')
  emit('upload-success', response)
}

const handleError = (error: Error) => {
  uploadProgress.value = 0
  const message = error instanceof Error ? error.message : '上传失败，请重试'
  ElMessage.error(message)
}

defineExpose({
  uploadProgress,
  beforeUpload,
  handleSuccess,
  handleError
})
</script>

<style scoped>
.resume-upload {
  margin: 20px;
}
.el-upload__tip {
  color: #909399;
  font-size: 14px;
  margin-top: 8px;
}
.upload-progress {
  margin-top: 20px;
}
</style>
