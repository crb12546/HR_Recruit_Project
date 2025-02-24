<template>
  <div class="job-requirement-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
    >
      <el-form-item label="职位名称" prop="position_name">
        <el-input v-model="form.position_name" />
      </el-form-item>
      <el-form-item label="部门" prop="department">
        <el-input v-model="form.department" />
      </el-form-item>
      <el-form-item label="岗位职责" prop="responsibilities">
        <el-input
          v-model="form.responsibilities"
          type="textarea"
          :rows="4"
        />
      </el-form-item>
      <el-form-item label="任职要求" prop="requirements">
        <el-input
          v-model="form.requirements"
          type="textarea"
          :rows="4"
        />
      </el-form-item>
      <el-form-item label="薪资范围" prop="salary_range">
        <el-input v-model="form.salary_range" />
      </el-form-item>
      <el-form-item label="工作地点" prop="location">
        <el-input v-model="form.location" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits(['submit-success'])

const formRef = ref()
const form = reactive({
  position_name: '',
  department: '',
  responsibilities: '',
  requirements: '',
  salary_range: '',
  location: ''
})

const rules = {
  position_name: [{ required: true, message: '职位名称不能为空', trigger: 'blur' }],
  responsibilities: [{ required: true, message: '岗位职责不能为空', trigger: 'blur' }],
  requirements: [{ required: true, message: '任职要求不能为空', trigger: 'blur' }]
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      emit('submit-success', form)
    }
  })
}
</script>
