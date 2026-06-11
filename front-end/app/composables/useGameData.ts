import type { MediaItem } from '~/types'
  
export const useGameData = () => {
    const { users } = useUserData()
    const Games: MediaItem[] = [
        {
        id: 6,
        imgLink: "black_myth_wukong.png",
        imgAlt:"Cover du jeu Back Myth: Wukong",
        title: 'Black Myth: Wukong',
        year: 2024, type: 'jeu', score: 9.2,
        tags: ['Action RPG', 'Mythologie'],
        director: "Game Science",
        description: "Action RPG inspiré de la mythologie chinoise, où tu incarnes une figure proche du Roi Singe dans un monde rempli de divinités, de créatures et de combats exigeants. Le jeu se distingue par son système de combat technique, ses boss spectaculaires et une direction artistique très cinématographique qui mélange folklore et fantasy sombre.",
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
        imgLink: "astro_bot.png",
        imgAlt: "Cover du jeu Astro Bot",
        title: "Astro Bot",
        year: 2024,
        type: "jeu",
        score: 9.5,
        tags: ["Plateforme", "Aventure"],
        director: "Team Asobi",
        description: "Jeu de plateforme 3D centré sur l’exploration et la créativité, où Astro traverse des mondes variés remplis de puzzles, d’ennemis et de mécaniques innovantes. Le gameplay mise sur la précision, la fluidité et une mise en scène très joyeuse et accessible.",
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
        imgLink: "stellar_blade.png",
        imgAlt: "Cover du jeu Stellar Blade",
        title: "Stellar Blade",
        year: 2024,
        type: "jeu",
        score: 8.8,
        tags: ["Action", "Hack'n Slash"],
        director: "Shift Up",
        description: "Action hack’n slash futuriste dans un monde post-apocalyptique, où le joueur incarne une combattante affrontant des créatures mécaniques. Le jeu se distingue par son système de combat rapide, son esthétique sci-fi et sa narration centrée sur la survie humaine.",
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
        imgLink: "helldivers_2.png",
        imgAlt: "Cover du jeu Helldivers 2",
        title: "Helldivers 2",
        year: 2024,
        type: "jeu",
        score: 9.1,
        tags: ["Coop", "TPS"],
        director: "Arrowhead Game Studios",
        description: "Shooter coopératif en vue troisième personne où des escouades de soldats combattent des forces extraterrestres pour “la démocratie galactique”. Le jeu repose sur le chaos contrôlé, le tir allié dangereux et une forte dimension multijoueur stratégique.",
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
        imgLink: "dragon_age_veilguard.png",
        imgAlt: "Cover du jeu Dragon Age The Veilguard",
        title: "Dragon Age: The Veilguard",
        year: 2024,
        type: "jeu",
        score: 8.3,
        tags: ["RPG", "Fantasy"],
        director: "BioWare",
        description: "RPG narratif dans un univers fantasy où le joueur dirige un groupe de héros confrontés à des forces mystiques menaçant le monde. Le jeu met l’accent sur les choix, les relations entre personnages et une histoire fortement cinématographique.",
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
        imgLink: "space_marine_2.png",
        imgAlt: "Cover du jeu Warhammer 40K Space Marine 2",
        title: "Warhammer 40,000: Space Marine 2",
        year: 2024,
        type: "jeu",
        score: 8.9,
        tags: ["Action", "TPS"],
        director: "Saber Interactive",
        description: "Shooter brutal dans l’univers Warhammer 40K où le joueur incarne un Space Marine surpuissant combattant des hordes alien. Le gameplay est centré sur l’action intense, le combat au corps à corps et une mise en scène massive et spectaculaire.",
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
        imgLink: "silent_hill_2.png",
        imgAlt: "Cover du jeu Silent Hill 2 Remake",
        title: "Silent Hill 2 Remake",
        year: 2024,
        type: "jeu",
        score: 9.0,
        tags: ["Horreur", "Survie"],
        director: "Bloober Team",
        description: "Remake du classique du survival horror, plongeant le joueur dans une ville brumeuse remplie de manifestations psychologiques et de créatures symboliques. Le jeu met l’accent sur la tension, l’exploration et une narration profondément psychologique.",
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
