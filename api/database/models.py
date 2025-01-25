from sqlmodel import Field, SQLModel, Relationship, LargeBinary, UUID
from datetime import date as Date
from typing import List
from uuid import uuid4


class BaseModel(SQLModel):
    id: UUID = Field(primary_key=True, default_factory=uuid4, default=lambda: uuid4())


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
    category_id: UUID = Field(foreign_key="categories.id")
    desc: str

    user_id: UUID = Field(foreign_key="user.id")
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

    listing_id: UUID = Field(foreign_key="listing.id")
    listing: Listing = Relationship(back_populates="fields")


class Media(BaseModel, table=True):
    data: bytes = Field(sa_column_args=[LargeBinary])

    listing_id: UUID = Field(foreign_key="listing.id")
    listing: Listing = Relationship(
        back_populates="medias",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )
