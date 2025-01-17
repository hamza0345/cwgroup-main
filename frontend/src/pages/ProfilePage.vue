<template>
  <div class="profile-page">
    <h2>Profile</h2>
    <div v-if="userStore.currentUser">
      <label>
        Name:
        <input v-model="editName" />
      </label>
      <label>
        Email:
        <input v-model="editEmail" />
      </label>
      <label>
        Date of Birth:
        <input type="date" v-model="editDOB" />
      </label>
      <div>
        <label>
          Hobbies (comma-separated):
          <input v-model="editHobbies" />
        </label>
      </div>

      <!-- OPTIONAL: Fields for changing username and password -->
      <div>
        <label>
          Username:
          <input id="username-input" v-model="editUsername" />
        </label>
      </div>
      <div>
        <label>
          New Password:
          <input id="password-input" type="password" v-model="editPassword" />
        </label>
      </div>

      <button @click="saveProfile">Save</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useUserStore } from '../stores/userStore';
import { useHobbyStore } from '../stores/hobbyStore';

export default defineComponent({
  name: 'ProfilePage',
  setup() {
    const userStore = useUserStore();
    const hobbyStore = useHobbyStore();

    const editName = ref<string>('');
    const editEmail = ref<string>('');
    const editDOB = ref<string>('');
    const editHobbies = ref<string>('');

    // For changing username and password
    const editUsername = ref<string>('');
    const editPassword = ref<string>('');

    onMounted(async () => {
      const userId = userStore.currentUser?.id ||
        parseInt(localStorage.getItem('myUserId') || '0', 10);

      if (userId) {
        await userStore.fetchMe(userId);
        await hobbyStore.fetchHobbies();

        if (userStore.currentUser) {
          editName.value = userStore.currentUser.name;
          editEmail.value = userStore.currentUser.email;
          editDOB.value = userStore.currentUser.date_of_birth || '';
          editHobbies.value = userStore.currentUser.hobbies.join(', ');
          editUsername.value = userStore.currentUser.username;
        }
      }
    });

    const saveProfile = async () => {
      if (!userStore.currentUser) return;

      const hobbiesArray = editHobbies.value
        .split(',')
        .map(h => h.trim())
        .filter(Boolean);

      try {
        await userStore.updateProfile(userStore.currentUser.id, {
          name: editName.value,
          email: editEmail.value,
          date_of_birth: editDOB.value || undefined,
          hobbies: hobbiesArray,
          username: editUsername.value || undefined,
          password: editPassword.value || undefined,
        });
        alert('Profile updated successfully!');
      } catch (error) {
        console.error(error);
        alert('Failed to update profile.');
      }
    };

    return {
      userStore,
      hobbyStore,
      editName,
      editEmail,
      editDOB,
      editHobbies,
      editUsername,
      editPassword,
      saveProfile,
    };
  },
});
</script>

<style scoped>
.profile-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}
label {
  display: block;
  margin-bottom: 10px;
  font-size: 1rem;
}
input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 15px;
  font-size: 1rem;
  border: 1px solid ;
  border-radius: 4px;
}
button {
  padding: 10px 15px;
  font-size: 1rem;

  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
