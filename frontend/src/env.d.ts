/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const vueComponent: DefineComponent<Record<string, unknown>, Record<string, unknown>, unknown>
  export default vueComponent
}

declare module 'element-plus/dist/locale/zh-cn.mjs'
