# 构建阶段
FROM node:16-alpine as build-stage

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目文件
COPY . .

# 构建应用
ARG VUE_APP_API_BASE_URL
ENV VUE_APP_API_BASE_URL=${VUE_APP_API_BASE_URL}
RUN npm run build

# 生产阶段
FROM nginx:alpine as production-stage

# 复制构建结果到Nginx目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
