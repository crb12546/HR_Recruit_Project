<template>
  <div class="resume-upload">
    <div class="upload-header">
      <h3>简历上传</h3>
      <p class="upload-description">支持单个或批量上传简历文件，系统将自动提取简历内容并生成人才画像</p>
    </div>
    <el-upload
      class="upload-area"
      drag
      :action="uploadUrl"
      :headers="headers"
      :before-upload="handleBeforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-progress="handleProgress"
      :on-exceed="handleExceed"
      :limit="5"
      accept=".pdf,.doc,.docx,.txt,.xls,.xlsx"
      multiple
      :disabled="isUploading"
    >
      <template #trigger>
        <el-icon class="el-icon--upload">
          <upload-filled />
        </el-icon>
        <div class="el-upload__text">
          将文件拖到此处或 <em>点击上传</em>
        </div>
      </template>
      
      <template #tip>
        <div class="el-upload__tip">
          支持 PDF、Word、Excel、TXT 格式，文件大小不超过100MB，可批量上传（最多5个文件）
        </div>
      </template>
    </el-upload>

    <div v-if="isUploading" class="upload-progress">
      <el-progress 
        :percentage="uploadProgress" 
        :status="uploadStatus"
      >
        <template #default="{ percentage }">
          <span class="progress-text">{{ percentage }}%</span>
        </template>
      </el-progress>
      <p class="progress-tip">正在处理文件，请稍候...</p>
    </div>

    <div
      v-if="lastUploadedResume"
      class="upload-result"
    >
      <el-alert
        title="简历上传成功"
        type="success"
        show-icon
        :closable="false"
      >
        <template #description>
          <div class="resume-content">
            <div class="talent-portrait">
              <h4>人才画像</h4>
              <p>{{ lastUploadedResume.talent_portrait }}</p>
            </div>
            <div class="ocr-content">
              <h4>简历内容</h4>
              <el-scrollbar height="200px">
                <p class="text-content">{{ lastUploadedResume.ocr_content }}</p>
              </el-scrollbar>
            </div>
            <div class="resume-tags">
              <h4>技能标签</h4>
              <div class="tags-container">
                <el-tag 
                  v-for="tag in lastUploadedResume.tags" 
                  :key="tag.id"
                  class="mx-1"
                  type="info"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
            </div>
          </div>
        </template>
      </el-alert>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { UploadProps } from 'element-plus'
import type { Resume } from '@/types'
import { useResumeStore } from '@/store/resume'

const resumeStore = useResumeStore()

// 状态管理
const isUploading = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref<'success' | 'exception'>('success')
const lastUploadedResume = ref<Resume | null>(null)

// 上传配置
const uploadUrl = '/api/v1/resumes/upload'
const headers = {
  'Accept': 'application/json'
}

// 文件上传前的验证
const handleBeforeUpload: UploadProps['beforeUpload'] = (file) => {
  const isValidType = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/plain'
  ].includes(file.type)
  
  const isLt100M = file.size / 1024 / 1024 < 100

  if (!isValidType) {
    ElMessage.error('不支持的文件格式')
    return false
  }
  
  if (!isLt100M) {
    ElMessage.error('文件大小不能超过100MB')
    return false
  }

  isUploading.value = true
  uploadProgress.value = 0
  uploadStatus.value = 'success'
  return true
}

// 上传进度处理
const handleProgress: UploadProps['onProgress'] = (event) => {
  if (event) {
    uploadProgress.value = Math.round(event.percent)
  }
}

// 上传成功处理
const handleSuccess: UploadProps['onSuccess'] = (response) => {
  isUploading.value = false
  uploadProgress.value = 100
  
  const resume = response as Resume
  lastUploadedResume.value = resume
  resumeStore.addResume(resume)
  
  ElMessage.success('简历上传成功')
}

// 上传失败处理
const handleError: UploadProps['onError'] = (error) => {
  isUploading.value = false
  uploadStatus.value = 'exception'
  
  ElMessage.error(`上传失败: ${error.message || '未知错误'}`)
}

// 超出文件数量限制
const handleExceed: UploadProps['onExceed'] = () => {
  ElMessage.warning('一次最多上传5个文件')
}
</script>

<style scoped>
.resume-upload {
  width: 100%;
  padding: 20px;
}

.upload-area {
  border: 2px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: border-color .3s;
}

.upload-area:hover {
  border-color: var(--el-color-primary);
}

.el-icon--upload {
  font-size: 48px;
  color: var(--el-text-color-regular);
  margin: 20px 0 16px;
}

.el-upload__text {
  color: var(--el-text-color-regular);
  font-size: 14px;
  text-align: center;
  margin: 0 0 16px;
}

.el-upload__text em {
  color: var(--el-color-primary);
  font-style: normal;
}

.el-upload__tip {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 8px;
}

.upload-result {
  margin-top: 20px;
}

.upload-header {
  margin-bottom: 20px;
  text-align: center;
}

.upload-header h3 {
  font-size: 24px;
  color: var(--el-text-color-primary);
  margin-bottom: 8px;
}

.upload-description {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.resume-content {
  padding: 16px;
}

.talent-portrait,
.ocr-content,
.resume-tags {
  margin-bottom: 20px;
}

.talent-portrait h4,
.ocr-content h4,
.resume-tags h4 {
  font-size: 16px;
  color: var(--el-text-color-primary);
  margin-bottom: 8px;
}

.text-content {
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-regular);
  white-space: pre-wrap;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.upload-progress {
  margin-top: 16px;
  text-align: center;
}

.progress-text {
  font-size: 14px;
  color: var(--el-color-primary);
}

.progress-tip {
  margin-top: 8px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.el-progress {
  margin: 0 auto;
  max-width: 400px;
}
</style>
