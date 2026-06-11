import type { MediaItem } from '~/types'

export const useMovieData = () => {
  const { users } = useUserData()

  const Movies: MediaItem[] = [
    {
      id: 15,
      imgLink: "dune.png",
      imgAlt: "Affiche de Dune Part Two",
      title: "Dune: Part Two",
      year: 2024,
      type: "film",
      score: 9.3,
      tags: ["Science-Fiction", "Épopée"],
      director: "Denis Villeneuve",
      description: "Paul Atreides poursuit son ascension sur la planète Arrakis en s’alliant aux Fremen pour renverser les forces en place. Le film explore le pouvoir, la religion et le destin à travers une mise en scène massive, une photographie immersive et une tension politique permanente.",
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
      imgLink: "oppenheimer.png",
      imgAlt: "Affiche de Oppenheimer",
      title: "Oppenheimer",
      year: 2023,
      type: "film",
      score: 9.5,
      tags: ["Drame", "Historique"],
      director: "Christopher Nolan",
      description: "Le film retrace la vie de J. Robert Oppenheimer et son rôle dans le développement de la bombe atomique. Il explore les dilemmes moraux, les conséquences scientifiques et politiques de cette invention, dans une narration non linéaire centrée sur la culpabilité et la responsabilité.",
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
      imgLink: "killers_of_the_flower_moon.png",
      imgAlt: "Affiche de Killers of the Flower Moon",
      title: "Killers of the Flower Moon",
      year: 2023,
      type: "film",
      score: 8.8,
      tags: ["Crime", "Drame"],
      director: "Martin Scorsese",
      description: "L’histoire vraie d’une série de meurtres visant la communauté Osage après la découverte de pétrole sur leurs terres. Le film met en lumière la corruption, la violence systémique et l’exploitation, dans une fresque lente mais profondément marquante.",
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
      imgLink: "barbie.png",
      imgAlt: "Affiche du film Barbie",
      title: "Barbie",
      year: 2023,
      type: "film",
      score: 8.2,
      tags: ["Comédie", "Satire"],
      director: "Greta Gerwig",
      description: "Une satire moderne qui utilise l’univers de Barbie pour questionner les normes sociales, les rôles de genre et la quête d’identité. Le film mélange humour, critique sociale et esthétique très stylisée pour proposer une lecture à plusieurs niveaux.",
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
      imgLink: "spider_man_across.png",
      imgAlt: "Affiche Spider-Man Across the Spider-Verse",
      title: "Spider-Man: Across the Spider-Verse",
      year: 2023,
      type: "film",
      score: 9.4,
      tags: ["Animation", "Action"],
      director: "Joaquim Dos Santos, Kemp Powers, Justin K. Thompson",
      description: "Miles Morales est projeté à travers le multivers et découvre des versions alternatives de Spider-Man. Le film explore les notions de destin, de choix et d’identité avec une animation innovante et extrêmement dynamique.",
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
      imgLink: "the_batman.png",
      imgAlt: "Affiche The Batman",
      title: "The Batman",
      year: 2022,
      type: "film",
      score: 8.9,
      tags: ["Action", "Thriller"],
      director: "Matt Reeves",
      description: "Batman débute ses premières années de lutte contre le crime à Gotham, confronté à une enquête complexe menée par le Riddler. Le film adopte une approche plus détective et sombre du personnage, centrée sur la psychologie et la corruption de la ville.",
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
      imgLink: "parasite.png",
      imgAlt: "Affiche Parasite",
      title: "Parasite",
      year: 2019,
      type: "film",
      score: 9.6,
      tags: ["Thriller", "Drame"],
      director: "Bong Joon-ho",
      description: "Deux familles issues de classes sociales opposées voient leurs destins s’entremêler dans une spirale de manipulation et de tension. Le film est une critique puissante des inégalités sociales, mêlant thriller, drame et satire.",
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