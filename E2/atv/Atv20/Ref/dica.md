A ponte principal é o `views/static/js/torre.js` — o HTML não “loga” no Flask com session de cookie; o formulário chama a API JSON, igual ao Thunder Client.

1. App registra o front, o JWT e as APIs juntos

app.py
```
def criar_app() -> Flask:
    app = Flask(..., template_folder="views/templates", static_folder="views/static")
    configurar_jwt(app)              # ← callbacks da docs
    app.register_blueprint(site_bp)  # ← front (HTML)
    app.register_blueprint(auth_api_bp)
    app.register_blueprint(torre_api_bp)
```

2. Form da home dispara fetch, não POST clássico

home.html — `id="form-login"` sem action.
torre.js — `POST /api/auth/login` com JSON `{ username, senha }`.

3. Token vai no header (JWT Locations → Headers)

```
Authorization: Bearer <access_token>
```

O access (15 min, fresh no login) abre radar/eu/admin.
O refresh (1 dia) só entra em `POST /api/auth/refresh`.
Logout grava o `jti` em `blocklist.db` — o mesmo token deixa de passar.

Fluxo resumido:

HTML form → JS fetch → auth_api / torre_api → services (emitir_tokens, blocklist) → jsonify

O front e o Thunder Client não se falam; os dois consomem a mesma API.
