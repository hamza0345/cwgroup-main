import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { IUser } from '../types';
import { getCsrfToken } from '../utils/csrf';

export const useUserStore = defineStore('userStore', () => {
  const currentUser = ref<IUser | null>(null);
  const users = ref<IUser[]>([]);
  const hasNext = ref(false);
  const totalPages = ref(1);

  async function fetchMe(userId: number) {
    try {
      const response = await fetch(`/api/users/${userId}/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      if (!response.ok) {
        console.error('Error fetching user profile');
        return;
      }
      currentUser.value = await response.json();
    } catch (error) {
      console.error('Error in fetchMe:', error);
    }
  }

  async function fetchCurrentUser() {
    try {
      const response = await fetch('/api/users/current/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      if (!response.ok) {
        console.error('Error fetching current user');
        return;
      }
      currentUser.value = await response.json();
    } catch (error) {
      console.error('Error in fetchCurrentUser:', error);
    }
  }

  async function fetchUsers(params: URLSearchParams) {
    try {
      const response = await fetch(`/api/users/?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      if (!response.ok) {
        console.error('Error fetching users');
        return;
      }
      const data = await response.json();
      users.value = data.users;
      hasNext.value = data.has_next;
      totalPages.value = data.total_pages;
    } catch (error) {
      console.error('Error in fetchUsers:', error);
    }
  }

  async function updateProfile(userId: number, newUserData: Partial<IUser>) {
    try {
      const response = await fetch(`/api/users/${userId}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify(newUserData),
      });
      if (!response.ok) {
        console.error('Profile update failed');
        throw new Error(await response.text());
      }
      return await response.json();
    } catch (error) {
      console.error('Error in updateProfile:', error);
      throw error;
    }
  }

  async function sendFriendRequest(toUserId: number) {
    try {
      const response = await fetch('/api/friend-requests/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ to_user_id: toUserId }),
      });
      if (!response.ok) {
        throw new Error('Failed to send friend request');
      }
      return await response.json();
    } catch (error) {
      console.error('Error in sendFriendRequest:', error);
      throw error;
    }
  }

  return {
    currentUser,
    users,
    hasNext,
    totalPages,
    fetchMe,
    fetchCurrentUser,
    fetchUsers,
    updateProfile,
    sendFriendRequest,
  };
});
