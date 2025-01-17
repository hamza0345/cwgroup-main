import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { IHobby } from '../types';
import { getCsrfToken } from '../utils/csrf';

export const useHobbyStore = defineStore('hobbyStore', () => {
  const hobbies = ref<IHobby[]>([]);

  async function fetchHobbies(): Promise<void> {
    try {
      const response = await fetch('/api/hobbies/', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!response.ok) {
        console.error('Error fetching hobbies');
        return;
      }
      const data = await response.json();
      hobbies.value = data.hobbies;
    } catch (error) {
      console.error('Error fetching hobbies:', error);
    }
  }

  async function addHobby(hobbyName: string): Promise<void> {
    try {
      const response = await fetch('/api/hobbies/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ hobby_name: hobbyName }),
      });
      if (!response.ok) {
        throw new Error('Failed to create hobby');
      }
      // After creating, we refetch the global list
      await fetchHobbies();
    } catch (error) {
      console.error('Error adding a hobby:', error);
      throw error;
    }
  }

  return {
    hobbies,
    fetchHobbies,
    addHobby,
  };
});
