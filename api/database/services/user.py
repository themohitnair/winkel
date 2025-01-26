from database.init import Database

# from models.user import UserInit, UserLoginRequest, UserLoginVerify
from datetime import date
# from aiosqlite import OperationalError


class UserService(Database):
    def __init__(self, db_path: str = "database.db"):
        super().__init__(db_path)

    async def create_user(
        self,
        first_name: str,
        last_name: str,
        uni_serial_number: str,
        ph_no: str,
        date_of_birth: date,
    ):
        await self.connect()

        ...
