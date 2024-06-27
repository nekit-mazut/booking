<template>
  <div class="profile">
    <h2>Профиль пользователя</h2>
    <div v-if="isLoading">
      <p>Загрузка данных...</p>
    </div>
    <div v-else>
      <h3>Бронирования пользователя</h3>
      <div v-if="bookings.length === 0">
        <p>У вас нет бронирований.</p>
      </div>
      <div v-else>
        <div v-for="booking in bookings" :key="booking.id" class="booking-card">
          <p><strong>Номер бронирования:</strong> {{ booking.id }}</p>
          <p><strong>Номер комнаты:</strong> {{ booking.room_id }}</p>
          <p><strong>Дата заезда:</strong> {{ formatBookingDate(booking.check_in) }}</p>
          <p><strong>Дата выезда:</strong> {{ formatBookingDate(booking.check_out) }}</p>
          <p><strong>Итоговая цена:</strong> {{ booking.total_price }}</p>
          <hr>
        </div>
      </div>
      <h3>Изменение данных</h3>
      <div>
        <button @click="showChangeUsernameForm">Изменить имя пользователя</button>
        <button @click="showChangeEmailForm">Изменить email</button>
        <button @click="showChangePasswordForm">Изменить пароль</button>
      </div>
      <div v-if="changeUsernameVisible">
        <form @submit.prevent="changeUsername">
          <div>
            <label for="newUsername">Новое имя пользователя:</label>
            <input type="text" id="newUsername" v-model="newUsername">
          </div>
          <button type="submit">Сохранить</button>
        </form>
      </div>
      <div v-if="changeEmailVisible">
        <form @submit.prevent="changeEmail">
          <div>
            <label for="newEmail">Новый email:</label>
            <input type="email" id="newEmail" v-model="newEmail">
          </div>
          <div>
            <label for="currentPassword">Текущий пароль:</label>
            <input type="password" id="currentPassword" v-model="currentPassword">
          </div>
          <button type="submit">Сменить email</button>
        </form>
      </div>
      <div v-if="changePasswordVisible">
        <form @submit.prevent="changePassword">
          <div>
            <label for="newPassword">Новый пароль:</label>
            <input type="password" id="newPassword" v-model="newPassword">
          </div>
          <div>
            <label for="currentPassword">Текущий пароль:</label>
            <input type="password" id="currentPassword" v-model="currentPassword">
          </div>
          <button type="submit">Сменить пароль</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { format } from 'date-fns';

export default {
  data() {
    return {
      isLoading: false,
      bookings: [],
      userId: null,
      newUsername: '',
      newEmail: '',
      currentPassword: '',
      newPassword: '',
      changeUsernameVisible: false,
      changeEmailVisible: false,
      changePasswordVisible: false
    };
  },
  mounted() {
    this.getUserIdAndFetchBookings();
  },
  methods: {
    async getUserIdAndFetchBookings() {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('Отсутствует токен авторизации.');
        return;
      }

      try {
        const decodedToken = jwtDecode(token);
        this.userId = decodedToken.sub;
        await this.fetchUserBookings();
      } catch (error) {
        console.error('Ошибка при декодировании токена:', error);
      }
    },
    async fetchUserBookings() {
      try {
        this.isLoading = true;
        const response = await axios.get(`http://localhost:5000/bookings/user/${this.userId.id}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.bookings = response.data.bookings;
      } catch (error) {
        console.error('Ошибка при получении бронирований:', error);
      } finally {
        this.isLoading = false;
      }
    },
    formatBookingDate(date) {
      return format(new Date(date), 'dd.MM.yyyy');
    },
    showChangeUsernameForm() {
      this.changeUsernameVisible = true;
      this.changeEmailVisible = false;
      this.changePasswordVisible = false;
      this.newUsername = '';
      this.newEmail = '';
      this.currentPassword = '';
      this.newPassword = '';
    },
    showChangeEmailForm() {
      this.changeUsernameVisible = false;
      this.changeEmailVisible = true;
      this.changePasswordVisible = false;
      this.newUsername = '';
      this.newEmail = '';
      this.currentPassword = '';
      this.newPassword = '';
    },
    showChangePasswordForm() {
      this.changeUsernameVisible = false;
      this.changeEmailVisible = false;
      this.changePasswordVisible = true;
      this.newUsername = '';
      this.newEmail = '';
      this.currentPassword = '';
      this.newPassword = '';
    },
    async changeUsername() {
      try {
        const response = await axios.put(`http://localhost:5001/users/change_username/${this.userId.id}`, { username: this.newUsername }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log('Имя пользователя изменено:', response.data);
      } catch (error) {
        console.error('Ошибка при изменении имени пользователя:', error);
      }
    },
    async changeEmail() {
      try {
        const response = await axios.put(`http://localhost:5001/users/${this.userId.id}/change_email`, {
          email: this.newEmail,
          currentPassword: this.currentPassword
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log('Email пользователя изменен:', response.data);
      } catch (error) {
        console.error('Ошибка при изменении email:', error);
      }
    },
    async changePassword() {
      try {
        const response = await axios.put(`http://localhost:5001/users/${this.userId.id}/change_password`, {
          current_password: this.currentPassword,
          new_password: this.newPassword
        }, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log('Пароль изменен:', response.data);
      } catch (error) {
        console.error('Ошибка при изменении пароля:', error);
      }
    }
  }
};
</script>

<style scoped>
.profile {
  margin: 20px;
}
.booking-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
form {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  width: 50%;
}
form div {
  margin-bottom: 10px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input[type="text"],
input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 5px;
  font-size: 16px;
}
button[type="submit"] {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}
button[type="submit"]:hover {
  background-color: #0056b3;
}
</style>