from typing import type, List, TypeVar, Generic
from sqlmodel import Session, select
from database.models import BaseModel, User, Categories, Product, Media, Fields

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T], session: Session):
        self.model = model
        self.session = session

    def get(self, id: int) -> T:
        return self.session.get(self.model, id)

    def create(self, obj: T) -> T:
        self.session.add(self.model, obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj: T) -> T:
        obj = self.session.get(self.model, obj.id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            return obj

    def get_all(self) -> List[T]:
        stmt = select(self.model)
        return self.session.exec(stmt).all()


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)


class ListingRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Product, session)


class CategoriesRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Categories, session)


class MediaRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Media, session)


class FieldsRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Fields, session)
