<template>
  <div>
    <h2>Hobbies</h2>
    <div>
      <label for="newHobby">Add a New Hobby:</label>
      <input
        id="newHobby"
        type="text"
        v-model="newHobby"
        @keyup.enter="createHobby"
      />
      <button @click="createHobby">Add Hobby</button>
    </div>

    <ul>
      <li v-for="hob in hobbyStore.hobbies" :key="hob.id">
        {{ hob.name }}
        <!-- Button to add the hobby to the user's own hobbies -->
        <button @click="addHobbyToUser(hob.name)" style="margin-left:10px;">
          Add to My Hobbies
        </button>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useHobbyStore } from '../stores/hobbyStore';
import { useUserStore } from '../stores/userStore';

export default defineComponent({
  name: 'HobbiesPage',
  setup() {
    const hobbyStore = useHobbyStore();
    const userStore = useUserStore();
    const newHobby = ref<string>('');

    const fetchHobbies = async () => {
      try {
        await hobbyStore.fetchHobbies();
      } catch (error) {
        console.error(error);
      }
    };

    const createHobby = async () => {
      const trimmed = newHobby.value.trim();
      if (!trimmed) return;
      try {
        await hobbyStore.addHobby(trimmed);
        newHobby.value = '';
      } catch (error) {
        console.error(error);
      }
    };

    const addHobbyToUser = async (hobbyName: string) => {
      if (!userStore.currentUser) {
        alert('You need to be logged in to add hobbies to your profile.');
        return;
      }
      try {
        await userStore.addHobbyToCurrentUser(hobbyName);
        alert(`"${hobbyName}" added to your profile!`);
      } catch (error) {
        console.error(error);
        alert('Failed to add hobby to user.');
      }
    };

    onMounted(() => {
      fetchHobbies();
    });

    return {
      hobbyStore,
      userStore,
      newHobby,
      createHobby,
      addHobbyToUser,
    };
  },
});
</script>

<style scoped>
h2 {
  margin-bottom: 1rem;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin: 0.5rem 0;
}
button {
  cursor: pointer;
  color: #fff;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
}
</style>
