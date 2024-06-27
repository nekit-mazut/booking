<template>
  <div id="app">
    <header>
      <nav>
        <ul>
          <!-- Для неавторизованных пользователей -->
          <li v-if="!authState.isAuthenticated">
            <router-link to="/">Главная</router-link>
          </li>
          <li v-if="!authState.isAuthenticated">
            <router-link to="/login">Войти</router-link>
          </li>
          <li v-if="!authState.isAuthenticated">
            <router-link to="/register">Регистрация</router-link>
          </li>

          <!-- Для авторизованных пользователей -->
          <li v-if="authState.isAuthenticated && !authState.isAdmin">
            <router-link to="/">Главная</router-link>
          </li>
          <li v-if="authState.isAuthenticated && !authState.isAdmin">
            <router-link to="/profile">Мой профиль</router-link>
          </li>
          <li v-if="authState.isAuthenticated && !authState.isAdmin">
            <router-link to="/search">Поиск номеров</router-link>
          </li>
          <li v-if="authState.isAuthenticated && !authState.isAdmin">
            <router-link to="/logout" @click="logout">Выйти</router-link>
          </li>
          <li v-if="authState.isAuthenticated && !authState.isAdmin">
            <router-link to="/createadmin">Создать Админа</router-link>
          </li>

          <!-- Для администраторов -->
          <li v-if="authState.isAuthenticated && authState.isAdmin">
            <router-link to="/">Главная</router-link>
          </li>
          <li v-if="authState.isAuthenticated && authState.isAdmin">
            <router-link to="/adminpanel">Админ панель</router-link>
          </li>
          <li v-if="authState.isAuthenticated && authState.isAdmin">
            <router-link to="/logout" @click="logout">Выйти</router-link>
          </li>
        </ul>
      </nav>
    </header>
    <router-view />
  </div>
</template>

<script>
import { onMounted } from 'vue';
import auth from './auth';

export default {
  name: 'App',
  setup() {
    onMounted(() => {
      auth.checkAuth();
    });

    const logout = async () => {
  try {
    localStorage.removeItem('token');
    console.log('User logged out successfully.');

    window.location.href = '/';
  } catch (error) {
    console.error('Error during logout:', error);
  }
};

    return {
      authState: auth.state,
      logout
    };
  }
};
</script>

<style>

@import './assets/css/style.css';


header {
  background-color: #333;
  color: #fff;
  padding: 10px 0;
}

nav ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  text-align: center;
}

nav ul li {
  display: inline;
  margin-right: 20px;
}

nav ul li a {
  color: #fff;
  text-decoration: none;
  font-size: 16px;
}
</style>