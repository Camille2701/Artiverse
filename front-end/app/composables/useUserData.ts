import type { User } from "@/types/user";

export const useUserData = () => {
    const users: User[] = [
        { id: 1, username: "Pamelo", createdAt : new Date("2026-05-08") },
        { id: 2, username: "Luna", createdAt : new Date("2026-05-02") },
        { id: 3, username: "Nexus", createdAt : new Date("2026-05-04") },
        { id: 4, username: "Shadow", createdAt : new Date("2026-05-12") },
        { id: 5, username: "Milo", createdAt : new Date("2026-06-01") },
        { id: 6, username: "Ghost", createdAt : new Date("2026-05-24") },
        { id: 7, username: "Raven", createdAt : new Date("2026-05-25") },
        { id: 8, username: "Pixel", createdAt : new Date("2026-05-29") },
        { id: 9, username: "Arwen", createdAt : new Date("2026-05-30") },
        { id: 10, username: "Titan", createdAt : new Date("2026-05-29") },
        { id: 11, username: "Nova", createdAt : new Date("2026-05-14") },
        { id: 12, username: "Echo", createdAt : new Date("2026-05-24") },
        { id: 13, username: "Night", createdAt : new Date("2026-05-03") }
    ]

    return { users }
}