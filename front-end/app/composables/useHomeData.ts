import type { MediaItem, ActivityItem, CategoryItem, StatItem } from '@/types'

export const useHomeData = () => {
  const stats: StatItem[] = [
    { imgLink: "oeuvres", imgAlt: "Oeuvres logo", value: '18M',  label: 'Œuvres cataloguées' },
    { imgLink: "critiques", imgAlt: "Critques logo", value: '7,2M', label: 'Critiques publiées'  },
    { imgLink: "badges", imgAlt:"Badges logo", value: '430K', label: 'Badges débloqués'    },
    { imgLink: "comptes", imgAlt:"Comptes logo", value: '3M',    label: 'Comptes inscrits'    },
  ]

  const featuredItem: MediaItem = {
    id: 1,
    title: 'Dune: Part Two',
    year: 2024,
    type: 'film',
    score: 9.4,
    tags: ['Science-fiction', 'Épopée', 'Adapté du roman'],
    description:
      "La suite épique de l'adaptation de Frank Herbert. Paul Atréides s'engage dans un voyage spirituel et stratégique pour devenir le Messie des Fremen.",
    duration: '2h46',
    director: 'Denis Villeneuve',
  }

  const sideItems: MediaItem[] = [
    { id: 2, title: 'Elden Ring', type: 'jeu', score: 9.6, imgLink:"elden_ring" , imgAlt:"Image du jeu Elden Ring", tags: [] },
    { id: 3, title: 'Shōgun', type: 'serie', score: 9.0, imgLink:"shogun" , imgAlt:"Image de la série Shogun", tags: [] },
    { id: 4, title: 'Intermezzo', type: 'livre', score: 8.3, imgLink:"intermezzo" , imgAlt:"Image du livre Intermezzo", tags: [] },
  ]

  const trending: MediaItem[] = [
    {
      id: 5, rank: 1,
      imgLink: "alien_romulus.png",
      imgAlt:"Cover du film Alien: Romulus",
      title: 'Alien: Romulus',
      year: 2024, type: 'film', score: 8.7,
      tags: ['Horreur', 'SF'],
    },
    {
      id: 6, rank: 2,
      imgLink: "black_myth_wukong.png",
      imgAlt:"Cover du jeu Back Myth: Wukong",
      title: 'Black Myth: Wukong',
      year: 2024, type: 'jeu', score: 9.2,
      tags: ['Action RPG', 'Mythologie'],
    },
    {
      id: 7, rank: 3,
      title: 'The Bear: S3',
      imgLink: "the_bear_s3.png",
      imgAlt:"Cover de la série The Bear: S3",
      year: 2024, type: 'serie', score: 9.1,
      tags: ['Drame', 'Cuisine'],
    },
    {
      id: 8, rank: 4,
      title: 'Orbital',
      imgLink: "orbital.png",
      imgAlt:"Cover du roman Orbital",
      year: 2024, type: 'livre', score: 8.5,
      tags: ['Booker Prize', 'Littérature'],
    },
  ]

  const activity: ActivityItem[] = [
    {
      id: 1,
      user: { initials: 'ML'},
      action: 'a noté',
      target: 'Oppenheimer',
      extra: '9/10',
      time: 'Il y a 3 min',
    },
    {
      id: 2,
      user: { initials: 'TK'},
      action: 'a terminé',
      target: "Baldur's Gate 3",
      extra: 'Platine',
      extraType: 'badge',
      time: 'Il y a 12 min',
    },
    {
      id: 3,
      user: { initials: 'SB'},
      action: 'a ajouté 3 films à',
      target: 'À voir absolument',
      time: 'Il y a 28 min',
    },
    {
      id: 4,
      user: { initials: 'NR'},
      action: 'a critiqué',
      target: 'The Bear S3',
      extra: '"Bouleversant"',
      extraType: 'quote',
      time: 'Il y a 45 min',
    },
  ]

  const categories: CategoryItem[] = [
    { id: 'film',  label: 'Films',      count: '842 000 titres',  imgLink: '/icons/films.png',  imgAlt: 'icone films'},
    { id: 'serie', label: 'Séries',     count: '128 000 titres',  imgLink: '/icons/series.png', imgAlt: 'icone series'},
    { id: 'jeu',   label: 'Jeux vidéo', count: '310 000 jeux',    imgLink: '/icons/jeux.png',   imgAlt: 'icone jeux'},
    { id: 'livre', label: 'Livres',     count: '4,2 millions',    imgLink: '/icons/livres.png', imgAlt: 'icone livres'},
  ]

  return { stats, featuredItem, sideItems, trending, activity, categories }
}
