# from enum import Enum
import enum

from sqlalchemy import Boolean, Column, Enum, Identity, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class Gender(enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class Role(enum.Enum):
    admin = "Admin"
    student = "Student"
    deve = "Developer"
    cust = "Customer"
    other = "Other"


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    first_name = Column(
        String,
    )
    last_name = Column(
        String,
    )
    gender = Column(
        Enum(Gender),
    )
    role = Column(
        Enum(Role),
    )
