from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas, models
from database import get_db,engine
from auth import get_current_user, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from auth import get_password_hash
from models import User

app = FastAPI()

@app.on_event("startup")
def startup():
    # Create tables if they do not exist
    models.Base.metadata.create_all(bind=engine)
    
    # Check if the admin user already exists
    db = next(get_db())
    admin_user = db.query(User).filter(User.username == "arehman").first()
    
    if not admin_user:
        # Create the admin user if not already created
        hashed_password = get_password_hash("arehman")
        admin_user = User(
            username="arehman",
            email="arehman@example.com",
            hashed_password=hashed_password,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Admin user 'arehman' created successfully.")
    else:
        print("Admin user 'arehman' already exists.")

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create users")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view all users")
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_user(db, user_id=user_id, requesting_user_id=current_user.id, requesting_user_role=current_user.role)

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update users")
    return crud.update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete users")
    return crud.delete_user(db=db, user_id=user_id)