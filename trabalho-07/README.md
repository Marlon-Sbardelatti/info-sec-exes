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
2. Seed:

Uma seed.sql esta disponível para mock de dados, basta executar no banco sqlite3.

3. Migrações: 

As migrações deste projeto são gerenciadas através do alembic, para estar atualizado execute: 

```bash
alembic upgrade head
```

4. Client:

Para testar a aplicação foi desenvolvido um client que realiza os requests autenticados através de um menu, para utilizá-lo execute:


```bash
python3 -m app.client
```
