from contextlib import asynccontextmanager
from sqlmodel import Session, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class DatabaseSessionManager:
    def __init__(self, connection_string: str):
        self.engine = create_async_engine(url=connection_string)
        self.asyn_session_factory = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all())

    @asynccontextmanager
    def session_scope(self):
        session = AsyncEngine(self.engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_session(self) -> Session:
        return AsyncSession(self.engine)


# def example_usage():
#     session_manager = DatabaseSessionManager("sqlite:///example.db")
#     session_manager.create_tables()
#
#     # Method 1: Using context manager
#     with session_manager.session_scope() as session:
#         user_repo = UserRepository(session)
#         user = user_repo.create(User(name="John Doe"))
#
#     # Method 2: Manually managing session
#     session = session_manager.get_session()
#     try:
#         user_repo = UserRepository(session)
#         user = user_repo.create(User(name="Jane Doe"))
#         session.commit()
#     except Exception as e:
#         session.rollback()
#         raise
#     finally:
#         session.close()
#
# database_session_manager = DatabaseSessionManager("sqlite:///your_database.db")
