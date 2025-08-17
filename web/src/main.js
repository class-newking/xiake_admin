import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import { autoRoutes } from "./router/auto-routes.js"
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: autoRoutes
})
createApp(App).use(router).use(ElementPlus).mount('#app')