<!-- <template>
    <div class="h3">
      {{ title }}
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Other Page",
              }
          }
      })
  </script>
  
  <style scoped>
  </style>
   -->

<template>
  <div>
    <h2>{{ title }}</h2>
    <p>This is another page in the Hobbies SPA.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'OtherPage',
  data() {
    return {
      title: 'OtherPage',
    }
  },
})
</script>

<style scoped>
h2 {
  color: #555;
}
</style>
