export type User = {
    id: string,
    username: string,
    email: string,
    bio: string | null,
    avatar_url: string | null,
    level: number,
    experience_points: number
}