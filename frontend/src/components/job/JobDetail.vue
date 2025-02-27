<template>
  <div class="job-detail" v-loading="loading">
    <div v-if="job">
      <div class="job-header">
        <h1>{{ job.position_name }}</h1>
        <div class="job-meta">
          <el-tag>{{ job.department }}</el-tag>
          <el-tag type="success">{{ job.location }}</el-tag>
          <el-tag type="warning">{{ job.salary_range }}</el-tag>
        </div>
      </div>
      
      <div class="job-tags">
        <el-tag
          v-for="tag in job.tags"
          :key="tag"
          class="mx-1"
          effect="plain"
        >
          {{ tag }}
        </el-tag>
      </div>
      
      <el-divider />
      
      <div class="job-section">
        <h2>岗位职责</h2>
        <div class="job-content">{{ job.responsibilities }}</div>
      </div>
      
      <div class="job-section">
        <h2>任职要求</h2>
        <div class="job-content">{{ job.requirements }}</div>
      </div>
      
      <div class="job-actions">
        <el-button type="primary" @click="matchResumes">匹配简历</el-button>
        <el-button @click="goBack">返回列表</el-button>
      </div>
    </div>
    
    <el-empty v-else-if="!loading" description="职位不存在" />
    
    <!-- 匹配结果对话框 -->
    <el-dialog
      v-model="matchDialogVisible"
      title="匹配结果"
      width="70%"
    >
      <div v-loading="matchLoading">
        <div v-if="matches.length > 0">
          <el-table :data="matches" style="width: 100%">
            <el-table-column prop="candidate_name" label="候选人" width="120" />
            <el-table-column prop="match_score" label="匹配度" width="100">
              <template #default="scope">
                <el-progress
                  :percentage="scope.row.match_score"
                  :color="getScoreColor(scope.row.match_score)"
                />
              </template>
            </el-table-column>
            <el-table-column prop="match_explanation" label="匹配理由" />
            <el-table-column label="操作" width="180">
              <template #default="scope">
                <el-button
                  size="small"
                  @click="viewResumeDetail(scope.row.resume_id)"
                >
                  查看简历
                </el-button>
                <el-button
                  size="small"
                  type="primary"
                  @click="scheduleInterview(scope.row.resume_id)"
                >
                  安排面试
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <el-empty v-else description="暂无匹配结果" />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const job = ref(null)
const loading = ref(false)
const matchDialogVisible = ref(false)
const matchLoading = ref(false)
const matches = ref([])

// 获取职位详情
const fetchJobDetail = async () => {
  const jobId = route.params.id
  if (!jobId) return
  
  loading.value = true
  try {
    const response = await fetch(`/api/v1/jobs/${jobId}`)
    if (response.ok) {
      job.value = await response.json()
    } else {
      ElMessage.error('获取职位详情失败')
    }
  } catch (error) {
    ElMessage.error('获取职位详情失败')
    console.error('获取职位详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 匹配简历
const matchResumes = async () => {
  const jobId = route.params.id
  if (!jobId) return
  
  matchDialogVisible.value = true
  matchLoading.value = true
  matches.value = []
  
  try {
    const response = await fetch(`/api/v1/jobs/${jobId}/matches`)
    const data = await response.json()
    matches.value = data.matches || []
  } catch (error) {
    ElMessage.error('匹配简历失败')
    console.error('匹配简历失败:', error)
  } finally {
    matchLoading.value = false
  }
}

// 获取匹配度颜色
const getScoreColor = (score) => {
  if (score >= 80) return '#67C23A'
  if (score >= 60) return '#E6A23C'
  return '#F56C6C'
}

// 查看简历详情
const viewResumeDetail = (resumeId) => {
  router.push(`/resumes/${resumeId}`)
}

// 安排面试
const scheduleInterview = (resumeId) => {
  router.push({
    path: '/interviews/new',
    query: {
      resumeId,
      jobId: route.params.id
    }
  })
}

// 返回列表
const goBack = () => {
  router.push('/jobs')
}

onMounted(() => {
  fetchJobDetail()
})
</script>

<style scoped>
.job-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.job-header {
  margin-bottom: 20px;
}

.job-meta {
  margin-top: 10px;
}

.job-meta .el-tag {
  margin-right: 10px;
}

.job-tags {
  margin: 15px 0;
}

.job-tags .el-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.job-section {
  margin-bottom: 30px;
}

.job-content {
  white-space: pre-line;
  line-height: 1.6;
}

.job-actions {
  margin-top: 30px;
}
</style>
