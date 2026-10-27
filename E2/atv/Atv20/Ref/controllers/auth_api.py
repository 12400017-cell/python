# Rotas de autenticação (Basic Usage + Refresh + Freshness + Logout/blocklist).

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, get_jwt, jwt_required

from services import (
    autenticar,
    emitir_tokens,
    registrar,
    renovar_access,
    revogar_jwt_atual,
    trocar_senha,
)

auth_api_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")


def _json() -> dict:
    """Lê o body JSON sem estourar se vier vazio."""
    return request.get_json(silent=True) or {}


@auth_api_bp.route("/registrar", methods=["POST"])
def criar_conta() -> Any:
    """POST /api/auth/registrar — cadastra visitante e já devolve tokens fresh."""
    try:
        usuario = registrar(_json())
    except ValueError as erro:
        status = 409 if "já cadastrado" in str(erro) else 400
        return jsonify({"erro": str(erro)}), status

    return jsonify(
        {
            "mensagem": "Conta criada. Papel: visitante.",
            **emitir_tokens(usuario, fresh=True),
        }
    ), 201


@auth_api_bp.route("/login", methods=["POST"])
def login() -> Any:
    """POST /api/auth/login — Basic Usage: identity + access (fresh) + refresh."""
    dados = _json()
    try:
        usuario = autenticar(dados.get("username"), dados.get("senha"))
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 401

    return jsonify(
        {
            "mensagem": "Crachá emitido. Access é fresh até expirar ou você usar /refresh.",
            **emitir_tokens(usuario, fresh=True),
        }
    )


@auth_api_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh() -> Any:
    """
    POST /api/auth/refresh — Explicit Refreshing With Refresh Tokens.
    Header: Authorization: Bearer <refresh_token>
    O access novo NÃO é fresh (Token Freshness Pattern).
    """
    return jsonify(renovar_access(current_user))


@auth_api_bp.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
def logout() -> Any:
    """
    DELETE /api/auth/logout — aceita access OU refresh (verify_type=False).
    Chame duas vezes (um token de cada) para encerrar a sessão de verdade.
    """
    return jsonify(revogar_jwt_atual())


@auth_api_bp.route("/eu", methods=["GET"])
@jwt_required()
def eu() -> Any:
    """GET /api/auth/eu — Automatic User Loading: current_user + get_jwt()."""
    claims = get_jwt()
    return jsonify(
        {
            "usuario": current_user.para_dict(),
            "claims": {
                "sub": claims.get("sub"),
                "papel": claims.get("papel"),
                "nome": claims.get("nome"),
                "fresh": claims.get("fresh"),
                "type": claims.get("type"),
                "jti": claims.get("jti"),
                "exp": claims.get("exp"),
            },
        }
    )


@auth_api_bp.route("/senha", methods=["POST"])
@jwt_required(fresh=True)
def senha() -> Any:
    """
    POST /api/auth/senha — Token Freshness Pattern.
    Só funciona com access emitido no login (fresh=True), não no /refresh.
    Body: { "senha_atual": "...", "senha_nova": "..." }
    """
    dados = _json()
    try:
        trocar_senha(
            current_user,
            dados.get("senha_atual"),
            dados.get("senha_nova"),
        )
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    return jsonify({"mensagem": "Senha atualizada. Os tokens antigos continuam válidos até expirar ou logout."})
