import type { User } from '@/types/user'

export const useActiveUser = () => useState<User | null>('activeUser', () => null)