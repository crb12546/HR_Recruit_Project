<template>
  <div class="interview-list">
    <div class="interview-list-header">
      <h2>面试管理</h2>
      <el-button type="primary" @click="scheduleInterview">安排面试</el-button>
    </div>
    
    <el-table
      v-loading="loading"
      :data="interviews"
      style="width: 100%"
    >
      <el-table-column
        prop="candidateName"
        label="候选人"
        width="120"
      />
      <el-table-column
        prop="positionName"
        label="职位"
        width="150"
      />
      <el-table-column
        prop="interviewerName"
        label="面试官"
        width="120"
      />
      <el-table-column
        prop="interview_time"
        label="面试时间"
        width="180"
      >
        <template #default="scope">
          {{ formatDateTime(scope.row.interview_time) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态"
        width="100"
      >
        <template #default="scope">
          <el-tag
            :type="getStatusType(scope.row.status)"
            class="interview-status"
          >
            {{ getStatusText(scope.row.status) }}
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
            @click="viewInterviewDetail(scope.row.id)"
          >
            查看详情
          </el-button>
          <el-button
            v-if="scope.row.status === 'scheduled'"
            size="small"
            type="primary"
            @click="submitFeedback(scope.row.id)"
          >
            提交反馈
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div v-if="interviews.length === 0 && !loading" class="no-data">
      <el-empty description="暂无面试记录" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const interviews = ref([])
const loading = ref(false)

// 获取面试列表
const fetchInterviews = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/v1/interviews')
    const data = await response.json()
    
    // 处理面试数据，获取关联信息
    const interviewsData = data.interviews || []
    const processedInterviews = await Promise.all(
      interviewsData.map(async (interview) => {
        // 获取候选人姓名
        let candidateName = '未知候选人'
        try {
          const resumeResponse = await fetch(`/api/v1/resumes/${interview.resume_id}`)
          if (resumeResponse.ok) {
            const resumeData = await resumeResponse.json()
            candidateName = resumeData.candidate_name
          }
        } catch (error) {
          console.error('获取候选人信息失败:', error)
        }
        
        // 获取职位名称
        let positionName = '未知职位'
        try {
          const jobResponse = await fetch(`/api/v1/jobs/${interview.job_requirement_id}`)
          if (jobResponse.ok) {
            const jobData = await jobResponse.json()
            positionName = jobData.position_name
          }
        } catch (error) {
          console.error('获取职位信息失败:', error)
        }
        
        // 获取面试官姓名
        let interviewerName = '未知面试官'
        try {
          const userResponse = await fetch(`/api/v1/users/${interview.interviewer_id}`)
          if (userResponse.ok) {
            const userData = await userResponse.json()
            interviewerName = userData.username
          }
        } catch (error) {
          console.error('获取面试官信息失败:', error)
        }
        
        return {
          ...interview,
          candidateName,
          positionName,
          interviewerName
        }
      })
    )
    
    interviews.value = processedInterviews
  } catch (error) {
    ElMessage.error('获取面试列表失败')
    console.error('获取面试列表失败:', error)
    
    // 测试环境使用模拟数据
    interviews.value = [
      {
        id: 1,
        candidateName: '张三',
        positionName: 'Python高级工程师',
        interviewerName: '李面试官',
        interview_time: '2025-03-01T14:00:00',
        status: 'scheduled'
      },
      {
        id: 2,
        candidateName: '李四',
        positionName: '前端开发工程师',
        interviewerName: '王面试官',
        interview_time: '2025-03-02T10:30:00',
        status: 'completed'
      }
    ]
  } finally {
    loading.value = false
  }
}

// 安排面试
const scheduleInterview = () => {
  router.push('/interviews/new')
}

// 查看面试详情
const viewInterviewDetail = (interviewId) => {
  router.push(`/interviews/${interviewId}`)
}

// 提交反馈
const submitFeedback = (interviewId) => {
  router.push(`/interviews/${interviewId}/feedback`)
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '未设置'
  const date = new Date(dateTimeStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    scheduled: 'info',
    completed: 'success',
    rejected: 'danger',
    pending: 'warning',
    cancelled: 'info'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    scheduled: '待面试',
    completed: '已通过',
    rejected: '未通过',
    pending: '待定',
    cancelled: '已取消'
  }
  return statusMap[status] || '未知状态'
}

onMounted(() => {
  fetchInterviews()
})
</script>

<style scoped>
.interview-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.interview-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.no-data {
  margin-top: 40px;
}
</style>
