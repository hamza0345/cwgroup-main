import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import MainPage from '../pages/MainPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import HobbiesPage from '../pages/HobbiesPage.vue'
import UsersPage from '../pages/UsersPage.vue'
import { useUserStore } from '../stores/userStore'
import OtherPage from '../pages/OtherPage.vue'

const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'MainPage', component: MainPage },
  { path: '/profile', name: 'ProfilePage', component: ProfilePage },
  { path: '/hobbies', name: 'HobbiesPage', component: HobbiesPage },
  { path: '/users', name: 'UsersPage', component: UsersPage },
  { path: '/other', name: 'OtherPage', component: OtherPage }, // Add this
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Example navigation guard if you want to ensure user is fetched:
router.beforeEach(async (to, from) => {
  const userStore = useUserStore()
  if (!userStore.currentUser) {
    await userStore.fetchCurrentUser()
  }
  return true
})

export default router
