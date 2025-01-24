from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID

# i will continne this file tomorrow


class BaseCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create(self, model):
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get_by_id(self, model_class, model_id: UUID):
        return self.session.get(model_class, model_id)

    def list_all(self, model_class):
        return self.session.exec(select(model_class)).all()

    def update(self, model):
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def delete(self, model):
        self.session.delete(model)
        self.session.commit()
