from fastapi import FastAPI
from app.modules.users import router as users
 
app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"message": "Bem-vindo à API!"}

