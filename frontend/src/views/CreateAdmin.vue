<template>
  <div>
    <h2>Create Admin</h2>
    <form @submit.prevent="createAdmin">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="formData.username" required>
      <br><br>
      <label for="email">Email:</label>
      <input type="email" id="email" v-model="formData.email" required>
      <br><br>
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="formData.password" required>
      <br><br>
      <button type="submit">Create Admin</button>
    </form>
    <div v-if="adminCreated">
      <h3>Admin Created Successfully!</h3>
      <p>ID: {{ adminData.id }}</p>
      <p>Username: {{ adminData.username }}</p>
      <p>Email: {{ adminData.email }}</p>
      <p>Admin Status: {{ adminData.is_admin }}</p>
      <p>Created At: {{ adminData.created_at }}</p>
    </div>
    <div v-if="error">
      <h3>Error:</h3>
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: ''
      },
      adminCreated: false,
      adminData: {},
      error: false,
      errorMessage: ''
    };
  },
  methods: {
    async createAdmin() {
      try {

        const token = localStorage.getItem('token');

        if (!token) {
          throw new Error('No token found. Please log in again.');
        }

        const headers = {
          Authorization: `Bearer ${token}`
        };

        const response = await axios.post('http://localhost:5001/users/admin', this.formData, { headers });

        this.adminData = response.data;
        this.adminCreated = true;
        this.error = false;
      } catch (error) {
        this.error = true;
        this.errorMessage = error.response ? error.response.data.error || 'Failed to create admin.' : error.message;
        console.error(error);
      }
    }
  }
};
</script>

<style>
/* Add your styles here */
</style>