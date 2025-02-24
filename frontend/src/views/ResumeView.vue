<template>
  <div class="resume-view">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="resume-card">
          <template #header>
            <div class="card-header">
              <h2>简历管理</h2>
              <el-button
                type="primary"
                @click="handleUpload"
              >
                上传简历
              </el-button>
            </div>
          </template>
          <div
            v-if="resumeStore.uploadedResumes.length > 0"
            class="resume-content"
          >
            <el-table
              :data="resumeStore.uploadedResumes"
              style="width: 100%"
            >
              <el-table-column
                prop="candidate_name"
                label="候选人"
                width="120"
              />
              <el-table-column
                prop="file_type"
                label="文件类型"
                width="100"
              />
              <el-table-column
                prop="talent_portrait"
                label="人才画像"
              />
              <el-table-column
                label="标签"
                width="200"
              >
                <template #default="{ row }">
                  <el-tag
                    v-for="tag in row.tags"
                    :key="tag.id"
                    size="small"
                    class="mx-1"
                  >
                    {{ tag.name }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column
                label="操作"
                width="120"
              >
                <template #default="{ row }">
                  <el-button
                    link
                    type="primary"
                    @click="handleView(row)"
                  >
                    查看
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          <div
            v-else
            class="empty-tip"
          >
            暂无简历记录，请点击右上角"上传简历"按钮添加
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      v-model="uploadDialogVisible"
      title="上传简历"
      width="50%"
      destroy-on-close
    >
      <ResumeUpload @upload-success="handleUploadSuccess" />
    </el-dialog>

    <el-dialog
      v-model="detailDialogVisible"
      title="简历详情"
      width="70%"
    >
      <ResumeDetail
        v-if="currentResume"
        :resume="currentResume"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElRow, ElCol, ElCard, ElTable, ElTableColumn, ElTag, ElButton, ElDialog } from 'element-plus'
import ResumeUpload from '@/components/resume/ResumeUpload.vue'
import ResumeDetail from '@/components/resume/ResumeDetail.vue'
import { useResumeStore } from '@/store/resume'
import type { Resume } from '@/types'

const resumeStore = useResumeStore()
const uploadDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const currentResume = ref<Resume | null>(null)

const handleUpload = () => {
  uploadDialogVisible.value = true
}

const handleUploadSuccess = () => {
  uploadDialogVisible.value = false
}

const handleView = (resume: Resume) => {
  currentResume.value = resume
  detailDialogVisible.value = true
}
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

h2 {
  margin: 0;
  font-size: 18px;
  color: var(--el-text-color-primary);
}

.resume-content {
  margin-top: 20px;
}

.empty-tip {
  text-align: center;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  padding: 40px 0;
}

.el-tag {
  margin-right: 4px;
  margin-bottom: 4px;
}

:deep(.el-dialog__body) {
  padding-top: 20px;
}
</style>
