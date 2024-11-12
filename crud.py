from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import models, schemas
from auth import get_password_hash, verify_password
from typing import List, Optional

# Create a new user (only admin)
def create_user(db: Session, user: schemas.UserCreate):
    # Check if the username or email already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving it
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by ID (Admin or user viewing own profile)
def get_user(db: Session, user_id: int, requesting_user_id: int, requesting_user_role: str):
    if requesting_user_role == "admin" or user_id == requesting_user_id:
        return db.query(models.User).filter(models.User.id == user_id).first()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view this profile")

# Get all users (Admin only)
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# Update a user (Admin only)
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields if provided
    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.hashed_password = get_password_hash(user.password)
    if user.role:
        db_user.role = user.role

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a user (Admin only)
def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"msg": "User deleted successfully"}
