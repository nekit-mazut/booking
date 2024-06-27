import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5001',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  checkAuth() {
    return apiClient.get('/users/check_auth');
  }
};