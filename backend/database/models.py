from sqlmodel import Field, SQLModel, Relationship, LargeBinary
from typing import List
from uuid import uuid4


class User(SQLModel, table=True):
    user_id: int = Field(primary_key=True, default=lambda: uuid4())
    products: List["Product"] = Relationship(back_populates="user")
    user_name: str
    user_email: str
    college_id: str
    ph_no: str


class Categories(SQLModel, table=True):
    id: int = Field(primary_key=True)
    category_name: str
    products: List["Product"] = Relationship(back_populates="categories")


class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.user_id")
    user: User = Relationship(back_populates="products")
    medias: List["Media"] = Relationship(back_populates="product")
    product_name: str
    product_price: float
    categories: List["Categories"] = Relationship(back_populates="products")
    fields: List["Fields"] = Relationship(back_populates="product")


class Fields(SQLModel, table=True):
    id: int = Field(primary_key=True)
    field_name: str
    field_value: str
    product: Product = Relationship(back_populates="fields")


class Media(SQLModel, table=True):
    id: int = Field(primary_key=True)
    data: bytes = Field(sa_column_args={"type_": LargeBinary})
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="medias")
