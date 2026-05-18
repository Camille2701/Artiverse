export type User = {
    id: number,
    name: string,
    email: string,
    role: 'admin' | 'user',
    isActive: boolean,
    avatar: string,
    age: number
}