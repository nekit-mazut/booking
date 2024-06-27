<template>
  <div>
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" v-model="username" required>
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email">
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" v-model="password" required>
      </div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <button type="submit">Войти</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import auth from '../auth';

export default {
  setup() {
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const errorMessage = ref('');
    const router = useRouter();

    const login = async () => {
      try {
        const response = await fetch('http://localhost:5001/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: username.value,
            email: email.value,
            password: password.value
          })
        });
        const data = await response.json();
        if (response.ok) {
          localStorage.setItem('token', data.access_token);
          auth.setAuth(true, data.isAdmin);
          router.push('/');
        } else {
          errorMessage.value = data.message;
        }
      } catch (error) {
        console.error('Error during login:', error);
        errorMessage.value = 'Ошибка при попытке входа';
      }
    };

    return {
      username,
      email,
      password,
      errorMessage,
      login,
    };
  }
};
</script>

<style scoped>
/* Стили для страницы входа */
.login {
  text-align: center;
  margin-top: 20px;
}

form {
  display: inline-block;
  text-align: left;
}

form div {
  margin-bottom: 10px;
}

form label {
  display: block;
}

form input {
  width: 200px;
  padding: 5px;
  margin-top: 5px;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  margin-top: 5px;
}
</style>