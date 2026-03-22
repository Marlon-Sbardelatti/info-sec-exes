import datetime
import re
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
import uvicorn

DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String)


class LoginAttempt(Base):
    __tablename__ = "login_attempts"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    ip_address = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())
    blocked_at = Column(DateTime, nullable=True)


Base.metadata.create_all(bind=engine)

app = FastAPI()


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class WeakPasswordError(HTTPException):
    def __init__(self, message: Optional[str] = "Senha fraca."):
        super().__init__(status_code=400, detail=message)


# Rota para registrar usuário
@app.post("/register/")
def register_user(
    request: Request, payload: RegisterRequest, db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário já existe"
        )

    # prevenções contra senhas fracas
    if len(payload.password) < 15:
        raise WeakPasswordError(message="A senha deve ter no mínimo 15 caracteres.")

    special_chars = re.findall(r"\W", payload.password)
    if not special_chars:
        raise WeakPasswordError(
            message="A senha deve ter no mínimo 1 caracter especial."
        )

    capital_letters = re.search(r"[A-Z]", payload.password)
    if not capital_letters:
        raise WeakPasswordError(
            message="A senha deve conter pelo menos 1 letra maiúscula."
        )

    if payload.username in payload.password or payload.email in payload.password:
        raise WeakPasswordError(
            message="Não utilize suas informações pessoais na senha."
        )

    user = User(
        username=payload.username, email=payload.email, password=payload.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Usuário registrado com sucesso!"}


# Rota de login
@app.post("/login/")
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    # Restringe tentativas por IP
    ip_address = _verify_ip_attempts(request, db)

    # Bloqueio temporário de contas
    _verify_user_attempts(payload, db)

    user = (
        db.query(User)
        .filter(User.username == payload.username, User.password == payload.password)
        .first()
    )

    if not user:
        one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
        consecutive_attempts = (
            db.query(func.count(LoginAttempt.id))
            .filter(
                LoginAttempt.username == payload.username,
                LoginAttempt.created_at >= one_minute_ago,
            )
            .scalar()
        )

        # Marca como bloqueado terceira tentativa consecutiva para o mesmo usuário
        blocked_at = None
        if consecutive_attempts + 1 >= 2:
            blocked_at = datetime.datetime.now()

        # Registra tentativa de login por IP e conta alvo
        attempt = LoginAttempt(
            username=payload.username, ip_address=ip_address, blocked_at=blocked_at
        )

        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )

    return {"message": "Login realizado com sucesso!"}


def _verify_ip_attempts(request: Request, db: Session = Depends(get_db)) -> str:
    five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)

    ip = request.client.host

    ip_attempts = (
        db.query(func.count(LoginAttempt.id))
        .filter(
            LoginAttempt.ip_address == ip,
            LoginAttempt.created_at >= five_minutes_ago,
        )
        .scalar()
    )

    if ip_attempts >= 9:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limite de requisições por IP excedido. Tente novamente mais tarde.",
        )
    return ip


def _verify_user_attempts(payload: LoginRequest, db: Session = Depends(get_db)) -> None:
    five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)

    last_attempt = (
        db.query(LoginAttempt)
        .filter(
            LoginAttempt.username == payload.username,
            LoginAttempt.blocked_at >= five_minutes_ago,
        )
        .first()
    )

    if last_attempt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário bloqueado por 5 minutos.",
        )


# Inicialização direta do servidor
if __name__ == "__main__":
    uvicorn.run("servico:app", host="0.0.0.0", port=8000, reload=False)
