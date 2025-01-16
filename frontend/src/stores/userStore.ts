import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { IUser } from '../types';
import { getCsrfToken } from '../utils/csrf';

export const useUserStore = defineStore('userStore', () => {
  // We call this `currentUser` so the router can check `currentUser`.
  const currentUser = ref<IUser | null>(null);

  // Fetch user by ID (GET /api/users/<id>/)
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

  // Fetch the currently logged-in user (e.g. GET /api/users/current/)
  // Adjust the endpoint to however your backend provides the logged-in user data.
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

  // Update user’s data (PUT /api/users/<id>/)
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

  // Send friend request (POST /api/friend-requests/)
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
    fetchMe,
    fetchCurrentUser,
    updateProfile,
    sendFriendRequest,
  };
});
