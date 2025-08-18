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


class InformationStored(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, )
    planet_id: Mapped[int] = mapped_column(nullable=True)
    character_id: Mapped[int] = mapped_column(nullable=True)
    favorites_id: Mapped[int] = mapped_column(ForeignKey("favorites.id"))
    info: Mapped["User"] = relationship(back_populates="info_favorited")

    def serialize(self):
        return {
            "id": self.id,

            # do not serialize the password, its a security breach
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, )
    favorite_the_planet_id: Mapped[int] = mapped_column(nullable=True)
    favorite_the_character_id: Mapped[int] = mapped_column(nullable=True)
    favorite_planets_id: Mapped[int] = mapped_column(nullable=True)
    favorite_characters_id: Mapped[int] = mapped_column(nullable=True)
    info_favorited: Mapped[List["InformationStored"]] = relationship(back_populates="info")

    def serialize(self):
        return {
            "id": self.id,

            # do not serialize the password, its a security breach
        }
