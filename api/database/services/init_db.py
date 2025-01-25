from contextlib import contextmanager
from sqlmodel import create_engine, Session, SQLModel

class DatabaseSessionManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
    
    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)
    
    @contextmanager
    def session_scope(self):
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_session(self) -> Session:
        return Session(self.engine)

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
