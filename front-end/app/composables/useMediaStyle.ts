import type { MediaType } from '~/types'

interface MediaStyle {
  icon: string
  color: string
  bg: string
  tagClass: string
  label: string
}

const mediaMap: Record<MediaType, MediaStyle> = {
  film:  { icon: 'ti-movie',            color: '#7F77DD', bg: '#221955', tagClass: 'tag-purple', label: 'Film'      },
  serie: { icon: 'ti-device-tv',        color: '#5DCAA5', bg: '#04342C', tagClass: 'tag-teal',   label: 'Série'     },
  jeu:   { icon: 'ti-device-gamepad-2', color: '#EF9F27', bg: '#1A1040', tagClass: 'tag-gold',   label: 'Jeu vidéo' },
  livre: { icon: 'ti-book',             color: '#ED93B1', bg: '#4B1528', tagClass: 'tag-pink',   label: 'Roman'     },
}

export const useMediaStyle = () => {
  const getStyle = (type: MediaType) => mediaMap[type]

  const starsFromScore = (score: number): string => {
    const full = Math.round(score / 2)
    return '★'.repeat(full) + '☆'.repeat(5 - full)
  }

  return { getStyle, starsFromScore }
}
