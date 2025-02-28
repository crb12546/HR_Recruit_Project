<template>
  <div class="onboarding-list">
    <div class="onboarding-list-header">
      <h2>入职管理</h2>
      <el-button type="primary" @click="createOnboarding">创建入职记录</el-button>
    </div>
    
    <el-table
      v-loading="loading"
      :data="onboardings"
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
        prop="department"
        label="部门"
        width="120"
      />
      <el-table-column
        prop="offer_date"
        label="Offer日期"
        width="120"
      >
        <template #default="scope">
          {{ formatDate(scope.row.offer_date) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="start_date"
        label="入职日期"
        width="120"
      >
        <template #default="scope">
          {{ formatDate(scope.row.start_date) }}
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
            class="onboarding-status"
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
            @click="viewOnboardingDetail(scope.row.id)"
          >
            查看详情
          </el-button>
          <el-button
            size="small"
            type="primary"
            @click="updateOnboarding(scope.row.id)"
          >
            更新状态
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <div v-if="onboardings.length === 0 && !loading" class="no-data">
      <el-empty description="暂无入职记录" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const onboardings = ref([])
const loading = ref(false)

// 获取入职记录列表
const fetchOnboardings = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/v1/onboardings')
    const data = await response.json()
    
    // 处理入职数据，获取关联信息
    const onboardingsData = data.onboardings || []
    const processedOnboardings = await Promise.all(
      onboardingsData.map(async (onboarding) => {
        // 获取候选人姓名
        let candidateName = '未知候选人'
        try {
          const resumeResponse = await fetch(`/api/v1/resumes/${onboarding.resume_id}`)
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
          const jobResponse = await fetch(`/api/v1/jobs/${onboarding.job_requirement_id}`)
          if (jobResponse.ok) {
            const jobData = await jobResponse.json()
            positionName = jobData.position_name
          }
        } catch (error) {
          console.error('获取职位信息失败:', error)
        }
        
        return {
          ...onboarding,
          candidateName,
          positionName
        }
      })
    )
    
    onboardings.value = processedOnboardings
  } catch (error) {
    ElMessage.error('获取入职记录列表失败')
    console.error('获取入职记录列表失败:', error)
    
    // 测试环境使用模拟数据
    onboardings.value = [
      {
        id: 1,
        candidateName: '张三',
        positionName: 'Python高级工程师',
        department: '技术部',
        offer_date: '2025-03-10T00:00:00',
        start_date: '2025-04-01T00:00:00',
        status: 'pending'
      },
      {
        id: 2,
        candidateName: '李四',
        positionName: '前端开发工程师',
        department: '技术部',
        offer_date: '2025-03-15T00:00:00',
        start_date: '2025-04-15T00:00:00',
        status: 'in_progress'
      }
    ]
  } finally {
    loading.value = false
  }
}

// 创建入职记录
const createOnboarding = () => {
  router.push('/onboardings/new')
}

// 查看入职详情
const viewOnboardingDetail = (onboardingId) => {
  router.push(`/onboardings/${onboardingId}`)
}

// 更新入职状态
const updateOnboarding = (onboardingId) => {
  router.push(`/onboardings/${onboardingId}/edit`)
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未设置'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    pending: '待入职',
    in_progress: '入职中',
    completed: '已入职',
    cancelled: '已取消'
  }
  return statusMap[status] || '未知状态'
}

onMounted(() => {
  fetchOnboardings()
})
</script>

<style scoped>
.onboarding-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.onboarding-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.no-data {
  margin-top: 40px;
}
</style>
