from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import User
from app.schemas import ListResponse, ListCreate, ListUpdate
from app.services import ListService, MediaService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/lists", tags=["lists"])


@router.post("", response_model=ListResponse)
async def create_list(
    list_create: ListCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new list."""
    user_list = await ListService.create_list(db, list_create, current_user.id)
    return user_list


@router.get("/user/me", response_model=dict)
async def get_my_lists(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all lists for current user."""
    lists = await ListService.get_user_lists(db, current_user.id)
    return {
        "lists": [ListResponse.model_validate(lst).model_dump(mode="json") for lst in lists],
        "count": len(lists)
    }


@router.get("/{list_id}", response_model=ListResponse)
async def get_list(
    list_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a list by ID."""
    user_list = await ListService.get_list_by_id(db, list_id)
    
    if not user_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    
    return user_list


@router.patch("/{list_id}", response_model=ListResponse)
async def update_list(
    list_id: str,
    list_update: ListUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a list."""
    user_list = await ListService.get_list_by_id(db, list_id)
    
    if not user_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    
    if user_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this list"
        )
    
    update_data = list_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user_list, field, value)

    await db.commit()
    await db.refresh(user_list)
    return user_list


@router.post("/{list_id}/items/{media_id}", response_model=dict)
async def add_to_list(
    list_id: str,
    media_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add media to a list."""
    user_list = await ListService.get_list_by_id(db, list_id)
    
    if not user_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    
    if user_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this list"
        )

    # Verify media exists
    media = await MediaService.get_media_by_id(db, media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )

    list_item = await ListService.add_to_list(db, list_id, media_id)
    
    return {
        "list_id": list_id,
        "media_id": media_id,
        "item_id": list_item.id,
        "created_at": list_item.created_at
    }


@router.delete("/{list_id}/items/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_list(
    list_id: str,
    media_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove media from a list."""
    user_list = await ListService.get_list_by_id(db, list_id)
    
    if not user_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    
    if user_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this list"
        )

    await ListService.remove_from_list(db, list_id, media_id)


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(
    list_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a list."""
    user_list = await ListService.get_list_by_id(db, list_id)
    
    if not user_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    
    if user_list.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this list"
        )

    await ListService.delete_list(db, list_id)
