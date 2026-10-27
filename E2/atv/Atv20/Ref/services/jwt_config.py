# Callbacks do Flask-JWT-Extended:
# https://flask-jwt-extended.readthedocs.io/en/stable/
#
# Automatic User Loading, additional claims, blocklist e mensagens em português.

from flask import jsonify
from flask_jwt_extended import JWTManager

from models import TokenRevogado, Usuario

jwt = JWTManager()


def configurar_jwt(app):
    """Liga o JWTManager ao Flask (depois das configs JWT_* no app)."""
    jwt.init_app(app)
    return jwt


@jwt.user_identity_loader
def identidade_do_usuario(usuario):
    """
    Converte o objeto passado em create_access_token(identity=...)
    para um valor JSON (vai no claim "sub").
    """
    if hasattr(usuario, "id"):
        return usuario.id
    return usuario


@jwt.user_lookup_loader
def carregar_usuario(_jwt_header, jwt_data):
    """
    Recarrega o Usuario do banco a cada rota protegida.
    Resultado fica em current_user. None → 401 (user_lookup_error_loader).
    """
    identity = jwt_data["sub"]
    return Usuario.query.filter_by(id=identity).one_or_none()


@jwt.additional_claims_loader
def claims_extras(identity):
    """
    Storing Additional Data in JWTs: papel e nome entram no payload
    (além do "sub"). A rota lê com get_jwt()["papel"].
    """
    if hasattr(identity, "papel"):
        return {"papel": identity.papel, "nome": identity.nome}
    usuario = Usuario.query.filter_by(id=identity).one_or_none()
    if usuario:
        return {"papel": usuario.papel, "nome": usuario.nome}
    return {"papel": "visitante"}


@jwt.token_in_blocklist_loader
def token_esta_na_blocklist(_jwt_header, jwt_payload: dict) -> bool:
    """
    JWT Revoking / Blocklist (docs, seção Database).
    True = token revogado → rota protegida responde 401.
    """
    jti = jwt_payload["jti"]
    return TokenRevogado.esta_revogado(jti)


@jwt.expired_token_loader
def token_expirado(_jwt_header, jwt_payload):
    return jsonify(
        {
            "erro": "Token expirado",
            "tipo": jwt_payload.get("type"),
            "dica": "Use POST /api/auth/refresh com o refresh_token",
        }
    ), 401


@jwt.invalid_token_loader
def token_invalido(motivo: str):
    return jsonify({"erro": "Token inválido", "detalhe": motivo}), 401


@jwt.unauthorized_loader
def token_ausente(motivo: str):
    return jsonify(
        {
            "erro": "Token ausente",
            "detalhe": motivo,
            "dica": "Header Authorization: Bearer <access_token>",
        }
    ), 401


@jwt.revoked_token_loader
def token_revogado(_jwt_header, _jwt_payload):
    return jsonify({"erro": "Token revogado (logout). Faça login de novo."}), 401


@jwt.needs_fresh_token_loader
def precisa_token_fresh(_jwt_header, _jwt_payload):
    return jsonify(
        {
            "erro": "Esta operação exige um token fresh",
            "dica": "Faça POST /api/auth/login de novo (o refresh não gera token fresh)",
        }
    ), 401


@jwt.user_lookup_error_loader
def usuario_sumiu(_jwt_header, _jwt_payload):
    return jsonify({"erro": "Usuário do token não existe mais no principal.db"}), 401
