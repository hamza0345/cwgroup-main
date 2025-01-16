<template>
  <div class="main-page">
    <header>
      <h1>{{ title }}</h1>
    </header>
    <main>
      <p>Welcome to the Hobbies Single Page Application. Explore your interests and discover new hobbies!</p>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'MainPage',
  data() {
    return {
      title: 'Welcome to the Hobbies SPA',
    };
  },
});
</script>

<style scoped>
.main-page {
  text-align: center;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

header h1 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 10px;
}

main p {
  color: #555;
  font-size: 1.2rem;
  line-height: 1.5;
}
</style>
