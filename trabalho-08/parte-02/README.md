## Exemplo .env

```.env
DB_URL=sqlite:///uri_conexão
```
---

## Instruções de uso

1. Para rodar a aplicação podemos utilizar: 

Caso a cli make esteja disponível no sistema: 

```bash
make run
```
ou

```bash
uvicorn app.main:app --reload
```
