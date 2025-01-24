# i have made some changes to the models and also crud_for_models file
# depending on what uttam wants and how he will work i will change shit
# so i will do this after asking him tomorrow

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


class ProductRepository(BaseRepository):
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


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(
        self, user_name: str, user_email: str, college_id: str, ph_no: str
    ) -> User:
        user = User(
            user_name=user_name,
            user_email=user_email,
            college_id=college_id,
            ph_no=ph_no,
        )
        return self.user_repository.create(user)
