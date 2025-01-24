from sqlmodel import Field, SQLModel, Relationship, LargeBinary, UUID
from typing import List
from uuid import uuid4


class User(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default=lambda: uuid4())
    products: List["Product"] = Relationship(back_populates="user")
    user_name: str
    user_email: str
    college_id: str
    ph_no: str


class Categories(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default=lambda: uuid4())
    category_name: str
    products: List["Product"] = Relationship(
        back_populates="categories",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )


class Product(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default=lambda: uuid4())
    user_id: UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="products")
    medias: List["Media"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )
    product_name: str
    product_price: float
    categories: List["Categories"] = Relationship(
        back_populates="products",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )
    fields: List["Fields"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )


class Fields(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default=lambda: uuid4())
    field_name: str
    field_value: str
    product: Product = Relationship(
        back_populates="fields",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )


class Media(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default=lambda: uuid4())
    data: bytes = Field(sa_column_args=[LargeBinary])
    product_id: UUID = Field(foreign_key="product.id")
    product: Product = Relationship(
        back_populates="medias",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )
