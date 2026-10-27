# Aula 20 — TorreJWT: segurança com Flask-JWT-Extended

Igual à [Aula 19](../Aula19Webscraping) na estrutura (app, controllers, models, services, views, dois SQLite), trocando o scraping por **autenticação JWT** segundo a [documentação oficial](https://flask-jwt-extended.readthedocs.io/en/stable/).

## Site (render_template)

| Rota | Página |
|------|--------|
| GET `/` | Home — crachá + playground que chama a API |
| GET `/praticas` | Mapa docs → código |

## Dois bancos SQLite

| Arquivo | Uso |
|---------|-----|
| `principal.db` | `Usuario` (bind padrão) |
| `blocklist.db` | `TokenRevogado` (bind `seguranca`, logout) |

## API JSON

| Método | Rota | Auth |
|--------|------|------|
| GET | `/api` | público |
| POST | `/api/auth/registrar` | público |
| POST | `/api/auth/login` | público |
| POST | `/api/auth/refresh` | refresh token |
| DELETE | `/api/auth/logout` | access ou refresh |
| GET | `/api/auth/eu` | access |
| POST | `/api/auth/senha` | access **fresh** |
| GET | `/api/torre/saguao` | opcional |
| GET | `/api/torre/radar` | access |
| GET | `/api/torre/admin` | access + papel admin |
| GET | `/api/torre/blocklist` | access + papel admin |

Header: `Authorization: Bearer <token>`

## Usuários de demonstração

| username | senha | papel |
|----------|--------|--------|
| `admin` | `admin123` | admin |
| `piloto` | `piloto123` | piloto |
| `visitante` | `visitante123` | visitante |

## Rodar

```powershell
cd flask/Aula20seguranca
pip install -r requirements.txt
python app.py
```

Abra: http://127.0.0.1:5000

Roteiro curto: `Aula20.txt`. Guia para dar a aula: `GUIA_PROFESSOR.md`. Thunder Client: `THUNDER_CLIENT.md`. Ponte front↔API: `dica.md`.

**Atividade (aluno arruma a segurança):** [`Atividade/Atividade.txt`](Atividade/Atividade.txt)
