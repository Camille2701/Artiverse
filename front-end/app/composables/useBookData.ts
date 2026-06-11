import type { MediaItem } from '~/types'

export const useBookData = () => {
  const { users } = useUserData()

  const Books: MediaItem[] = [
    {
      id: 29,
      rank: 1,
      imgLink: "dune_book.png",
      imgAlt: "Couverture Dune",
      title: "Dune",
      year: 1965,
      type: "livre",
      score: 9.4,
      tags: ["Science-Fiction", "Classique"],
      critiques: [
        {
          id: 35,
          user: users[1],
          note: 10,
          commentaire: "Un univers d'une richesse incroyable.",
          date: new Date("2026-06-01")
        },
        {
          id: 36,
          user: users[3],
          note: 9,
          commentaire: "Dense mais fascinant.",
          date: new Date("2026-06-03")
        }
      ]
    },
    {
      id: 30,
      rank: 2,
      imgLink: "harry_potter.png",
      imgAlt: "Harry Potter",
      title: "Harry Potter à l'école des sorciers",
      year: 1997,
      type: "livre",
      score: 9.0,
      tags: ["Fantasy", "Jeunesse"],
      critiques: [
        {
          id: 37,
          user: users[2],
          note: 9,
          commentaire: "Toujours aussi magique.",
          date: new Date("2026-06-02")
        }
      ]
    },
    {
      id: 31,
      rank: 3,
      imgLink: "1984.png",
      imgAlt: "1984",
      title: "1984",
      year: 1949,
      type: "livre",
      score: 9.5,
      tags: ["Dystopie", "Classique"],
      critiques: [
        {
          id: 38,
          user: users[4],
          note: 10,
          commentaire: "Terrifiant et visionnaire.",
          date: new Date("2026-06-04")
        },
        {
          id: 39,
          user: users[5],
          note: 9,
          commentaire: "Toujours d'actualité.",
          date: new Date("2026-06-05")
        }
      ]
    },
    {
      id: 32,
      rank: 4,
      imgLink: "le_petit_prince.png",
      imgAlt: "Le Petit Prince",
      title: "Le Petit Prince",
      year: 1943,
      type: "livre",
      score: 9.6,
      tags: ["Poétique", "Philosophique"],
      critiques: [
        {
          id: 40,
          user: users[6],
          note: 10,
          commentaire: "Simple mais profond.",
          date: new Date("2026-06-06")
        }
      ]
    },
    {
      id: 33,
      rank: 5,
      imgLink: "the_hobbit.png",
      imgAlt: "Le Hobbit",
      title: "Le Hobbit",
      year: 1937,
      type: "livre",
      score: 9.2,
      tags: ["Fantasy", "Aventure"],
      critiques: [
        {
          id: 41,
          user: users[7],
          note: 9,
          commentaire: "Une aventure intemporelle.",
          date: new Date("2026-06-07")
        }
      ]
    },
    {
      id: 34,
      rank: 6,
      imgLink: "sapiens.png",
      imgAlt: "Sapiens",
      title: "Sapiens",
      year: 2011,
      type: "livre",
      score: 9.1,
      tags: ["Essai", "Histoire"],
      critiques: [
        {
          id: 42,
          user: users[8],
          note: 9,
          commentaire: "Très instructif et accessible.",
          date: new Date("2026-06-08")
        },
        {
          id: 43,
          user: users[9],
          note: 8,
          commentaire: "Dense mais passionnant.",
          date: new Date("2026-06-09")
        }
      ]
    },
    {
      id: 35,
      rank: 7,
      imgLink: "atomic_habits.png",
      imgAlt: "Atomic Habits",
      title: "Atomic Habits",
      year: 2018,
      type: "livre",
      score: 8.9,
      tags: ["Développement personnel"],
      critiques: [
        {
          id: 44,
          user: users[10],
          note: 9,
          commentaire: "Très utile au quotidien.",
          date: new Date("2026-06-10")
        },
        {
          id: 45,
          user: users[11],
          note: 8,
          commentaire: "Simple mais efficace.",
          date: new Date("2026-06-11")
        },
        {
          id: 46,
          user: users[12],
          note: 9,
          commentaire: "Bon livre de discipline personnelle.",
          date: new Date("2026-06-12")
        }
      ]
    }
  ]

  return { Books }
}