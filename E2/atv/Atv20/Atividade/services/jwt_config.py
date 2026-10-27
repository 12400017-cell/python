# ATIVIDADE — callbacks JWT incompletos. Compare com a Aula 20 (pasta pai).

from flask import jsonify
from flask_jwt_extended import JWTManager

from models import TokenRevogado, Usuario

jwt = JWTManager()


def configurar_jwt(app):
    jwt.init_app(app)
    return jwt


@jwt.user_identity_loader
def identidade_do_usuario(usuario):
    if hasattr(usuario, "id"):
        return usuario.id
    return usuario


@jwt.user_lookup_loader
def carregar_usuario(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Usuario.query.filter_by(id=identity).one_or_none()


@jwt.additional_claims_loader
def claims_extras(identity):
    # TODO(segurança): o claim papel não entra no token. Admin nunca consegue
    # ser reconhecido pelo payload. Devolva {"papel": ..., "nome": ...}.
    return {}


@jwt.token_in_blocklist_loader
def token_esta_na_blocklist(_jwt_header, jwt_payload: dict) -> bool:
    # TODO(segurança): sempre False = logout não funciona. Consulte TokenRevogado.
    return False


@jwt.expired_token_loader
def token_expirado(_jwt_header, jwt_payload):
    return jsonify({"erro": "Token expirado", "tipo": jwt_payload.get("type")}), 401


@jwt.invalid_token_loader
def token_invalido(motivo: str):
    return jsonify({"erro": "Token inválido", "detalhe": motivo}), 401


@jwt.unauthorized_loader
def token_ausente(motivo: str):
    return jsonify({"erro": "Token ausente", "detalhe": motivo}), 401


@jwt.revoked_token_loader
def token_revogado(_jwt_header, _jwt_payload):
    return jsonify({"erro": "Token revogado (logout). Faça login de novo."}), 401


@jwt.needs_fresh_token_loader
def precisa_token_fresh(_jwt_header, _jwt_payload):
    return jsonify({"erro": "Esta operação exige um token fresh"}), 401


@jwt.user_lookup_error_loader
def usuario_sumiu(_jwt_header, _jwt_payload):
    return jsonify({"erro": "Usuário do token não existe mais"}), 401
