from fastapi import FastAPI
from app.modules.products import router as products
 
app = FastAPI()

app.include_router(products.router)

@app.get("/")
async def read_root():
    return {"message": "Bem-vindo à API!"}
