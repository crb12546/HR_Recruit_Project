import { config } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, afterEach, vi } from 'vitest'
import type { Component, ComponentOptions } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'

// Setup Pinia
beforeEach(() => {
  setActivePinia(createPinia())
})

// Mock Element Plus icons
const icons: Record<string, Component> = {
  'upload-filled': { template: '<div>Upload Icon</div>' }
}

// Mock Element Plus components
const mockComponents: Record<string, ComponentOptions> = {
  'el-form': {
    template: '<form ref="form" class="el-form" @submit.prevent><slot></slot></form>',
    props: {
      model: {
        type: Object,
        required: true
      },
      rules: {
        type: Object as () => FormRules,
        default: () => ({})
      }
    },
    data() {
      return {
        formInstance: null as FormInstance | null
      }
    },
    methods: {
      validate(): Promise<boolean> {
        const rules = this.$props.rules || {}
        const model = this.$props.model || {}
        
        const hasEmptyRequired = Object.entries(rules).some(([field, fieldRules]) => {
          if (!fieldRules) return false
          const ruleArray = Array.isArray(fieldRules) ? fieldRules : [fieldRules]
          return ruleArray.some(rule => rule?.required && !model[field])
        })
        
        if (hasEmptyRequired) {
          ElMessage.error('表单验证失败，请检查必填项')
          return Promise.reject(new Error('表单验证失败，请检查必填项'))
        }
        
        return Promise.resolve(true)
      }
    }
  },
  'el-form-item': {
    template: '<div class="el-form-item"><label v-if="label" class="el-form-item__label">{{ label }}</label><slot></slot></div>',
    props: ['label', 'prop']
  },
  'el-input': {
    template: '<input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" :name="name" :type="type" />',
    props: {
      modelValue: [String, Number],
      name: String,
      type: {
        type: String,
        default: 'text'
      }
    }
  },
  'el-button': {
    template: '<button :class="[\'el-button\', type ? `el-button--${type}` : \'\', customClass]" @click="$emit(\'click\')"><slot></slot></button>',
    props: ['type', 'customClass']
  },
  'el-upload': { render: () => null },
  'el-progress': { render: () => null },
  'el-alert': { render: () => null },
  'el-tag': { render: () => null },
  'el-icon': { render: () => null }
}

// Global test setup
config.global.components = {
  ...icons,
  ...mockComponents
}

// Mock Element Plus
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn()
  }
}))

// Mock console.error to catch frontend errors during tests
const originalConsoleError = console.error
console.error = (...args) => {
  // Don't throw for form validation errors
  if (args[0] && typeof args[0] === 'string' && args[0].includes('Form validation failed')) {
    originalConsoleError(...args)
    return
  }
  originalConsoleError(...args)
  throw new Error('Console error was called during test')
}

// Setup browser console monitoring
beforeEach(() => {
  console.log('Test started:', expect.getState().currentTestName)
  vi.clearAllMocks()
})

afterEach(() => {
  console.log('Test finished:', expect.getState().currentTestName)
})
