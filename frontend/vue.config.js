const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  productionSourceMap: false,
  
  // 部署路径
  publicPath: process.env.NODE_ENV === 'production'
    ? '/'
    : '/',
  
  // 输出目录
  outputDir: 'dist',
  
  // 静态资源目录
  assetsDir: 'static',
  
  // 开发服务器配置
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  },
  
  // 禁用eslint
  lintOnSave: false,
  
  // 构建优化
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        minSize: 20000,
        maxSize: 250000,
        cacheGroups: {
          vendors: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: -10,
            chunks: 'initial'
          },
          elementPlus: {
            name: 'chunk-elementplus',
            test: /[\\/]node_modules[\\/]element-plus[\\/]/,
            priority: 20,
            chunks: 'all'
          },
          common: {
            name: 'chunk-common',
            minChunks: 2,
            priority: -20,
            chunks: 'initial',
            reuseExistingChunk: true
          }
        }
      }
    },
    performance: {
      hints: false
    }
  },
  
  // CSS配置
  css: {
    extract: process.env.NODE_ENV === 'production',
    sourceMap: false
  }
})
