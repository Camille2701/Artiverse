from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas import ListResponse, ListCreate, ListUpdate
from app.services import ListService, MediaService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/lists", tags=["lists"])


@router.post("", response_model=ListResponse)
def create_list(
    list_create: ListCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new list."""
    user_list = ListService.create_list(db, list_create, current_user.id)
    return user_list


@router.get("/user/me", response_model=dict)
def get_my_lists(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all lists for current user."""
    lists = ListService.get_user_lists(db, current_user.id)
    
    return {
        "lists": lists,
        "count": len(lists)
    }


@router.get("/{list_id}", response_model=ListResponse)
def get_list(
    list_id: str,
    db: Session = Depends(get_db)
):
    """Get a list by ID."""
    user_list = ListService.get_list_by_id(db, list_id)
    
    if not user_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="List not found"
        )
    
    return user_list


@router.patch("/{list_id}", response_model=ListResponse)
def update_list(
    list_id: str,
    list_update: ListUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a list."""
    user_list = ListService.get_list_by_id(db, list_id)
    
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
    
    update_data = list_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user_list, field, value)
    
    db.commit()
    db.refresh(user_list)
    return user_list


@router.post("/{list_id}/items/{media_id}", response_model=dict)
def add_to_list(
    list_id: str,
    media_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add media to a list."""
    user_list = ListService.get_list_by_id(db, list_id)
    
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
    media = MediaService.get_media_by_id(db, media_id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    list_item = ListService.add_to_list(db, list_id, media_id)
    
    return {
        "list_id": list_id,
        "media_id": media_id,
        "item_id": list_item.id,
        "created_at": list_item.created_at
    }


@router.delete("/{list_id}/items/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_list(
    list_id: str,
    media_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove media from a list."""
    user_list = ListService.get_list_by_id(db, list_id)
    
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
    
    ListService.remove_from_list(db, list_id, media_id)


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(
    list_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a list."""
    user_list = ListService.get_list_by_id(db, list_id)
    
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
    
    ListService.delete_list(db, list_id)
