import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { IUser, IUserUpdate } from '../types';
import { getCsrfToken } from '../utils/csrf';

export const useUserStore = defineStore('userStore', () => {
  const currentUser = ref<IUser | null>(null);
  const users = ref<IUser[]>([]);
  const hasNext = ref<boolean>(false);
  const totalPages = ref<number>(1);

  // stores pending friend requests for the useer
  const pendingFriendRequests = ref<any[]>([]);

  // list of friends 
  const friendsList = ref<IUser[]>([]);

  async function fetchMe(userId: number): Promise<void> {
    try {
      const response = await fetch(`/api/users/${userId}/`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
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

  async function fetchCurrentUser(): Promise<void> {
    try {
      const response = await fetch('/api/users/current/', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
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

  async function fetchUsers(params: URLSearchParams): Promise<void> {
    try {
      const response = await fetch(`/api/users/?${params.toString()}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
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

  async function updateProfile(userId: number, newUserData: Partial<IUserUpdate>): Promise<any> {
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
      const result = await response.json();
      // refetch the user data 
      await fetchMe(userId);
      return result;
    } catch (error) {
      console.error('Error in updateProfile:', error);
      throw error;
    }
  }

  /**
   * Add a  hobby to the user current hobby list.
   */
  async function addHobbyToCurrentUser(hobbyName: string): Promise<void> {
    if (!currentUser.value) return;
    // Re-fetch the user to get their latest hobbies
    await fetchMe(currentUser.value.id);

    const existingHobbies = currentUser.value.hobbies || [];
    if (existingHobbies.includes(hobbyName)) {
      return;
    }
    const newHobbies = [...existingHobbies, hobbyName];
    await updateProfile(currentUser.value.id, {
      hobbies: newHobbies,
    });
  }

  async function sendFriendRequest(toUserId: number): Promise<any> {
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

  /**
   * fetch requests where the current user is the 'to_user' and accepted=false (
   */
  async function fetchFriendRequests(): Promise<void> {
    try {
      const response = await fetch('/api/friend-requests/', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch friend requests');
      }
      const data = await response.json();
      pendingFriendRequests.value = data;
    } catch (error) {
      console.error('Error fetching friend requests:', error);
    }
  }

  async function acceptFriendRequest(friendRequestId: number): Promise<any> {
    try {
      const response = await fetch('/api/friend-requests/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({
          friend_request_id: friendRequestId,
          action: 'accept',
        }),
      });
      if (!response.ok) {
        throw new Error('Failed to accept friend request');
      }
      return await response.json();
    } catch (error) {
      console.error('Error in acceptFriendRequest:', error);
      throw error;
    }
  }

  
  async function fetchFriends(): Promise<void> {
    if (!currentUser.value) return;
    try {
      const response = await fetch('/api/users/current/friends/', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch friends');
      }
      const data = await response.json();
      friendsList.value = data; // data is an array of user objects
    } catch (error) {
      console.error('Error fetching friends:', error);
    }
  }

  return {
    currentUser,
    users,
    hasNext,
    totalPages,
    pendingFriendRequests,
    friendsList,
    fetchMe,
    fetchCurrentUser,
    fetchUsers,
    updateProfile,
    addHobbyToCurrentUser,
    sendFriendRequest,
    fetchFriendRequests,
    acceptFriendRequest,
    fetchFriends,
  };
});
