import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ElMessage } from 'element-plus'
import ResumeDetail from '@/components/resume/ResumeDetail.vue'
import { createTestingPinia } from '@pinia/testing'
import { useResumeStore } from '@/store/resume'
import type { Resume } from '@/types'

vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: { id: '1' }
  }),
  useRouter: () => ({
    push: vi.fn()
  })
}))

vi.mock('element-plus', () => ({
  ElMessage: {
    error: vi.fn(),
    success: vi.fn()
  }
}))

describe('简历详情组件', () => {
  const mockResume = {
    id: 1,
    candidate_name: '张三',
    file_url: 'http://example.com/resume.pdf',
    file_type: 'application/pdf',
    ocr_content: '简历原文内容',
    parsed_content: '解析后内容',
    talent_portrait: '人才画像描述',
    tags: [
      { id: 1, name: 'Python', category: '技能' },
      { id: 2, name: 'Vue.js', category: '技能' }
    ],
    created_at: '2025-02-23T08:00:00Z',
    updated_at: '2025-02-23T08:00:00Z'
  }

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('应该正确显示简历详情', async () => {
    const wrapper = mount(ResumeDetail, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            initialState: {
              resume: {
                resumes: [mockResume]
              }
            }
          })
        ]
      }
    })

    const store = useResumeStore()
    // @ts-ignore
    store.getResumeById.mockResolvedValue(mockResume)

    await wrapper.vm.$nextTick()

    expect(wrapper.text()).toContain('张三')
    expect(wrapper.text()).toContain('人才画像描述')
    expect(wrapper.findAll('.el-tag')).toHaveLength(2)
  })

  it('应该处理标签删除', async () => {
    const wrapper = mount(ResumeDetail, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            initialState: {
              resume: {
                resumes: [mockResume]
              }
            }
          })
        ]
      }
    })

    const store = useResumeStore()
    // @ts-ignore
    store.getResumeById.mockResolvedValue(mockResume)
    // @ts-ignore
    store.removeTagFromResume.mockResolvedValue({
      ...mockResume,
      tags: [mockResume.tags[1]]
    })

    await wrapper.vm.$nextTick()
    
    const closeButton = wrapper.find('.el-tag .el-tag__close')
    await closeButton.trigger('click')

    expect(store.removeTagFromResume).toHaveBeenCalledWith(1, 1)
    expect(ElMessage.success).toHaveBeenCalledWith('标签移除成功')
  })

  it('应该处理简历下载', async () => {
    const wrapper = mount(ResumeDetail, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn,
            initialState: {
              resume: {
                resumes: [mockResume]
              }
            }
          })
        ]
      }
    })

    const store = useResumeStore()
    // @ts-ignore
    store.getResumeById.mockResolvedValue(mockResume)

    await wrapper.vm.$nextTick()
    
    const windowSpy = vi.spyOn(window, 'open')
    const downloadButton = wrapper.find('button:contains("下载简历")')
    await downloadButton.trigger('click')

    expect(windowSpy).toHaveBeenCalledWith('http://example.com/resume.pdf', '_blank')
  })

  it('应该在加载失败时显示错误信息', async () => {
    const wrapper = mount(ResumeDetail, {
      global: {
        plugins: [
          createTestingPinia({
            createSpy: vi.fn
          })
        ]
      }
    })

    const store = useResumeStore()
    // @ts-ignore
    store.getResumeById.mockRejectedValue(new Error('加载失败'))

    await wrapper.vm.$nextTick()
    expect(ElMessage.error).toHaveBeenCalledWith('获取简历详情失败')
  })
})
