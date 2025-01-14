<template>
    <div>
      <h2>Hobbies</h2>
      <div>
        <label for="newHobby">Add a New Hobby:</label>
        <input 
          id="newHobby"
          type="text"
          v-model="newHobby"
          @keyup.enter="addHobby"
        />
        <button @click="addHobby">Add Hobby</button>
      </div>
  
      <ul>
        <li v-for="hob in hobbies" :key="hob.id">{{ hob.name }}</li>
      </ul>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue'
  import { IHobby } from '../types'
  
  export default defineComponent({
    name: 'HobbiesPage',
    setup() {
      const hobbies = ref<IHobby[]>([])
      const newHobby = ref('')
  
      const fetchHobbies = async () => {
        try {
          const resp = await fetch('/api/hobbies/')
          if (!resp.ok) throw new Error('Failed to fetch hobbies')
          const data = await resp.json()
          hobbies.value = data.hobbies
        } catch (error) {
          console.error(error)
        }
      }
  
      const addHobby = async () => {
        const trimmed = newHobby.value.trim()
        if (!trimmed) return
        try {
          const resp = await fetch('/api/hobbies/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ hobby_name: trimmed }),
          })
          if (!resp.ok) throw new Error('Failed to add hobby')
          const result = await resp.json()
          // Refresh the list
          await fetchHobbies()
          newHobby.value = ''
        } catch (error) {
          console.error(error)
        }
      }
  
      onMounted(() => {
        fetchHobbies()
      })
  
      return {
        hobbies,
        newHobby,
        addHobby,
      }
    },
  })
  </script>
    <style scoped>
  h2 {
    margin-bottom: 1rem;
  }
  </style>
  
