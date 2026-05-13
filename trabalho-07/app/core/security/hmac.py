from time import time
import base64
import hmac
import hashlib
from fastapi import Request, HTTPException


class Hmac:
    def __init__(self, key: str | bytes):
        self.key = key.encode("utf-8") if isinstance(key, str) else key

    async def build_payload(self, request: Request) -> str:
        body = await request.body()
        method = request.method
        path = request.url.path
        queries = "&".join(f"{k}={v}" for k, v in sorted(request.query_params.items()))
        timestamp = request.headers.get("X-Timestamp")

        body_hash = hashlib.sha256(body).hexdigest()

        payload = "\n".join(
            map(str, [method.upper(), path, queries, timestamp, body_hash])
        )
        return payload

    def sign_request(self, payload: str) -> str:
        mac = hmac.new(self.key, payload.encode("utf-8"), hashlib.sha256).digest()
        return base64.b64encode(mac).decode("utf-8")

    def verify_timestamp(self, timestamp: str) -> bool:
        now = int(time())
        ts = int(timestamp)

        return abs(now - ts) <= 30

    async def verify_request(
        self,
        request: Request,
    ) -> bool:
        timestamp = request.headers.get("X-Timestamp")
        if timestamp is None or not self.verify_timestamp(timestamp):
            raise HTTPException(status_code=401, detail="Request fora do intervalo de tempo de 30s.")

        mac_received = request.headers.get("X-Signature")

        if mac_received is None:
            raise HTTPException(status_code=401, detail="Assinatura de Requisição não recebida.")

        payload = await self.build_payload(request)
        mac = self.sign_request(payload)
        if not hmac.compare_digest(mac, mac_received):
            raise HTTPException(status_code=401, detail="Assinatura inválida.")

        return True
