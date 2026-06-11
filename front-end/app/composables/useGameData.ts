import type { MediaItem } from '~/types'
  
export const useGameData = () => {
    const { users } = useUserData()
    const Games: MediaItem[] = [
        {
        id: 6, rank: 2,
        imgLink: "black_myth_wukong.png",
        imgAlt:"Cover du jeu Back Myth: Wukong",
        title: 'Black Myth: Wukong',
        year: 2024, type: 'jeu', score: 9.2,
        tags: ['Action RPG', 'Mythologie'],
        critiques: [
            {
                id: 1,
                user: users[1],
                note: 9,
                commentaire: "Super jeu",
                date: new Date()
            }
        ]
        },
        {
        id: 9,
        rank: 1,
        imgLink: "astro_bot.png",
        imgAlt: "Cover du jeu Astro Bot",
        title: "Astro Bot",
        year: 2024,
        type: "jeu",
        score: 9.5,
        tags: ["Plateforme", "Aventure"],
        critiques: [
            {
            id: 1,
            user: users[2],
            note: 10,
            commentaire: "Le meilleur jeu de plateforme depuis longtemps.",
            date: new Date("2024-09-15")
            },
            {
            id: 2,
            user: users[3],
            note: 9,
            commentaire: "Créatif et très fun.",
            date: new Date("2024-09-18")
            }
        ]
        },
        {
        id: 10,
        rank: 2,
        imgLink: "stellar_blade.png",
        imgAlt: "Cover du jeu Stellar Blade",
        title: "Stellar Blade",
        year: 2024,
        type: "jeu",
        score: 8.8,
        tags: ["Action", "Hack'n Slash"],
        critiques: [
            {
            id: 3,
            user: users[4],
            note: 9,
            commentaire: "Gameplay nerveux et excellente direction artistique.",
            date: new Date("2024-05-01")
            },
            {
            id: 4,
            user: users[5],
            note: 8,
            commentaire: "Très bon mais quelques quêtes répétitives.",
            date: new Date("2024-05-05")
            }
        ]
        },
        {
        id: 11,
        rank: 3,
        imgLink: "helldivers_2.png",
        imgAlt: "Cover du jeu Helldivers 2",
        title: "Helldivers 2",
        year: 2024,
        type: "jeu",
        score: 9.1,
        tags: ["Coop", "TPS"],
        critiques: [
            {
            id: 5,
            user: users[5],
            note: 10,
            commentaire: "Incroyable entre amis.",
            date: new Date("2024-03-10")
            },
            {
            id: 6,
            user: users[7],
            note: 9,
            commentaire: "Du chaos comme on l'aime.",
            date: new Date("2024-03-12")
            },
            {
            id: 7,
            user: users[8],
            note: 8,
            commentaire: "Très bon suivi des développeurs.",
            date: new Date("2024-03-20")
            }
        ]
        },
        {
        id: 12,
        rank: 4,
        imgLink: "dragon_age_veilguard.png",
        imgAlt: "Cover du jeu Dragon Age The Veilguard",
        title: "Dragon Age: The Veilguard",
        year: 2024,
        type: "jeu",
        score: 8.3,
        tags: ["RPG", "Fantasy"],
        critiques: [
            {
            id: 8,
            user: users[8],
            note: 8,
            commentaire: "Bonne histoire et compagnons attachants.",
            date: new Date("2024-11-05")
            }
        ]
        },
        {
        id: 13,
        rank: 5,
        imgLink: "space_marine_2.png",
        imgAlt: "Cover du jeu Warhammer 40K Space Marine 2",
        title: "Warhammer 40,000: Space Marine 2",
        year: 2024,
        type: "jeu",
        score: 8.9,
        tags: ["Action", "TPS"],
        critiques: [
            {
            id: 9,
            user: { id: 10, username: "Titan" },
            note: 9,
            commentaire: "Une vraie démonstration de puissance.",
            date: new Date("2024-09-12")
            },
            {
            id: 10,
            user: users[3],
            note: 9,
            commentaire: "Le meilleur jeu Warhammer depuis des années.",
            date: new Date("2024-09-15")
            }
        ]
        },
        {
        id: 14,
        rank: 6,
        imgLink: "silent_hill_2.png",
        imgAlt: "Cover du jeu Silent Hill 2 Remake",
        title: "Silent Hill 2 Remake",
        year: 2024,
        type: "jeu",
        score: 9.0,
        tags: ["Horreur", "Survie"],
        critiques: [
            {
            id: 11,
            user: users[12],
            note: 10,
            commentaire: "Une ambiance exceptionnelle.",
            date: new Date("2024-10-09")
            },
            {
            id: 12,
            user: users[9],
            note: 8,
            commentaire: "Très fidèle à l'original.",
            date: new Date("2024-10-12")
            }
        ]
        },
    ]
    return { Games }
}
