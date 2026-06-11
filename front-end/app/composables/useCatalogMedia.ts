export const useCatalogMedia = () => {
  const { Movies } = useMovieData()
  const { Series } = useSeriesData()
  const { Games } = useGameData()
  const { Books } = useBookData()

  const allMedia = [...Movies, ...Series, ...Games, ...Books]

  const findMediaById = (id: number | string) => {
    const mediaId = Number(id)
    return allMedia.find(item => item.id === mediaId)
  }

  return {
    allMedia,
    findMediaById,
  }
}