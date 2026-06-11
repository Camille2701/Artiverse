import type { MediaItem } from '~/types'

export const useMovieData = () => {
  const { users } = useUserData()

  const Movies: MediaItem[] = [
    {
      id: 15,
      rank: 2,
      imgLink: "dune.png",
      imgAlt: "Affiche de Dune Part Two",
      title: "Dune: Part Two",
      year: 2024,
      type: "film",
      score: 9.3,
      tags: ["Science-Fiction", "Épopée"],
      critiques: [
        {
          id: 13,
          user: users[1],
          note: 10,
          commentaire: "Visuellement incroyable, une claque.",
          date: new Date("2026-06-04")
        }
      ]
    },
    {
      id: 16,
      rank: 1,
      imgLink: "oppenheimer.png",
      imgAlt: "Affiche de Oppenheimer",
      title: "Oppenheimer",
      year: 2023,
      type: "film",
      score: 9.5,
      tags: ["Drame", "Historique"],
      critiques: [
        {
          id: 14,
          user: users[2],
          note: 10,
          commentaire: "Dense, puissant, magistral.",
          date: new Date("2026-06-06")
        },
        {
          id: 15,
          user: users[3],
          note: 9,
          commentaire: "Long mais captivant du début à la fin.",
          date: new Date("2026-06-03")
        }
      ]
    },
    {
      id: 17,
      rank: 3,
      imgLink: "killers_of_the_flower_moon.png",
      imgAlt: "Affiche de Killers of the Flower Moon",
      title: "Killers of the Flower Moon",
      year: 2023,
      type: "film",
      score: 8.8,
      tags: ["Crime", "Drame"],
      critiques: [
        {
          id: 16,
          user: users[4],
          note: 9,
          commentaire: "Très lent mais fascinant.",
          date: new Date("2026-05-30")
        }
      ]
    },
    {
      id: 18,
      rank: 4,
      imgLink: "barbie.png",
      imgAlt: "Affiche du film Barbie",
      title: "Barbie",
      year: 2023,
      type: "film",
      score: 8.2,
      tags: ["Comédie", "Satire"],
      critiques: [
        {
          id: 17,
          user: users[5],
          note: 8,
          commentaire: "Drôle et surprenant.",
          date: new Date("2026-06-03")
        },
        {
          id: 18,
          user: users[6],
          note: 9,
          commentaire: "Une vraie surprise niveau écriture.",
          date: new Date("2026-06-01")
        }
      ]
    },
    {
      id: 19,
      rank: 5,
      imgLink: "spider_man_across.png",
      imgAlt: "Affiche Spider-Man Across the Spider-Verse",
      title: "Spider-Man: Across the Spider-Verse",
      year: 2023,
      type: "film",
      score: 9.4,
      tags: ["Animation", "Action"],
      critiques: [
        {
          id: 19,
          user: users[7],
          note: 10,
          commentaire: "Animation complètement folle.",
          date: new Date("2023-06-02")
        }
      ]
    },
    {
      id: 20,
      rank: 6,
      imgLink: "the_batman.png",
      imgAlt: "Affiche The Batman",
      title: "The Batman",
      year: 2022,
      type: "film",
      score: 8.9,
      tags: ["Action", "Thriller"],
      critiques: [
        {
          id: 20,
          user: users[8],
          note: 9,
          commentaire: "Ambiance noire très réussie.",
          date: new Date("2026-06-03")
        },
        {
          id: 21,
          user: users[9],
          note: 8,
          commentaire: "Très bon mais un peu long.",
          date: new Date("2026-06-12")
        }
      ]
    },
    {
      id: 21,
      rank: 7,
      imgLink: "parasite.png",
      imgAlt: "Affiche Parasite",
      title: "Parasite",
      year: 2019,
      type: "film",
      score: 9.6,
      tags: ["Thriller", "Drame"],
      critiques: [
        {
          id: 22,
          user: users[10],
          note: 10,
          commentaire: "Chef-d'œuvre absolu.",
          date: new Date("2026-06-10")
        }
      ]
    }
  ]

  return { Movies }
}