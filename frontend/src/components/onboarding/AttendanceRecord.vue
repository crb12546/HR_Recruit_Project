<template>
  <div class="attendance-record">
    <div class="attendance-actions">
      <el-button type="primary" @click="checkIn" :loading="loading">
        上班打卡
      </el-button>
      <el-button type="success" @click="checkOut" :loading="loading">
        下班打卡
      </el-button>
    </div>
    
    <div class="attendance-status" v-if="todayRecord">
      <h3>今日考勤状态</h3>
      <el-descriptions border>
        <el-descriptions-item label="上班时间">
          {{ formatTime(todayRecord.check_in) }}
        </el-descriptions-item>
        <el-descriptions-item label="下班时间">
          {{ todayRecord.check_out ? formatTime(todayRecord.check_out) : '未打卡' }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(todayRecord.status)">
            {{ todayRecord.status }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </div>
    
    <div class="attendance-history">
      <h3>考勤记录</h3>
      <el-table :data="records" style="width: 100%">
        <el-table-column prop="date" label="日期" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.check_in) }}
          </template>
        </el-table-column>
        <el-table-column prop="check_in" label="上班时间" width="180">
          <template #default="scope">
            {{ formatTime(scope.row.check_in) }}
          </template>
        </el-table-column>
        <el-table-column prop="check_out" label="下班时间" width="180">
          <template #default="scope">
            {{ scope.row.check_out ? formatTime(scope.row.check_out) : '未打卡' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import dayjs from 'dayjs'

const loading = ref(false)
const todayRecord = ref(null)
const records = ref([])

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

const formatDate = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD')
}

const getStatusType = (status: string) => {
  const types = {
    '正常': 'success',
    '迟到': 'warning',
    '早退': 'warning',
    '缺勤': 'danger'
  }
  return types[status] || 'info'
}

const checkIn = async () => {
  loading.value = true
  try {
    const response = await request.post('/api/v1/attendance/check-in/1') // TODO: 使用实际的员工ID
    ElMessage.success('上班打卡成功')
    await loadTodayRecord()
  } catch (error) {
    ElMessage.error('打卡失败，请重试')
  } finally {
    loading.value = false
  }
}

const checkOut = async () => {
  loading.value = true
  try {
    const response = await request.post('/api/v1/attendance/check-out/1') // TODO: 使用实际的员工ID
    ElMessage.success('下班打卡成功')
    await loadTodayRecord()
  } catch (error) {
    ElMessage.error('打卡失败，请重试')
  } finally {
    loading.value = false
  }
}

const loadTodayRecord = async () => {
  try {
    const now = new Date()
    const response = await request.get('/api/v1/attendance/monthly/1', {
      params: {
        year: now.getFullYear(),
        month: now.getMonth() + 1
      }
    })
    const records = response.data
    todayRecord.value = records.find(r => 
      dayjs(r.check_in).format('YYYY-MM-DD') === dayjs().format('YYYY-MM-DD')
    )
  } catch (error) {
    ElMessage.error('获取考勤记录失败')
  }
}

const loadMonthlyRecords = async () => {
  try {
    const now = new Date()
    const response = await request.get('/api/v1/attendance/monthly/1', {
      params: {
        year: now.getFullYear(),
        month: now.getMonth() + 1
      }
    })
    records.value = response.data
  } catch (error) {
    ElMessage.error('获取考勤记录失败')
  }
}

onMounted(async () => {
  await loadTodayRecord()
  await loadMonthlyRecords()
})
</script>

<style scoped>
.attendance-record {
  padding: 20px;
}

.attendance-actions {
  margin-bottom: 20px;
}

.attendance-status {
  margin-bottom: 30px;
}

.attendance-history {
  margin-top: 30px;
}

h3 {
  margin-bottom: 15px;
  color: #606266;
}
</style>
