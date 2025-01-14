<!-- <template>
  <div class="h1">
    {{ title }}
  </div>
</template>

<script lang="ts">
    import { defineComponent } from "vue";

    export default defineComponent({
        data() {
            return {
                title: "Main Page",
            }
        }
    })
</script>

<style scoped>
</style> -->

<template>
  <div>
    <h1>{{ title }}</h1>
    <p>This is the main page of the Hobbies SPA.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'MainPage',
  data() {
    return {
      title: 'MainPage',
    }
  },
})
</script>

<style scoped>
h1 {
  color: teal;
}
</style>

