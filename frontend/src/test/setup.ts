import { config } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { beforeEach, afterEach, expect } from 'vitest'

// Global test setup
config.global.plugins = [ElementPlus]

// Mock console.error to catch frontend errors during tests
const originalConsoleError = console.error
console.error = (...args) => {
  originalConsoleError(...args)
  throw new Error('Console error was called during test')
}

// Setup browser console monitoring
beforeEach(() => {
  console.log('Test started:', expect.getState().currentTestName)
})

afterEach(() => {
  console.log('Test finished:', expect.getState().currentTestName)
})
