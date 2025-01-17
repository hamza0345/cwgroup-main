import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

import MainPage from '../pages/MainPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import HobbiesPage from '../pages/HobbiesPage.vue';
import UsersPage from '../pages/UsersPage.vue';
import OtherPage from '../pages/OtherPage.vue';

import { useUserStore } from '../stores/userStore';

const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'MainPage', component: MainPage },
  { path: '/profile', name: 'ProfilePage', component: ProfilePage },
  { path: '/hobbies', name: 'HobbiesPage', component: HobbiesPage },
  { path: '/users', name: 'UsersPage', component: UsersPage },
  { path: '/other', name: 'OtherPage', component: OtherPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach(async () => {
  const userStore = useUserStore();
  if (!userStore.currentUser) {
    await userStore.fetchCurrentUser();
  }
  return true;
});

export default router;
