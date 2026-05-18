import { type Media } from '~~/types/media';

export default defineEventHandler(async (event) => {
    const body: Partial<Media> = await readBody(event);
    

    const newMedia: Media = {
        id: Math.random().toString(36).substring(7),
        title: body.title || 'Untitled',
        description: body.description || '',
        type: body.type, 
        rating: 0,
        releaseDate: new Date().toISOString().split('T')[0],
        ...body
    };

    return {
        success: true,
        media: newMedia
    };
});
