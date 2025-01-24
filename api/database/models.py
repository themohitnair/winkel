from sqlmodel import Field, SQLModel, Relationship, LargeBinary, UUID
from typing import List
from uuid import uuid4


class BaseModel(SQLModel):
    id: UUID = Field(primary_key=True, default_factory=uuid4, default=lambda: uuid4())


class User(BaseModel, table=True):
    user_name: str
    user_email: str
    college_id: str
    ph_no: str

    products: List["Product"] = Relationship(back_populates="user")


class Categories(BaseModel, table=True):
    category_name: str

    products: List["Product"] = Relationship(
        back_populates="categories",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "onupdate": "CASCADE",
            "ondelete": "CASCADE",
        },
    )


class Product(BaseModel, table=True):
    product_name: str
    product_price: float

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

    categories: List[Categories] = Relationship(
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


class Fields(BaseModel, table=True):
    field_name: str
    field_value: str

    product_id: UUID = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="fields")


class Media(BaseModel, table=True):
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
