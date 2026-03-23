import { MediaType, type Media } from '~~/types/media';

export default defineEventHandler((event): Media[] => {
  return [
    {
      id: '1',
      title: 'Inception',
      type: MediaType.Movie,
      description: 'A thief who steals corporate secrets through the use of dream-sharing technology.',
      rating: 8.8,
      releaseDate: '2010-07-16'
    },
    {
      id: '2',
      title: 'The Witcher 3: Wild Hunt',
      type: MediaType.Game,
      description: 'Geralt of Rivia searches for his adopted daughter.',
      rating: 9.7,
      releaseDate: '2015-05-19'
    },
    {
      id: '3',
      title: '1984',
      type: MediaType.Book,
      description: 'A dystopian social science fiction novel and cautionary tale.',
      rating: 9.5,
      releaseDate: '1949-06-08'
    },
    {
      id: '4',
      title: 'Game of Thrones',
      type: MediaType.Serie,
      description: 'A culinary social science fiction series and princess tale.',
      rating: 10,
      releaseDate: '2326-06-08'
    }
  ];
});
