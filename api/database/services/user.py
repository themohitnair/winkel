from sqlmodel import Session
from typing import Sequence
from database.repository import UserRepository
from database.models import User
from datetime import date as Date


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.user_repository = UserRepository(self.session)

    def create_user(
        self, user_name: str, user_email: str, college_id: str, ph_no: str, rating: float, date_of_birth: Date
    ) -> User:
        user = User(
            user_name=user_name,
            user_email=user_email,
            college_id=college_id,
            ph_no=ph_no,
            rating=rating,
            date_of_birth=date_of_birth,
        )
        return self.user_repository.create(user)

    def get_user_by_id(self, user_id: int) -> User:
        try:
            user = self.user_repository.get(user_id)
            return user
        except Exception as e:
            raise e

    def get_all_users(self) -> Sequence[User]:
        return self.user_repository.get_all()

    def update_user(
        self,
        user_id: int,
        user_name: str,
        user_email: str,
        college_id: str,
        ph_no: str,
    ) -> User:
        try:
            user = self.user_repository.get(user_id)
            user.user_name = user_name
            user.user_email = user_email
            user.college_id = college_id
            user.ph_no = ph_no
            return self.user_repository.update(user)
        except Exception as e:
            raise e

    def delete_user(self, user_id: int):
        try:
            user = self.user_repository.get(user_id)
            return self.user_repository.delete(user)
        except Exception as e:
            raise e
