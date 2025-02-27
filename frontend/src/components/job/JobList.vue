<template>
  <div class="job-list">
    <div class="job-list-header">
      <h2>招聘职位列表</h2>
      <el-button type="primary" @click="showCreateForm">发布新职位</el-button>
    </div>
    
    <el-table
      v-loading="loading"
      :data="jobs"
      style="width: 100%"
    >
      <el-table-column
        prop="position_name"
        label="职位名称"
        width="180"
      />
      <el-table-column
        prop="department"
        label="部门"
        width="120"
      />
      <el-table-column
        prop="location"
        label="工作地点"
        width="120"
      />
      <el-table-column
        prop="salary_range"
        label="薪资范围"
        width="120"
      />
      <el-table-column
        label="标签"
        width="200"
      >
        <template #default="scope">
          <el-tag
            v-for="tag in scope.row.tags"
            :key="tag"
            class="mx-1"
            size="small"
          >
            {{ tag }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="200"
      >
        <template #default="scope">
          <el-button
            size="small"
            @click="viewJobDetail(scope.row.id)"
          >
            查看详情
          </el-button>
          <el-button
            size="small"
            type="primary"
            @click="matchResumes(scope.row.id)"
          >
            匹配简历
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 创建职位表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="发布新职位"
      width="50%"
    >
      <job-requirement-form @submit-success="handleFormSubmit" />
    </el-dialog>
    
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
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import JobRequirementForm from './JobRequirementForm.vue'

const router = useRouter()
const jobs = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const matchDialogVisible = ref(false)
const matchLoading = ref(false)
const matches = ref([])
const currentJobId = ref(null)

// 获取职位列表
const fetchJobs = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/v1/jobs')
    const data = await response.json()
    jobs.value = data.jobs || []
  } catch (error) {
    ElMessage.error('获取职位列表失败')
    console.error('获取职位列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 显示创建表单
const showCreateForm = () => {
  dialogVisible.value = true
}

// 处理表单提交
const handleFormSubmit = async (formData) => {
  try {
    const response = await fetch('/api/v1/jobs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
    
    if (response.ok) {
      ElMessage.success('职位发布成功')
      dialogVisible.value = false
      fetchJobs() // 刷新列表
    } else {
      const error = await response.json()
      throw new Error(error.detail || '职位发布失败')
    }
  } catch (error) {
    ElMessage.error(error.message || '职位发布失败')
    console.error('职位发布失败:', error)
  }
}

// 查看职位详情
const viewJobDetail = (jobId) => {
  router.push(`/jobs/${jobId}`)
}

// 匹配简历
const matchResumes = async (jobId) => {
  currentJobId.value = jobId
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
      jobId: currentJobId.value
    }
  })
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.job-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.el-tag {
  margin-right: 5px;
}
</style>
