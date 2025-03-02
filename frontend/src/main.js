import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import api from './api'

// 创建Vue应用实例
const app = createApp(App)

// 使用插件
app.use(router)
app.use(ElementPlus, {
  locale: zhCn
})

// 全局API服务
app.config.globalProperties.$http = api

// 挂载应用
app.mount('#app')
