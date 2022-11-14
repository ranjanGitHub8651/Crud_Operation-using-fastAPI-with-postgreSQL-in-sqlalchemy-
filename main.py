from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, Query

from db import SessionLocal, engine
from models import User, Base, Gender, Role
from validators import UserCreateRequest, UserResponse, UserUpdateRequest

Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/user/", response_model=UserResponse)
async def insert_user(
    user: UserCreateRequest,
    db: Session = Depends(get_db),
):
    try:
        db_data = User(**user.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
    except Exception as e:
        raise e
    
    return db_data


@app.get("/user/")
def all_users( gender: Gender | None = None, role: Role | None = None, db: Session = Depends(get_db),):

    query =  db.query(User)
    if gender:
        query = query.filter(User.gender == gender).filter(User.role == role)
    
    data = query.all()
    if not data:
        raise HTTPException(status_code=404, detail="User not found. ")
    return data


@app.get("/user/{user_id}/", response_model=UserResponse)
def user_by_id(user_id: int, db: Session=Depends(get_db)):
    data = db.query(User).where(User.user_id == user_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="User not found. ")
    return data


@app.patch("/user/{user_id}/", response_model=UserResponse)
def update_by_id(user_id: int, user:UserUpdateRequest, db: Session = Depends(get_db),):
    data = db.query(User).where(User.user_id == user_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="User not found. ")
    update_data = user.dict(exclude_unset=True)
    for field in data.__dict__:
        if field in update_data:
            setattr(
                data,field,update_data[field]
            )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


@app.delete("/user/{user_id}/")
def delete_by_id(user_id: int, db:Session = Depends(get_db)):
    data = db.query(User).where(User.user_id == user_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="User not found. ")
    db.delete(data)
    db.commit()
    return {"Message": f"User {data.user_id} deleted successfully. "}