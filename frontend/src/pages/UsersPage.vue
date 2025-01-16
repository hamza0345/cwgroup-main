<template>
  <div>
    <h2>Users</h2>
    <div class="filters">
      <label>Min Age:
        <input type="number" v-model="minAge" />
      </label>
      <label>Max Age:
        <input type="number" v-model="maxAge" />
      </label>
      <button @click="applyFilter">Apply Filter</button>
    </div>

    <ul>
      <li v-for="user in userStore.users" :key="user.id">
        <strong>{{ user.name }}</strong>
        ({{ user.common_hobbies }} common hobbies)
        <button @click="sendFriendRequest(user.id)">Send Friend Request</button>
      </li>
    </ul>

    <div class="pagination">
      <button 
        :disabled="page <= 1"
        @click="prevPage"
      >
        Previous
      </button>
      <span>Page {{ page }} of {{ userStore.totalPages }}</span>
      <button
        :disabled="!userStore.hasNext"
        @click="nextPage"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';

export default defineComponent({
  name: 'UsersPage',
  setup() {
    const userStore = useUserStore();
    const minAge = ref<number | null>(null);
    const maxAge = ref<number | null>(null);
    const page = ref(1);

    const fetchUsers = async () => {
      const params = new URLSearchParams();
      params.append('page', page.value.toString());
      if (minAge.value) params.append('min_age', minAge.value.toString());
      if (maxAge.value) params.append('max_age', maxAge.value.toString());

      try {
        await userStore.fetchUsers(params);
      } catch (error) {
        console.error(error);
      }
    };

    const applyFilter = () => {
      page.value = 1;
      fetchUsers();
    };

    const prevPage = () => {
      if (page.value > 1) {
        page.value--;
        fetchUsers();
      }
    };

    const nextPage = () => {
      if (userStore.hasNext) {
        page.value++;
        fetchUsers();
      }
    };

    const sendFriendRequest = async (toUserId: number) => {
      try {
        await userStore.sendFriendRequest(toUserId);
        alert('Friend request sent!');
      } catch (error) {
        console.error(error);
      }
    };

    onMounted(() => {
      fetchUsers();
    });

    return {
      userStore,
      minAge,
      maxAge,
      page,
      applyFilter,
      prevPage,
      nextPage,
      sendFriendRequest,
    };
  },
});
</script>

<style scoped>
.filters {
  margin-bottom: 1em;
}
.pagination {
  margin-top: 1em;
}
</style>
