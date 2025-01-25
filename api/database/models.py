from sqlmodel import Field, SQLModel, Relationship, LargeBinary
from datetime import date as Date
from typing import List


class BaseModel(SQLModel):
    id: int | None = Field(primary_key=True, default=None)


class User(BaseModel, table=True):
    user_name: str
    user_email: str
    college_id: str
    rating: float
    date_of_birth: Date
    ph_no: str

    listing: List["Listing"] = Relationship(back_populates="user")


class Categories(BaseModel, table=True):
    category_name: str

    listings: List["Listing"] = Relationship(
        back_populates="categories",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )


class Listing(BaseModel, table=True):
    listing_name: str
    listing_price: float
    category_id: int | None = Field(foreign_key="categories.id", default=None)
    desc: str

    user_id: int | None = Field(foreign_key="user.id", default=None)
    user: User = Relationship(back_populates="listings")

    medias: List["Media"] = Relationship(
        back_populates="listings",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )

    categories: Categories = Relationship(
        back_populates="listings",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )

    fields: List["Fields"] = Relationship(
        back_populates="listings",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )


class Fields(BaseModel, table=True):
    field_name: str
    field_value: str

    listing_id: int | None = Field(foreign_key="listing.id", default=None)
    listing: Listing = Relationship(back_populates="fields")


class Media(BaseModel, table=True):
    data: bytes = Field(sa_column_args=[LargeBinary])

    listing_id: int | None = Field(foreign_key="listing.id", default=None)
    listing: Listing = Relationship(
        back_populates="medias",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )
