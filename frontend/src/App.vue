<!-- <template>
    <main class="container pt-4">
        <div>
            <router-link
                class=""
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});

</script>

<style scoped>
</style> -->

<template>
    <main class="container pt-4">
      <div>
        <router-link :to="{ name: 'MainPage' }">Main Page</router-link>
        |
        <router-link :to="{ name: 'ProfilePage' }">Profile Page</router-link>
        |
        <router-link :to="{ name: 'HobbiesPage' }">Hobbies Page</router-link>
        |
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
  
