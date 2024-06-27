import { reactive } from 'vue';

const state = reactive({
  isAuthenticated: false,
  isAdmin: false,
});

const setAuth = (isAuthenticated, isAdmin) => {
  state.isAuthenticated = isAuthenticated;
  state.isAdmin = isAdmin;
};

const logout = () => {
  localStorage.removeItem('token');
  state.isAuthenticated = false;
  state.isAdmin = false;
};

const checkAuth = async () => {
  const token = localStorage.getItem('token');
  if (token) {
    try {
      const response = await fetch('http://localhost:5001/users/check_auth', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setAuth(data.isAuthenticated, data.isAdmin);
      }
    } catch (error) {
      console.error('Error checking authentication:', error);
    }
  }
};

export default {
  state,
  setAuth,
  logout,
  checkAuth,
};