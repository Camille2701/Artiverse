export enum MediaType {
  Movie = 'movie',
  Game = 'video_game',
  Book = 'book',
  Serie = 'tv_series'
}

export interface Media {
  id: string;
  title: string;
  type: MediaType;
  description: string;
  rating: number;
  releaseDate: string;
  image: string;
}
