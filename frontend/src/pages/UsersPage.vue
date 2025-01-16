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
      <li v-for="user in users" :key="user.id">
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
      <span class="page-info">Page {{ page }} of {{ totalPages }}</span>
      <button
        :disabled="!hasNext"
        @click="nextPage"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { IUser } from '../types';
import { getCsrfToken } from '../utils/csrf';

export default defineComponent({
  name: 'UsersPage',
  setup() {
    const users = ref<IUser[]>([]);
    const minAge = ref<number | null>(null);
    const maxAge = ref<number | null>(null);
    const page = ref(1);
    const hasNext = ref(false);
    const totalPages = ref(1);

    const fetchUsers = async () => {
      const params = new URLSearchParams();
      params.append('page', page.value.toString());
      if (minAge.value !== null) {
        params.append('min_age', minAge.value.toString());
      }
      if (maxAge.value !== null) {
        params.append('max_age', maxAge.value.toString());
      }

      try {
        const resp = await fetch('/api/users/?' + params.toString());
        if (!resp.ok) {
          throw new Error('Failed to fetch users');
        }
        const data = await resp.json();
        users.value = data.results;
        hasNext.value = data.has_next;
        page.value = data.page;
        totalPages.value = data.total_pages;
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
      if (hasNext.value) {
        page.value++;
        fetchUsers();
      }
    };

    const sendFriendRequest = async (toUserId: number) => {
      try {
        const resp = await fetch('/api/friend-requests/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
          },
          body: JSON.stringify({ to_user_id: toUserId }),
        });
        if (!resp.ok) {
          const errData = await resp.json();
          alert(errData.error || 'Error sending friend request');
          return;
        }
        alert('Friend request sent!');
      } catch (error) {
        console.error(error);
      }
    };

    onMounted(() => {
      fetchUsers();
    });

    return {
      users,
      minAge,
      maxAge,
      page,
      hasNext,
      totalPages,
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
