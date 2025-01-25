from typing import List, Sequence, TypeVar, Generic
from sqlmodel import Session, select
from database.models import BaseModel, User, Categories, Listing, Media, Fields

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T], session: Session):
        self.model = model
        self.session = session

    def get(self, id: int) -> T:
        if id is None:
            raise ValueError("ID is required")

        entity = self.session.get(self.model, id)
        if entity is None:
            raise ValueError("Entity not found")
        return entity

    def create(self, obj: T) -> T:
        if obj.id is not None:
            raise ValueError("ID must be None")

        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: T) -> T:
        entity = self.session.get(self.model, obj.id)
        if entity:
            self.session.delete(entity)
            self.session.commit()
            return entity
        else:
            raise ValueError("Entity not found")

    def get_all(self) -> Sequence[T]:
        stmt = select(self.model)
        return self.session.exec(stmt).all()


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)


class ListingRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Listing, session)


class CategoriesRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Categories, session)


class MediaRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Media, session)


class FieldsRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Fields, session)
