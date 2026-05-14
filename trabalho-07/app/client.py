from uuid import UUID
import asyncio
from datetime import datetime
import httpx
from app.core.security.hmac import Hmac
from app.modules.products.schemas import ProductCreate, ProductUpdate


async def get_products(hmac: Hmac):
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        timestamp = str(int(datetime.now().timestamp()))
        payload = await hmac.build_payload(("", "GET", "/products", "", timestamp))
        mac = hmac.sign_request(payload)

        # alterando o mac gerado para ficar incorreto
        # mac = f"{mac}{123}"

        headers = {
            "X-API-Key": "APP-01",
            "X-Timestamp": timestamp,
            "X-Signature": mac,
        }

        response = await client.get("/products", headers=headers)
        print(f"\nStatus da Requisição={response.status_code}\n")
        print(f"Resposta={response.text}\n")


async def get_product_by_id(hmac: Hmac, product_id: UUID):
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        timestamp = str(int(datetime.now().timestamp()))
        path = f"/products/{product_id}"
        payload = await hmac.build_payload(("", "GET", path, "", timestamp))
        mac = hmac.sign_request(payload)

        # alterando o mac gerado para ficar incorreto
        # mac = f"{mac}{123}"

        headers = {
            "X-API-Key": "APP-01",
            "X-Timestamp": timestamp,
            "X-Signature": mac,
        }

        response = await client.get(path, headers=headers)
        print(f"\nStatus da Requisição={response.status_code}\n")
        print(f"Resposta={response.text}\n")


async def create_product(hmac: Hmac, product_create: ProductCreate):
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        timestamp = str(int(datetime.now().timestamp()))
        product = product_create.model_dump_json()

        payload = await hmac.build_payload(
            (product, "POST", "/products", "", timestamp)
        )
        mac = hmac.sign_request(payload)

        # alterando o mac gerado para ficar incorreto
        # mac = f"{mac}{123}"

        headers = {
            "X-API-Key": "APP-01",
            "X-Timestamp": timestamp,
            "X-Signature": mac,
        }

        body = {
            "name": product_create.name,
            "description": product_create.description,
            "cost_price": product_create.cost_price,
            "sell_price": product_create.sell_price,
        }
        response = await client.post("/products", headers=headers, json=body)
        print(f"\nStatus da Requisição={response.status_code}\n")
        print(f"Resposta={response.text}\n")


async def delete_product(hmac: Hmac, product_id: UUID):
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        timestamp = str(int(datetime.now().timestamp()))
        path = f"/products/{product_id}"
        payload = await hmac.build_payload(("", "DELETE", path, "", timestamp))
        mac = hmac.sign_request(payload)

        # alterando o mac gerado para ficar incorreto
        # mac = f"{mac}{123}"

        headers = {
            "X-API-Key": "APP-01",
            "X-Timestamp": timestamp,
            "X-Signature": mac,
        }

        response = await client.delete(path, headers=headers)
        print(f"\nStatus da Requisição={response.status_code}\n")
        print(f"Resposta={response.text}\n")


async def main() -> None:
    operation = None
    hmac = Hmac("J32Omu/0/qCX4WY44fydlX85LY5xIKz+qPiumT/aqUw=")

    while operation != 6:
        print("Cliente - APP-01")
        print("[1] - Buscar todos produtos")
        print("[2] - Buscar produtos por ID")
        print("[3] - Criar produto")
        print("[4] - Atualizar produto")
        print("[5] - Remover produto")
        print("[6] Sair")

        operation = input("Escolha a opção: ")
        if not operation.isnumeric():
            print("Operação inválida.")
            continue

        operation = int(operation)

        match operation:
            case 1:
                await get_products(hmac)
            case 2:
                product_id = UUID(input("ID:"))
                await get_product_by_id(hmac, product_id)
            case 3:
                name = input("Nome:")
                description = input("Descrição:")
                cost_price = float(input("Preço de custo:"))
                sell_price = float(input("Preço de venda:"))
                product_create = ProductCreate(
                    name=name,
                    description=description,
                    cost_price=cost_price,
                    sell_price=sell_price,
                )
                await create_product(hmac, product_create)
            case 4:
                pass
            case 5:
                product_id = UUID(input("ID:"))
                await delete_product(hmac, product_id)
            case 6:
                break

            case _:
                print("Operação inválida.\n")


if __name__ == "__main__":
    asyncio.run(main())
