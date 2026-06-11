export function getDefaultCoverForType(type?: string | null): string {
  const covers: Record<string, string> = {
    movie: '/covers/movie.svg',
    tv_series: '/covers/tv_series.svg',
    book: '/covers/book.svg',
    video_game: '/covers/video_game.svg',
  }

  if (type && covers[type]) {
    return covers[type]
  }

  return '/covers/movie.svg'
}

export function resolveMediaImage(
  image?: string | null,
  type?: string | null,
): string {
  if (image) {
    return image
  }
  return getDefaultCoverForType(type)
}

export const useMediaCover = () => ({
  getDefaultCoverForType,
  resolveMediaImage,
})
