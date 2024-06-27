import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import LoginForm from './views/LoginForm.vue';
import RegisterForm from './views/RegisterForm.vue';
import RoomSearch from './views/RoomSearch.vue';
import SearchResults from './views/SearchResults.vue';
import ProfileView from './views/ProfileView.vue';
import AdminPanel from './views/AdminPanel.vue';
import CreateAdmin from './views/CreateAdmin.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: LoginForm },
  { path: '/register', component: RegisterForm },
  { path: '/search', component: RoomSearch },
  { path: '/results', component: SearchResults, props: route => ({ rooms: route.query.rooms }) },
  { path: '/profile', component: ProfileView },
  { path: '/adminpanel', component: AdminPanel },
  { path: '/createadmin', component: CreateAdmin }

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;