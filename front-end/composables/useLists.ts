import type { MediaList, ListItem, ListCreate, ListUpdate } from '~/types/list'

export const useLists = () => {
  const { fetchWithAuth } = useApi()

  async function getAllLists(): Promise<MediaList[]> {
    const response = await fetchWithAuth<{lists: MediaList[], count: number}>('/api/v1/lists/user/me')
    return response.lists || []
  }

  async function getListById(id: string): Promise<MediaList> {
    return await $fetch<MediaList>(`/api/v1/lists/${id}`)
  }

  async function createList(list: ListCreate): Promise<MediaList> {
    return await fetchWithAuth<MediaList>('/api/v1/lists', {
      method: 'POST',
      body: list
    })
  }

  async function updateList(id: string, list: ListUpdate): Promise<MediaList> {
    return await fetchWithAuth<MediaList>(`/api/v1/lists/${id}`, {
      method: 'PATCH',
      body: list
    })
  }

  async function deleteList(id: string): Promise<void> {
    await fetchWithAuth(`/api/v1/lists/${id}`, {
      method: 'DELETE'
    })
  }

  async function addMediaToList(listId: string, mediaId: string): Promise<ListItem> {
    return await fetchWithAuth<ListItem>(`/api/v1/lists/${listId}/items/${mediaId}`, {
      method: 'POST'
    })
  }

  async function removeMediaFromList(listId: string, mediaId: string): Promise<void> {
    await fetchWithAuth(`/api/v1/lists/${listId}/items/${mediaId}`, {
      method: 'DELETE'
    })
  }

  return {
    getAllLists,
    getListById,
    createList,
    updateList,
    deleteList,
    addMediaToList,
    removeMediaFromList
  }
}