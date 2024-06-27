<template>
  <div>
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" v-model="username" required>
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" required>
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" v-model="password" required>
      </div>
      <div>
        <label for="confirmPassword">Подтвердите пароль:</label>
        <input type="password" v-model="confirmPassword" required>
      </div>
      <button type="submit">Зарегистрироваться</button>
    </form>

    <!-- Всплывающее окно для ввода кода подтверждения -->
    <div v-if="confirmationRequired" class="confirmation-popup">
      <h3>Подтверждение почты</h3>
      <form @submit.prevent="confirmEmail">
        <div>
          <label for="confirmationCode">Код подтверждения:</label>
          <input type="text" v-model="confirmationCode" required>
        </div>
        <button type="submit">Подтвердить</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const username = ref('');
    const email = ref('');
    const password = ref('');
    const confirmPassword = ref('');
    const confirmationCode = ref('');
    const confirmationRequired = ref(false);
    const originalCode = ref('');

    const register = async () => {
      if (password.value !== confirmPassword.value) {
        alert('Пароли не совпадают');
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:5001/users/send_confirmation', {
          username: username.value,
          email: email.value,
          password: password.value
        });
        const data = response.data;
        originalCode.value = data.confirmation_code;
        confirmationRequired.value = true;
      } catch (error) {
        console.error('Error during registration:', error);
      }
    };

    const confirmEmail = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5001/confirm', {
          username: username.value,
          email: email.value,
          password: password.value,
          original_code: originalCode.value,
          confirmation_code: confirmationCode.value
        });
        const data = response.data;
        alert('Регистрация завершена!');
        localStorage.setItem('token', data.access_token);
        router.push('/');
      } catch (error) {
        console.error('Error during email confirmation:', error);
      }
    };

    return {
      username,
      email,
      password,
      confirmPassword,
      confirmationCode,
      confirmationRequired,
      register,
      confirmEmail
    };
  }
};
</script>

<style scoped>
.register {
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
  background-color: #28a745;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #218838;
}
</style>