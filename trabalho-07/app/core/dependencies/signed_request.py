from fastapi.security import APIKeyHeader
from fastapi import Request, Depends
from app.core.security.hmac import Hmac
from app.modules.clients.service import ClientService, get_client_service


async def signed_request(
    request: Request,
    x_api_key: str = Depends(APIKeyHeader(name="X-API-Key")),
    x_timestamp: str = Depends(APIKeyHeader(name="X-Timestamp")),
    x_signature: str = Depends(APIKeyHeader(name="X-Signature")),
    client_service: ClientService = Depends(get_client_service),
):
    client = client_service.get_client_by_api_key(x_api_key)

    hmac_auth = Hmac(client.hmac_secret)

    await hmac_auth.verify_request(request)

    return x_api_key
