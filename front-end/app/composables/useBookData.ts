import type { MediaItem } from '~/types'

export const useBookData = () => {
  const { users } = useUserData()

  const Books: MediaItem[] = [
    {
      id: 29,
      imgLink: "dune_book.png",
      imgAlt: "Couverture Dune",
      title: "Dune",
      year: 1965,
      type: "livre",
      score: 9.4,
      tags: ["Science-Fiction", "Classique"],
      author: "Frank Herbert",
        description: "Dans un futur lointain, Paul Atreides se retrouve au centre d’un conflit galactique autour de la planète Arrakis et de son épice. Le roman explore la politique, la religion, l’écologie et le destin dans un univers extrêmement détaillé.",
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
      imgLink: "harry_potter.png",
      imgAlt: "Harry Potter",
      title: "Harry Potter à l'école des sorciers",
      year: 1997,
      type: "livre",
      score: 9.0,
      tags: ["Fantasy", "Jeunesse"],
      author: "J.K. Rowling",
        description: "Harry découvre à 11 ans qu’il est un sorcier et intègre l’école de Poudlard. Il y découvre un monde magique, de nouveaux amis et les premières traces d’un danger qui menace son existence.",
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
      imgLink: "1984.png",
      imgAlt: "1984",
      title: "1984",
      year: 1949,
      type: "livre",
      score: 9.5,
      tags: ["Dystopie", "Classique"],
      author: "George Orwell",
        description: "Dans un régime totalitaire, chaque individu est surveillé en permanence et la vérité est manipulée par le pouvoir. Le roman décrit une société où la liberté de pensée est presque inexistante.",
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
      imgLink: "le_petit_prince.png",
      imgAlt: "Le Petit Prince",
      title: "Le Petit Prince",
      year: 1943,
      type: "livre",
      score: 9.6,
      tags: ["Poétique", "Philosophique"],
      author: "Antoine de Saint-Exupéry",
        description: "Un pilote rencontre un jeune prince venu d’une autre planète qui lui raconte ses voyages et ses réflexions sur la vie. Le récit aborde des thèmes comme l’amitié, l’amour et la vision du monde à travers un regard innocent.",
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
      imgLink: "the_hobbit.png",
      imgAlt: "Le Hobbit",
      title: "Le Hobbit",
      year: 1937,
      type: "livre",
      score: 9.2,
      tags: ["Fantasy", "Aventure"],
      author: "J.R.R. Tolkien",
        description: "Bilbo Baggins est entraîné dans une aventure inattendue pour aider des nains à reprendre leur royaume volé par un dragon. Le récit mêle exploration, magie et croissance personnelle.",
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
      imgLink: "sapiens.png",
      imgAlt: "Sapiens",
      title: "Sapiens",
      year: 2011,
      type: "livre",
      score: 9.1,
      tags: ["Essai", "Histoire"],
      author: "Yuval Noah Harari",
        description: "L’auteur retrace l’histoire de l’humanité depuis les premiers Homo sapiens jusqu’à la société moderne. Il analyse les grandes révolutions qui ont façonné notre monde : cognitive, agricole et scientifique.",
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
      imgLink: "atomic_habits.png",
      imgAlt: "Atomic Habits",
      title: "Atomic Habits",
      year: 2018,
      type: "livre",
      score: 8.9,
      tags: ["Développement personnel"],
      author: "James Clear",
        description: "Le livre explique comment de petites habitudes quotidiennes peuvent transformer durablement une vie. Il propose une méthode concrète pour améliorer sa discipline, sa productivité et ses objectifs personnels.",
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