import { User } from '~~/types/user'

export default defineEventHandler(async (event) => {
  try {
    const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
    const response = await $fetch(`${backendUrl}/api/v1/users/me`, {
      headers: {
        'Authorization': `Bearer ${getCookie(event, 'auth_token') || ''}`
      }
    });

    return [response];
  } catch (error) {
    console.error('Failed to fetch users from backend:', error);

    // Fallback to mock data
    const users = [
      { id: '1', username: 'nico_dev', email: 'nico.dev@example.com', bio: 'Full-stack developer', avatar_url: 'https://i.pravatar.cc/150?img=12', level: 5, experience_points: 2500},
      { id: '2', username: 'alice_ui', email: 'alice.ui@example.com', bio: 'UI/UX designer', avatar_url: 'https://i.pravatar.cc/150?img=32', level: 3, experience_points: 1200},
      { id: '3', username: 'bob_ts', email: 'bob.ts@example.com', bio: 'TypeScript enthusiast', avatar_url: 'https://i.pravatar.cc/150?img=56', level: 7, experience_points: 4500},
    ];

    return users;
  }
})