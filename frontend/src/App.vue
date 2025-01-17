<template>
    <main class="container pt-4">
      <div class="mb-4 text-center link-holder">
        <router-link :to="{ name: 'MainPage' }">Main Page</router-link>
        <router-link :to="{ name: 'ProfilePage' }">Profile Page</router-link>
        <router-link :to="{ name: 'HobbiesPage' }">Hobbies Page</router-link>
        <router-link :to="{ name: 'UsersPage' }">Users Page</router-link>
      </div>
      <RouterView class="flex-shrink-0" />
    </main>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue'
  import { RouterView, RouterLink } from 'vue-router'
  
  export default defineComponent({
    name: 'App',
    components: { RouterView, RouterLink },
  })
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: 0 auto;
  }
  </style>
  
