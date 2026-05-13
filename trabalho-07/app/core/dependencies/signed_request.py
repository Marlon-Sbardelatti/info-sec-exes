from fastapi.security import APIKeyHeader
from fastapi import Request, Depends, Security, HTTPException
from app.core.security.hmac import Hmac


# async def signed_request(
#     request: Request,
#     x_api_key: str = Depends(APIKeyHeader(name="X-API-Key")),
#     x_timestamp: str = Depends(APIKeyHeader(name="X-Timestamp")),
#     x_signature: str = Depends(APIKeyHeader(name="X-Signature")),
# ):
#     return

async def signed_request(
    request: Request,
    # x_api_key: str = Security(APIKeyHeader(name="X-API-Key")),
    x_api_key: str = Depends(APIKeyHeader(name="X-API-Key")),
    x_timestamp: str = Depends(APIKeyHeader(name="X-Timestamp")),
    x_signature: str = Depends(APIKeyHeader(name="X-Signature")),
):
    client = await get_client_by_api_key(x_api_key)

    if client is None:
        raise HTTPException(401, "Invalid API key")

    hmac_auth = Hmac(client.secret)

    await hmac_auth.verify_request(request)

    return x_api_key
