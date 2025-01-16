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
      <li v-for="hob in hobbyStore.hobbies" :key="hob.id">
        {{ hob.name }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useHobbyStore } from '../stores/hobbyStore';

export default defineComponent({
  name: 'HobbiesPage',
  setup() {
    const hobbyStore = useHobbyStore();
    const newHobby = ref('');

    const fetchHobbies = async () => {
      try {
        await hobbyStore.fetchHobbies();
      } catch (error) {
        console.error(error);
      }
    };

    const addHobby = async () => {
      const trimmed = newHobby.value.trim();
      if (!trimmed) return;
      try {
        await hobbyStore.addHobby(trimmed);
        newHobby.value = '';
      } catch (error) {
        console.error(error);
      }
    };

    onMounted(() => {
      fetchHobbies();
    });

    return {
      hobbyStore,
      newHobby,
      addHobby,
    };
  },
});
</script>

<style scoped>
h2 {
  margin-bottom: 1rem;
}
</style>
