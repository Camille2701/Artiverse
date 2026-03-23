export enum MediaType {
  Movie = 'Movie',
  Game = 'Game',
  Book = 'Book'
}

export interface Media {
  id: string;
  title: string;
  type: MediaType;
  description: string;
  rating: number;
  releaseDate: string;
}
