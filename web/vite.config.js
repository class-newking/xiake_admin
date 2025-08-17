import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    // 添加自动路由生成功能
    {
      name: 'auto-generate-routes',
      configureServer(server) {
        // 开发服务器启动时生成路由
        generateRoutes()
      },
      buildStart() {
        // 构建时生成路由
        generateRoutes()
      }
    }
  ],
  // 添加服务器配置
  server: {
    // 设置开发服务器端口
    port: 8000,
    // 设置代理，将API请求转发到Django后端
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        secure: false
      }
    },
    // 添加缓存控制头，避免304问题
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    }
  },
  // 添加路径别名配置
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    }
  },
  // 构建配置，添加缓存破坏
  build: {
    rollupOptions: {
      output: {
        // 添加哈希值以避免缓存问题
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash].[ext]'
      }
    }
  }
})

// 自动生成路由配置的函数
function generateRoutes() {
  const viewsDir = path.resolve(__dirname, 'src/views')
  const routesFile = path.resolve(__dirname, 'src/router/auto-routes.js')

  // 确保目录存在
  const routerDir = path.dirname(routesFile)
  if (!fs.existsSync(routerDir)) {
    fs.mkdirSync(routerDir, { recursive: true })
  }

  // 生成路由配置
  const routes = scanViewsDirectory(viewsDir)
  const routeContent = `// 自动生成的路由配置文件
// 请勿手动修改此文件

export const autoRoutes = [
${routes.map(route => `  {
    path: '${route.path}',
    name: '${route.name}',
    component: () => import('${route.component}'),
    meta: {
      title: '${route.title}'
    }
  }`).join(',\n')}
]
`

  fs.writeFileSync(routesFile, routeContent, 'utf-8')
  console.log('路由配置已生成:', routesFile)
}

// 扫描views目录并生成路由配置
function scanViewsDirectory(dir, baseDir = '') {
  const routes = []
  const files = fs.readdirSync(dir)

  for (const file of files) {
    const filePath = path.join(dir, file)
    const stat = fs.statSync(filePath)
    const routePath = path.join(baseDir, file).replace(/\\/g, '/')

    if (stat.isDirectory()) {
      // 递归扫描子目录
      const subRoutes = scanViewsDirectory(filePath, routePath)
      routes.push(...subRoutes)
    } else if (file.endsWith('.vue')) {
      // 处理Vue组件文件
      const componentName = file.replace('.vue', '')
      const routeName = routePath.replace(/\//g, '-').replace('.vue', '')
      // 修复组件路径，确保正确引用
      const componentPath = `../views/${routePath}`

      // 修复路由路径，确保以 / 开头
      const finalRoutePath = routePath.replace('.vue', '')
      const pathWithSlash = finalRoutePath.startsWith('/') ? finalRoutePath : '/' + finalRoutePath

      routes.push({
        path: pathWithSlash,
        name: routeName,
        // 修复组件导入路径
        component: componentPath,
        title: componentName
      })
    }
  }

  return routes
}