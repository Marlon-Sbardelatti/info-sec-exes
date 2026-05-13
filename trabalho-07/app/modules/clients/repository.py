from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.db.models.client import Client


class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_client_by_api_key(self, api_key: str) -> Client | None:
        stmt = select(Client).where(Client.api_key == api_key)
        client = self.session.execute(stmt).scalar_one_or_none()
        return client
