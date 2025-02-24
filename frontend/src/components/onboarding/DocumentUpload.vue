<template>
  <div class="document-upload">
    <el-upload
      class="upload-demo"
      :action="uploadUrl"
      :on-preview="handlePreview"
      :on-remove="handleRemove"
      :before-remove="beforeRemove"
      :on-success="handleSuccess"
      :on-error="handleError"
      multiple
      :limit="5"
    >
      <el-button type="primary">上传文件</el-button>
      <template #tip>
        <div class="el-upload__tip">
          支持任意格式文件，单个文件不超过10MB
        </div>
      </template>
    </el-upload>
    
    <div class="document-list">
      <h3>档案列表</h3>
      <el-table :data="documents" style="width: 100%">
        <el-table-column prop="document_type" label="文档类型" width="150" />
        <el-table-column prop="file_name" label="文件名" />
        <el-table-column prop="upload_time" label="上传时间" width="180">
          <template #default="scope">
            {{ formatTime(scope.row.upload_time) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button
              size="small"
              type="primary"
              link
              @click="downloadDocument(scope.row)"
            >
              下载
            </el-button>
            <el-button
              size="small"
              type="danger"
              link
              @click="deleteDocument(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import dayjs from 'dayjs'

const uploadUrl = '/api/v1/employees/1/documents' // TODO: 使用实际的员工ID
const documents = ref([])

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

const handleSuccess = (response, file) => {
  ElMessage.success('文件上传成功')
  loadDocuments()
}

const handleError = (error, file) => {
  ElMessage.error('文件上传失败，请重试')
}

const handlePreview = (file) => {
  window.open(file.url)
}

const handleRemove = (file, fileList) => {
  loadDocuments()
}

const beforeRemove = (file) => {
  return ElMessageBox.confirm(
    `确定移除 ${file.name}？`
  )
}

const downloadDocument = (document) => {
  window.open(document.file_url)
}

const deleteDocument = async (document) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个文档吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await request.delete(`/api/v1/employees/1/documents/${document.id}`)
    ElMessage.success('文档删除成功')
    loadDocuments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败，请重试')
    }
  }
}

const loadDocuments = async () => {
  try {
    const response = await request.get('/api/v1/employees/1/documents')
    documents.value = response.data
  } catch (error) {
    ElMessage.error('获取文档列表失败')
  }
}

onMounted(() => {
  loadDocuments()
})
</script>

<style scoped>
.document-upload {
  padding: 20px;
}

.document-list {
  margin-top: 30px;
}

h3 {
  margin-bottom: 15px;
  color: #606266;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 7px;
}
</style>
