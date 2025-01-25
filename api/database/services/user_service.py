from database.models import User
from typing import List, Optional
from database.repository import UserRepository
from sqlmodel import Session, UUID


class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.user_repository = UserRepository(self.session)

    def create_user(
        self, user_name: str, user_email: str, college_id: str, ph_no: str
    ) -> User:
        try:
            user = User(
                user_name=user_name,
                user_email=user_email,
                college_id=college_id,
                ph_no=ph_no,
            )
            repo = UserRepository(self.session)
            return repo.create(user)
        except Exception as e:
            return e

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return self.user_repository.get(user_id)

    def get_all_users(self) -> List[User]:
        return self.user_repository.get_all()

    def update_user(
        self,
        user_id: UUID,
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
            return e

    def delete_user(self, user_id: UUID) -> User:
        try:
            user = self.user_repository.get(user_id)
            return self.user_repository.delete(user)
        except Exception as e:
            return e
