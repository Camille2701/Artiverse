import { type Media } from '~~/types/media';

export default defineEventHandler(async (event) => {
    const body: Partial<Media> = await readBody(event);

    try {
        const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000';
        const response = await $fetch(`${backendUrl}/api/v1/media`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie(event, 'auth_token') || ''}`
            },
            body: body
        });

        return response;
    } catch (error) {
        console.error('Failed to create media in backend:', error);
        // Fallback to mock response
        const newMedia: Media = {
            id: Math.random().toString(36).substring(7),
            title: body.title || 'Untitled',
            description: body.description || '',
            type: body.type as any,
            rating: 0,
            releaseDate: new Date().toISOString().split('T')[0],
            image: body.image || '',
            ...body
        };

        return {
            success: true,
            media: newMedia
        };
    }
});
