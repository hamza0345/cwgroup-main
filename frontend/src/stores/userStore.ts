import { defineStore } from 'pinia'
import { IUser } from '../types'

export const useUserStore = defineStore('userStore', {
  state: () => ({
    currentUser: null as IUser | null,
  }),
  actions: {
    async fetchCurrentUser() {
      // For example, if you have an endpoint like /api/users/<my_id>/ 
      // But you might need to know the logged-in user's ID from a cookie or session.
      // This is just an example, adapt to your actual logic.
      try {
        const response = await fetch('/api/users/1')
        if (!response.ok) throw new Error('Failed to fetch current user')
        const data: IUser = await response.json()
        this.currentUser = data
      } catch (error) {
        console.error(error)
      }
    },
  },
})
