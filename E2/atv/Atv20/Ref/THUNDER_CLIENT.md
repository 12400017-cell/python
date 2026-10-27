# Thunder Client — TorreJWT (Aula 20)

Na versão gratuita o **Import** de coleção costuma não funcionar. Monte os requests na mão.

Objetivo: login → access + refresh → rota protegida → refresh (token deixa de ser fresh) → logout (blocklist).

Docs: [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)

## Passo 1 — Subir a API

```powershell
cd flask/Aula20seguranca
pip install -r requirements.txt
python app.py
```

Deixe rodando em `http://127.0.0.1:5000`.

## Passo 2 — Índice (GET, sem token)

| Campo | Valor |
|-------|--------|
| Método | `GET` |
| URL | `http://127.0.0.1:5000/api` |

## Passo 3 — Saguão sem crachá (optional JWT)

| Campo | Valor |
|-------|--------|
| Método | `GET` |
| URL | `http://127.0.0.1:5000/api/torre/saguao` |

Resposta: `"logado": false`.

## Passo 4 — Login (POST)

| Campo | Valor |
|-------|--------|
| Método | `POST` |
| URL | `http://127.0.0.1:5000/api/auth/login` |

Header: `Content-Type` = `application/json`

Body:

```json
{
    "username": "piloto",
    "senha": "piloto123"
}
```

**Send** → status **200**. Copie `access_token` e `refresh_token`.

## Passo 5 — Radar (protegido)

**New Request**

| Campo | Valor |
|-------|--------|
| Método | `GET` |
| URL | `http://127.0.0.1:5000/api/torre/radar` |

Auth: Bearer Token → cole o `access_token`
(ou Header `Authorization` = `Bearer <access_token>`).

## Passo 6 — Sala admin com piloto (deve falhar)

`GET http://127.0.0.1:5000/api/torre/admin` com o token do piloto.

Esperado: **403** (`papel_atual`: piloto).

Refaça o login como `admin` / `admin123` e tente de novo → **200**.

## Passo 7 — Refresh (access deixa de ser fresh)

| Campo | Valor |
|-------|--------|
| Método | `POST` |
| URL | `http://127.0.0.1:5000/api/auth/refresh` |

Auth: Bearer → o **refresh_token** (não o access).

Guarde o `access_token` novo.

## Passo 8 — Trocar senha com token do refresh (deve falhar)

`POST http://127.0.0.1:5000/api/auth/senha`

Body:

```json
{
    "senha_atual": "piloto123",
    "senha_nova": "piloto123"
}
```

Com o access **do refresh** → **401** (precisa token fresh).
Com o access **do login** → **200**.

## Passo 9 — Logout (blocklist)

`DELETE http://127.0.0.1:5000/api/auth/logout` com o access.

Depois `GET /api/torre/radar` com o mesmo access → **401** (token revogado).

Repita o DELETE com o **refresh_token** para ele também ir para o `blocklist.db`.
