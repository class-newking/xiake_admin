// api 工具文件
const API_BASE_URL = '/api'

// 创建一个简单的 api 请求封装
const api = {
  // GET 请求
  get: async (url) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },

  // POST 请求
  post: async (url, data) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    return response.json()
  },

  // PUT 请求
  put: async (url, data) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    return response.json()
  },

  // DELETE 请求
  delete: async (url) => {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.json()
  },
}

// 添加请求拦截器
const request = async (url, options = {}) => {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return response.json()
}

// 重新实现各方法，使用统一的请求处理
api.get = (url) => request(url, { method: 'GET' })
api.post = (url, data) => request(url, { 
  method: 'POST',
  body: JSON.stringify(data) 
})
api.put = (url, data) => request(url, { 
  method: 'PUT',
  body: JSON.stringify(data) 
})
api.delete = (url) => request(url, { method: 'DELETE' })

export default api