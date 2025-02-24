<template>
  <div class="job-requirement-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="job-form"
      @submit.prevent="submitForm"
    >
      <el-form-item
        label="职位名称"
        prop="position_name"
      >
        <el-input 
          v-model="form.position_name"
          name="position_name"
        />
      </el-form-item>
      <el-form-item
        label="部门"
        prop="department"
      >
        <el-input 
          v-model="form.department"
          name="department"
        />
      </el-form-item>
      <el-form-item
        label="岗位职责"
        prop="responsibilities"
      >
        <el-input
          v-model="form.responsibilities"
          name="responsibilities"
          type="textarea"
          :rows="4"
        />
      </el-form-item>
      <el-form-item
        label="任职要求"
        prop="requirements"
      >
        <el-input
          v-model="form.requirements"
          name="requirements"
          type="textarea"
          :rows="4"
        />
      </el-form-item>
      <el-form-item
        label="薪资范围"
        prop="salary_range"
      >
        <el-input 
          v-model="form.salary_range"
          name="salary_range"
        />
      </el-form-item>
      <el-form-item
        label="工作地点"
        prop="location"
      >
        <el-input 
          v-model="form.location"
          name="location"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          class="submit-button"
          @click="submitForm"
        >
          提交
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

interface JobRequirementForm {
  position_name: string
  department: string
  responsibilities: string
  requirements: string
  salary_range: string
  location: string
}

const emit = defineEmits<{
  (e: 'submit-success', form: JobRequirementForm): void
}>()

const formRef = ref<FormInstance>()
const form = reactive<JobRequirementForm>({
  position_name: '',
  department: '',
  responsibilities: '',
  requirements: '',
  salary_range: '',
  location: ''
})

const rules: FormRules = {
  position_name: [{ required: true, message: '职位名称不能为空', trigger: 'blur' }],
  responsibilities: [{ required: true, message: '岗位职责不能为空', trigger: 'blur' }],
  requirements: [{ required: true, message: '任职要求不能为空', trigger: 'blur' }]
}

const submitForm = async () => {
  if (!formRef.value) {
    ElMessage.error('表单初始化失败')
    return
  }
  
  try {
    const valid = await formRef.value.validate()
    if (valid) {
      emit('submit-success', { ...form })
    }
  } catch (error) {
    ElMessage.error('表单验证失败，请检查必填项')
    console.error('Form validation failed:', error)
  }
}

// Expose for testing
defineExpose({
  form,
  formRef,
  submitForm
})
</script>
