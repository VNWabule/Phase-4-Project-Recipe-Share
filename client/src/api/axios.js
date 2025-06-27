import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5555',
  withCredentials: true, // to send cookies (refresh_token)
});

// 🔐 Attach access token to outgoing requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 🔁 Refresh token logic
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

// 🔄 Response interceptor to handle 401s
api.interceptors.response.use(
  res => res,
  async err => {
    const originalRequest = err.config;

    if (err.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch(error => {
            return Promise.reject(error);
          });
      }

      isRefreshing = true;

      try {
        const refreshResponse = await api.post('/refresh');
        const newToken = refreshResponse.data.access_token;

        localStorage.setItem('access_token', newToken);
        api.defaults.headers.common.Authorization = `Bearer ${newToken}`;
        processQueue(null, newToken);

        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(err);
  }
);

// ✅ Your existing function
export async function checkSession() {
  const response = await api.get('/check_session');
  return response.data;
}

export default api;
