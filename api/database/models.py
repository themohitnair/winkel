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

    # mapped to user in Listing -> single user has several listings
    listings: List["Listing"] = Relationship(back_populates="user")


class Category(BaseModel, table=True):
    category_name: str

    # mapped to category in Listing -> single category has several listings
    listings: List["Listing"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )


class Listing(BaseModel, table=True):
    listing_name: str
    listing_price: float
    category_id: int | None = Field(foreign_key="category.id", default=None)
    desc: str

    user_id: int | None = Field(foreign_key="user.id", default=None)
    user: User = Relationship(back_populates="listings")

    # media is already plural - mapped to listing in Category -> one listing has multiple media elements
    media: List["Media"] = Relationship(
        back_populates="listing",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )

    # mapped to listings in Category -> one listing has a single category
    category: Category = Relationship(
        back_populates="listings",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )

    # mapped to listing in Field -> one listing has several fields
    fields: List["Parameter"] = Relationship(
        back_populates="listing",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )


class Parameter(BaseModel, table=True):
    field_name: str
    field_value: str

    listing_id: int | None = Field(foreign_key="listing.id", default=None)

    # mapped to fields in Listing -> one field is part of one listing
    listing: Listing = Relationship(back_populates="fields")


class Media(BaseModel, table=True):
    data: bytes = Field(sa_column_args=[LargeBinary])

    listing_id: int | None = Field(foreign_key="listing.id", default=None)

    # media is already plural - mapped to media in Listing -> one media element is part of one listing
    listing: Listing = Relationship(
        back_populates="media",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )
