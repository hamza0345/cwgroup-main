<template>
  <div class="main-page">
    <header>
      <h1>{{ title }}</h1>
    </header>
    <main>
      <p>Welcome to the Hobbies Single Page Application. Explore your interests and discover new hobbies!</p>
      
      <div v-if="userStore.currentUser">
        <h3>Pending Friend Requests</h3>
        <ul>
          <li v-for="fr in userStore.pendingFriendRequests" :key="fr.id">
            From: {{ fr.from_user }}
            <button @click="acceptFR(fr.id)">Accept</button>
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';

export default defineComponent({
  name: 'MainPage',
  data() {
    return {
      title: 'Welcome to the Hobbies SPA',
    };
  },
  setup() {
    const userStore = useUserStore();

    onMounted(async () => {
      // If user is logged in, fetch pending friend requests
      if (userStore.currentUser) {
        await userStore.fetchFriendRequests();
      }
    });

    const acceptFR = async (friendRequestId: number) => {
      try {
        await userStore.acceptFriendRequest(friendRequestId);
        // Re-fetch friend requests to remove the one we just accepted
        await userStore.fetchFriendRequests();
        alert('Friend request accepted!');
      } catch (err) {
        console.error(err);
        alert('Could not accept friend request');
      }
    };

    return {
      userStore,
      acceptFR,
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
ul {
  list-style: none;
  padding: 0;
}
button {
  margin-left: 10px;
  border: none;
  border-radius: 3px;
  color: #fff;
  cursor: pointer;
}
</style>
