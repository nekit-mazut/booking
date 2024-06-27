import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import auth from './auth';

const app = createApp(App);

app.provide('auth', auth);

app.use(router).mount('#app');