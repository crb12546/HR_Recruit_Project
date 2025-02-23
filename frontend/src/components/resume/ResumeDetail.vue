<template>
  <div class="resume-detail" v-loading="loading">
    <div class="resume-detail__header">
      <el-page-header @back="goBack">
        <template #content>
          <span class="font-bold">{{ resume?.candidate_name || '简历详情' }}</span>
        </template>
      </el-page-header>
    </div>

    <el-card v-if="resume" class="resume-detail__content">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
          <el-button-group>
            <el-button type="primary" @click="downloadResume">
              下载简历
            </el-button>
            <el-button @click="editTags">
              编辑标签
            </el-button>
          </el-button-group>
        </div>
      </template>

      <div class="info-section">
        <div class="info-item">
          <label>候选人：</label>
          <span>{{ resume.candidate_name }}</span>
        </div>
        <div class="info-item">
          <label>上传时间：</label>
          <span>{{ formatDate(resume.created_at) }}</span>
        </div>
        <div class="info-item">
          <label>文件类型：</label>
          <span>{{ resume.file_type }}</span>
        </div>
      </div>

      <div class="tags-section">
        <label>技能标签：</label>
        <div class="tags-container">
          <el-tag
            v-for="tag in resume.tags"
            :key="tag.id"
            class="mx-1"
            closable
            @close="removeTag(tag.id)"
          >
            {{ tag.name }}
          </el-tag>
          <el-button
            v-if="!showTagInput"
            class="button-new-tag"
            size="small"
            @click="showTagInput = true"
          >
            + 添加标签
          </el-button>
        </div>
      </div>

      <div class="portrait-section">
        <label>人才画像：</label>
        <p class="portrait-content">{{ resume.talent_portrait }}</p>
      </div>

      <div class="content-section">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="简历原文" name="original">
            <pre class="resume-content">{{ resume.ocr_content }}</pre>
          </el-tab-pane>
          <el-tab-pane label="解析内容" name="parsed">
            <pre class="resume-content">{{ resume.parsed_content }}</pre>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>

    <el-dialog
      v-model="tagDialogVisible"
      title="编辑标签"
      width="500px"
    >
      <div class="tag-dialog-content">
        <el-select
          v-model="selectedTags"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="请选择或创建标签"
          class="tag-select"
        >
          <el-option
            v-for="tag in availableTags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          />
        </el-select>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="tagDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveTags">
            确认
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useResumeStore } from '@/store/resume'
import type { Resume, Tag } from '@/types'

const route = useRoute()
const router = useRouter()
const resumeStore = useResumeStore()

const loading = ref(false)
const resume = ref<Resume | null>(null)
const activeTab = ref('original')
const tagDialogVisible = ref(false)
const selectedTags = ref<number[]>([])
const showTagInput = ref(false)
const availableTags = ref<Tag[]>([])

const goBack = () => {
  router.push('/resumes')
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const downloadResume = () => {
  if (!resume.value?.file_url) return
  window.open(resume.value.file_url, '_blank')
}

const editTags = async () => {
  try {
    // 获取所有可用标签
    const tags = await resumeStore.fetchTags()
    availableTags.value = tags
    selectedTags.value = resume.value?.tags.map(t => t.id) || []
    tagDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取标签列表失败')
  }
}

const saveTags = async () => {
  if (!resume.value) return
  
  try {
    loading.value = true
    // 更新标签
    const updatedResume = await resumeStore.updateResumeTags(
      resume.value.id,
      selectedTags.value
    )
    resume.value = updatedResume
    tagDialogVisible.value = false
    ElMessage.success('标签更新成功')
  } catch (error) {
    ElMessage.error('标签更新失败')
  } finally {
    loading.value = false
  }
}

const removeTag = async (tagId: number) => {
  if (!resume.value) return
  
  try {
    loading.value = true
    await resumeStore.removeTagFromResume(resume.value.id, tagId)
    resume.value.tags = resume.value.tags.filter(t => t.id !== tagId)
    ElMessage.success('标签移除成功')
  } catch (error) {
    ElMessage.error('标签移除失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const resumeId = parseInt(route.params.id as string)
  if (isNaN(resumeId)) {
    ElMessage.error('无效的简历ID')
    router.push('/resumes')
    return
  }

  loading.value = true
  try {
    resume.value = await resumeStore.getResumeById(resumeId)
  } catch (error) {
    ElMessage.error('获取简历详情失败')
    router.push('/resumes')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.resume-detail {
  padding: 20px;
}

.resume-detail__header {
  margin-bottom: 20px;
}

.resume-detail__content {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-section {
  margin-bottom: 24px;
}

.info-item {
  margin-bottom: 12px;
}

.info-item label {
  font-weight: bold;
  margin-right: 8px;
  color: #606266;
}

.tags-section {
  margin-bottom: 24px;
}

.tags-container {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.portrait-section {
  margin-bottom: 24px;
}

.portrait-content {
  margin-top: 8px;
  line-height: 1.6;
  white-space: pre-line;
}

.content-section {
  margin-top: 24px;
}

.resume-content {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
  white-space: pre-wrap;
  font-family: monospace;
  max-height: 500px;
  overflow-y: auto;
}

.tag-dialog-content {
  padding: 20px 0;
}

.tag-select {
  width: 100%;
}

.mx-1 {
  margin: 0 4px;
}

.button-new-tag {
  margin-left: 8px;
  height: 32px;
  padding-top: 0;
  padding-bottom: 0;
}
</style>
