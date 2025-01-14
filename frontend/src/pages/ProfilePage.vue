<template>
    <div>
      <h2>Profile</h2>
      <div v-if="user">
        <label>Name:
          <input v-model="editName" />
        </label>
        <label>Email:
          <input v-model="editEmail" />
        </label>
        <label>Date of Birth:
          <input type="date" v-model="editDOB" />
        </label>
        <div>
          <label>Hobbies (comma-separated):
            <input v-model="editHobbies" />
          </label>
        </div>
        <button @click="saveProfile">Save</button>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue'
  import { IUser } from '../types'
  
  export default defineComponent({
    name: 'ProfilePage',
    setup() {
      const user = ref<IUser | null>(null)
      const editName = ref('')
      const editEmail = ref('')
      const editDOB = ref('')
      const editHobbies = ref('')
  
      const fetchProfile = async () => {
        // Suppose the current user is user ID 1 or you determine ID dynamically
        const response = await fetch('/api/users/1')
        if (response.ok) {
          const data: IUser = await response.json()
          user.value = data
          editName.value = data.name
          editEmail.value = data.email
          editDOB.value = data.date_of_birth || ''
          editHobbies.value = data.hobbies.join(', ')
        }
      }
  
      const saveProfile = async () => {
        if (!user.value) return
        // Convert comma-separated list to array
        const hobbiesArray = editHobbies.value
          .split(',')
          .map(h => h.trim())
          .filter(Boolean)
  
        const payload = {
          name: editName.value,
          email: editEmail.value,
          date_of_birth: editDOB.value || null,
          hobbies: hobbiesArray,
        }
  
        const resp = await fetch(`/api/users/${user.value.id}/`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        })
  
        if (!resp.ok) {
          alert('Failed to update user profile')
          return
        }
        alert('Profile updated')
        await fetchProfile()
      }
  
      onMounted(() => {
        fetchProfile()
      })
  
      return {
        user,
        editName,
        editEmail,
        editDOB,
        editHobbies,
        saveProfile,
      }
    },
  })
  </script>
  