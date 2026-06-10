import type { MediaItem, ActivityItem, CategoryItem, StatItem } from '~/types'

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
    { id: 2, title: 'Elden Ring',    year: 2022, type: 'jeu',   score: 9.6, tags: [] },
    { id: 3, title: 'Shōgun',       year: 2024, type: 'serie', score: 9.0, tags: [] },
    { id: 4, title: 'Intermezzo',   year: 2024, type: 'livre', score: 8.3, tags: [] },
  ]

  const trending: MediaItem[] = [
    {
      id: 5, rank: 1,
      title: 'Alien: Romulus',
      year: 2024, type: 'film', score: 8.7,
      tags: ['Horreur', 'SF'],
    },
    {
      id: 6, rank: 2,
      title: 'Black Myth: Wukong',
      year: 2024, type: 'jeu', score: 9.2,
      tags: ['Action RPG', 'Mythologie'],
    },
    {
      id: 7, rank: 3,
      title: 'The Bear S3',
      year: 2024, type: 'serie', score: 9.1,
      tags: ['Drame', 'Cuisine'],
    },
    {
      id: 8, rank: 4,
      title: 'Orbital',
      year: 2024, type: 'livre', score: 8.5,
      tags: ['Booker Prize', 'Littérature'],
    },
  ]

  const activity: ActivityItem[] = [
    {
      id: 1,
      user: { initials: 'ML', color: '#3C3489', textColor: '#CECBF6' },
      action: 'a noté',
      target: 'Oppenheimer',
      extra: '9/10',
      time: 'Il y a 3 min',
    },
    {
      id: 2,
      user: { initials: 'TK', color: '#633806', textColor: '#FAC775' },
      action: 'a terminé',
      target: "Baldur's Gate 3",
      extra: 'Platine',
      extraType: 'badge',
      time: 'Il y a 12 min',
    },
    {
      id: 3,
      user: { initials: 'SB', color: '#085041', textColor: '#5DCAA5' },
      action: 'a ajouté 3 films à',
      target: 'À voir absolument',
      time: 'Il y a 28 min',
    },
    {
      id: 4,
      user: { initials: 'NR', color: '#4B1528', textColor: '#ED93B1' },
      action: 'a critiqué',
      target: 'The Bear S3',
      extra: '"Bouleversant"',
      extraType: 'quote',
      time: 'Il y a 45 min',
    },
  ]

  const categories: CategoryItem[] = [
    { id: 'film',  label: 'Films',      count: '842 000 titres',  icon: 'ti-movie',             iconColor: '#7F77DD', iconBg: '#26215C' },
    { id: 'serie', label: 'Séries',     count: '128 000 titres',  icon: 'ti-device-tv',         iconColor: '#5DCAA5', iconBg: '#04342C' },
    { id: 'jeu',   label: 'Jeux vidéo', count: '310 000 jeux',    icon: 'ti-device-gamepad-2',  iconColor: '#EF9F27', iconBg: '#1A1040' },
    { id: 'livre', label: 'Livres',     count: '4,2 millions',    icon: 'ti-book',              iconColor: '#ED93B1', iconBg: '#4B1528' },
  ]

  return { stats, featuredItem, sideItems, trending, activity, categories }
}
