import type { MediaItem } from '~/types'

export const useSeriesData = () => {
  const { users } = useUserData()

  const Series: MediaItem[] = [
    {
      id: 22,
      imgLink: "house_of_the_dragon.png",
      imgAlt: "House of the Dragon",
      title: "House of the Dragon",
      year: 2024,
      type: "serie",
      score: 9.1,
      tags: ["Fantasy", "Drame"],
      director: "Ryan Condal",
      description: "La série raconte la guerre civile interne à la maison Targaryen, des années avant Game of Thrones. Elle explore les luttes de pouvoir, les héritages familiaux et les conséquences destructrices des ambitions politiques.",
      critiques: [
        {
          id: 23,
          user: users[1],
          note: 9,
          commentaire: "Très intense et bien produit.",
          date: new Date("2026-06-02")
        },
        {
          id: 24,
          user: users[3],
          note: 8,
          commentaire: "Un bon rythme global.",
          date: new Date("2026-06-04")
        }
      ]
    },
    {
      id: 23,
      imgLink: "the_boys.png",
      imgAlt: "The Boys",
      title: "The Boys",
      year: 2024,
      type: "serie",
      score: 9.3,
      tags: ["Action", "Satire"],
      director: "Eric Kripke",
      description: "Dans un monde où les super-héros sont contrôlés par des corporations, un groupe clandestin tente de révéler leurs abus et leur corruption. La série mélange violence, satire et critique du pouvoir médiatique.",
      critiques: [
        {
          id: 25,
          user: users[2],
          note: 10,
          commentaire: "Toujours aussi violent et intelligent.",
          date: new Date("2026-06-01")
        },
        {
          id: 26,
          user: users[5],
          note: 9,
          commentaire: "Très bon équilibre humour/violence.",
          date: new Date("2026-06-05")
        }
      ]
    },
    {
      id: 24,
      imgLink: "stranger_things.png",
      imgAlt: "Stranger Things",
      title: "Stranger Things",
      year: 2023,
      type: "serie",
      score: 8.9,
      tags: ["Science-Fiction", "Horreur"],
      director: "The Duffer Brothers",
      description: "Dans une petite ville des années 80, la disparition d’un enfant révèle l’existence d’un monde parallèle et de phénomènes surnaturels. La série mêle horreur, science-fiction et nostalgie.",
      critiques: [
        {
          id: 27,
          user: users[4],
          note: 9,
          commentaire: "Très nostalgique et efficace.",
          date: new Date("2026-06-03")
        }
      ]
    },
    {
      id: 25,
      imgLink: "breaking_bad.png",
      imgAlt: "Breaking Bad",
      title: "Breaking Bad",
      year: 2013,
      type: "serie",
      score: 9.8,
      tags: ["Crime", "Drame"],
      director: "Vince Gilligan",
      description: "Un professeur de chimie atteint d’un cancer se lance dans la fabrication de drogue pour assurer l’avenir de sa famille. Il glisse progressivement dans un monde criminel où son identité change complètement.",
      critiques: [
        {
          id: 28,
          user: users[6],
          note: 10,
          commentaire: "Chef-d'œuvre absolu.",
          date: new Date("2026-06-06")
        },
        {
          id: 29,
          user: users[7],
          note: 10,
          commentaire: "Toujours incroyable même aujourd’hui.",
          date: new Date("2026-06-07")
        }
      ]
    },
    {
      id: 26,
      imgLink: "dark.png",
      imgAlt: "Dark",
      title: "Dark",
      year: 2020,
      type: "serie",
      score: 9.6,
      tags: ["Science-Fiction", "Thriller"],
      director: "Baran bo Odar, Jantje Friese",
      description: "Plusieurs familles sont liées par des événements qui traversent différentes périodes temporelles. La série explore le temps, le libre arbitre et les paradoxes à travers une intrigue complexe et structurée.",
      critiques: [
        {
          id: 30,
          user: users[8],
          note: 10,
          commentaire: "Complexe mais brillant.",
          date: new Date("2026-06-08")
        }
      ]
    },
    {
      id: 27,
      imgLink: "the_crown.png",
      imgAlt: "The Crown",
      title: "The Crown",
      year: 2023,
      type: "serie",
      score: 8.7,
      tags: ["Drame", "Historique"],
      director: "Peter Morgan",
      description: "La série retrace le règne d’Elizabeth II et les défis politiques, personnels et institutionnels auxquels elle fait face. Elle montre l’évolution de la monarchie britannique dans un monde en mutation.",
      critiques: [
        {
          id: 31,
          user: users[9],
          note: 9,
          commentaire: "Très bien interprété.",
          date: new Date("2026-06-09")
        },
        {
          id: 32,
          user: users[10],
          note: 8,
          commentaire: "Un peu lent mais solide.",
          date: new Date("2026-06-10")
        }
      ]
    },
    {
      id: 28,
      imgLink: "arcane.png",
      imgAlt: "Arcane",
      title: "Arcane",
      year: 2024,
      type: "serie",
      score: 9.7,
      tags: ["Animation", "Action"],
      director: "Christian Linke, Alex Yee",
      description: "L’histoire suit les tensions entre la ville riche de Piltover et les bas-fonds de Zaun à travers le destin de deux sœurs. La série combine émotion, action et une direction artistique unique inspirée de l’univers de League of Legends.",
      critiques: [
        {
          id: 33,
          user: users[11],
          note: 10,
          commentaire: "Animation et histoire incroyables.",
          date: new Date("2026-06-11")
        },
        {
          id: 34,
          user: users[12],
          note: 9,
          commentaire: "Très émotionnel et puissant.",
          date: new Date("2026-06-12")
        }
      ]
    }
  ]

  return { Series }
}