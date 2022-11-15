from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Query, Session

from db import SessionLocal, engine
from models import Base, Gender, Role, User
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
    f_name = db.query(User).filter(User.first_name == user.first_name).all()
    if not f_name:
        try:
            db_data = User(**user.dict())
            db.add(db_data)
            db.commit()
            db.refresh(db_data)
            return db_data
        except Exception as e:
            raise e

    raise HTTPException(status_code=403, detail="First name already taken. ")


@app.get("/user/")
def all_users(
    gender: Gender | None = None,
    role: Role | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if gender:
        query = query.filter(User.gender == gender)
    if role:
        query = query.filter(User.role == role)
    if search:
        query = query.filter(User.first_name.ilike(f"%{search}%"))

    data = query.all()

    return data


@app.get("/user/{user_id}/", response_model=UserResponse)
def user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    data = db.query(User).where(User.user_id == user_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="User not found. ")

    print(data.__dict__, "\n\n\n")
    return data

    # return data


@app.patch("/user/{user_id}/", response_model=UserResponse)
def update_by_id(
    user_id: int,
    user: UserUpdateRequest,
    db: Session = Depends(get_db),
):
    # name = db.query(User).filter(User.first_name).get(User.user_id == )
    f_name = db.query(User).filter(User.first_name == user.first_name).all()
    if not f_name:
        data = db.query(User).where(User.user_id == user_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="User not found.")

        try:
            update_data = user.dict(exclude_unset=True)
            for field in data.__dict__:
                if field in update_data:
                    setattr(data, field, update_data[field])
            db.add(data)
            db.commit()
            db.refresh(data)
            return data

        except Exception as error:
            return error
    raise HTTPException(
        status_code=422,
        detail=f"Unproc­essable entity, First name already exist with {user.first_name}",
    )


@app.delete("/user/{user_id}/")
def delete_by_id(user_id: int, db: Session = Depends(get_db)):
    data = db.query(User).where(User.user_id == user_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="User not found. ")
    try:
        db.delete(data)
        db.commit()
        return {"Message": f"User {data.user_id} deleted successfully. "}

    except Exception as error:
        return error
