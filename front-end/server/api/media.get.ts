import { MediaType, type Media } from '~~/types/media';

export default defineEventHandler((event): Media[] => {
  return [
    {
      id: '1',
      title: 'Inception',
      type: MediaType.Movie,
      description: 'A thief who steals corporate secrets through the use of dream-sharing technology.',
      rating: 8.8,
      releaseDate: '2010-07-16',
      image: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=1025&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
      id: '2',
      title: 'The Witcher 3: Wild Hunt',
      type: MediaType.Game,
      description: 'Geralt of Rivia searches for his adopted daughter.',
      rating: 9.7,
      releaseDate: '2015-05-19',
      image: 'https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
      id: '3',
      title: '1984',
      type: MediaType.Book,
      description: 'A dystopian social science fiction novel and cautionary tale.',
      rating: 9.5,
      releaseDate: '1949-06-08',
      image: 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=987&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
      id: '4',
      title: 'Game of Thrones',
      type: MediaType.Serie,
      description: 'A culinary social science fiction series and princess tale.',
      rating: 10,
      releaseDate: '2011-04-17',
      image: 'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?q=80&w=1769&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    }
  ];
});
