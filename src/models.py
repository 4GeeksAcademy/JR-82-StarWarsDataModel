from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,  ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped["Login"] = relationship(back_populates="user")
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password
            # do not serialize the password, its a security breach
        }


class Login(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="login")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    people: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[List["Favorites"]] = relationship(
        "Favorites", back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "people": self.people
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    planet: Mapped[str] = mapped_column(nullable=False)
    favorites: Mapped[List["Favorites"]] = relationship(
        "Favorites", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    favorite_people_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"), nullable=True)
    favorite_planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    people: Mapped["People"] = relationship(
        "People", back_populates="favorites")
    planet: Mapped["Planet"] = relationship(
        "Planet", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "favorite_people_id": self.favorite_people_id,
            "favorite_planet_id": self.favorite_planet_id
        }
