from fastapi import Depends, HTTPException
from app.core.db.session import get_session
from app.core.db.models.client import Client
from app.modules.clients.repository import ClientRepository


class ClientService:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def get_client_by_api_key(self, api_key: str) -> Client:
        client = self.repo.get_client_by_api_key(api_key)
        if not client:
            raise HTTPException(status_code=401, detail="API Key inválida")
        return client


def get_client_service(session=Depends(get_session)) -> ClientService:
    repo = ClientRepository(session)
    return ClientService(repo)
