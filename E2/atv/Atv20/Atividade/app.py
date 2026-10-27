# ATIVIDADE Aula 20 — TorreJWT INSEGURA (o aluno arruma a segurança).
# A aula resolvida está na pasta pai: flask/Aula20seguranca/
#
# Docs: https://flask-jwt-extended.readthedocs.io/en/stable/
#
# Banco 1 (principal.db): Usuario — bind padrão.
# Banco 2 (blocklist.db): TokenRevogado — bind "seguranca" (logout / revogação).
#
# Front: TorreJWT (render_template + JS) + API JSON em /api/*

import os
from datetime import timedelta

from flask import Flask, jsonify

from controllers import auth_api_bp, site_bp, torre_api_bp
from models import db
from services import configurar_jwt, popular_usuarios

ENDPOINTS: list[dict[str, str]] = [
    {
        "metodo": "POST",
        "rota": "/api/auth/registrar",
        "descricao": "Cadastra visitante e devolve access + refresh (fresh)",
        "auth": "público",
    },
    {
        "metodo": "POST",
        "rota": "/api/auth/login",
        "descricao": "Login → access_token (fresh) + refresh_token",
        "auth": "público",
    },
    {
        "metodo": "POST",
        "rota": "/api/auth/refresh",
        "descricao": "Gera access novo (não fresh) a partir do refresh_token",
        "auth": "Bearer refresh",
    },
    {
        "metodo": "DELETE",
        "rota": "/api/auth/logout",
        "descricao": "Revoga o token enviado (access ou refresh) na blocklist",
        "auth": "Bearer access|refresh",
    },
    {
        "metodo": "GET",
        "rota": "/api/auth/eu",
        "descricao": "current_user + claims do JWT (Automatic User Loading)",
        "auth": "Bearer access",
    },
    {
        "metodo": "POST",
        "rota": "/api/auth/senha",
        "descricao": "Troca senha — exige token fresh (Token Freshness Pattern)",
        "auth": "Bearer access fresh",
    },
    {
        "metodo": "GET",
        "rota": "/api/torre/saguao",
        "descricao": "Rota parcial: jwt_required(optional=True)",
        "auth": "opcional",
    },
    {
        "metodo": "GET",
        "rota": "/api/torre/radar",
        "descricao": "Painel de voos — só com crachá (JWT)",
        "auth": "Bearer access",
    },
    {
        "metodo": "GET",
        "rota": "/api/torre/admin",
        "descricao": "Sala de controle — claim papel == admin",
        "auth": "Bearer access + papel admin",
    },
    {
        "metodo": "GET",
        "rota": "/api/torre/blocklist",
        "descricao": "Lista tokens revogados no blocklist.db",
        "auth": "Bearer access + papel admin",
    },
]


def criar_app() -> Flask:
    """
    Monta a aplicação Flask: pastas de template/static, dois bancos SQLite,
    JWT-Extended, blueprints, tabelas, usuários de demonstração.
    """
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )
    pasta = os.path.abspath(os.path.dirname(__file__))

    # Dois bancos SQLite (mesmo padrão da Aula 19).
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "principal.db"
    )
    app.config["SQLALCHEMY_BINDS"] = {
        "seguranca": "sqlite:///" + os.path.join(pasta, "blocklist.db"),
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "aula20-torre-jwt-dev"

    # ATIVIDADE: esta config está INSEGURA de propósito. Arrume.
    # TODO(segurança): chave fraca — qualquer um forja JWT. Use um segredo forte (e não commite).
    app.config["JWT_SECRET_KEY"] = "123"
    # TODO(segurança): access não pode valer 1 ano. Na aula era 15 minutos.
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=365)
    # TODO(segurança): refresh longo demais para exercício em sala.
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=365)
    # TODO(segurança): token na query string vaza em log/histórico. Use ["headers"].
    app.config["JWT_TOKEN_LOCATION"] = ["query_string"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"

    db.init_app(app)
    configurar_jwt(app)

    app.register_blueprint(site_bp)
    app.register_blueprint(auth_api_bp)
    app.register_blueprint(torre_api_bp)

    with app.app_context():
        db.create_all()
        popular_usuarios()

    @app.route("/api")
    def api_index():
        """GET /api — índice JSON com a lista de endpoints (documentação rápida)."""
        return jsonify(
            {
                "aula": "20 — TorreJWT · Flask-JWT-Extended",
                "docs": "https://flask-jwt-extended.readthedocs.io/en/stable/",
                "site": "/",
                "bancos": {
                    "principal": "principal.db (Usuario)",
                    "seguranca": "blocklist.db (TokenRevogado)",
                },
                "demo": {
                    "admin": "admin / admin123",
                    "piloto": "piloto / piloto123",
                    "visitante": "visitante / visitante123",
                },
                "header": "Authorization: Bearer <access_token>",
                "endpoints": ENDPOINTS,
            }
        )

    return app


app = criar_app()

if __name__ == "__main__":
    # Sobe o servidor de desenvolvimento (debug=True recarrega ao salvar arquivos).
    app.run(debug=True)
