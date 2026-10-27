# ATIVIDADE — rotas de auth SEM proteção JWT. Recoloque os decorators.

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
    return request.get_json(silent=True) or {}


@auth_api_bp.route("/registrar", methods=["POST"])
def criar_conta() -> Any:
    try:
        usuario = registrar(_json())
    except ValueError as erro:
        status = 409 if "já cadastrado" in str(erro) else 400
        return jsonify({"erro": str(erro)}), status
    return jsonify({"mensagem": "Conta criada.", **emitir_tokens(usuario, fresh=True)}), 201


@auth_api_bp.route("/login", methods=["POST"])
def login() -> Any:
    dados = _json()
    try:
        usuario = autenticar(dados.get("username"), dados.get("senha"))
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 401
    return jsonify({"mensagem": "Crachá emitido.", **emitir_tokens(usuario, fresh=True)})


@auth_api_bp.route("/refresh", methods=["POST"])
# TODO(segurança): só o refresh_token pode entrar aqui → @jwt_required(refresh=True)
def refresh() -> Any:
    return jsonify(renovar_access(current_user))


@auth_api_bp.route("/logout", methods=["DELETE"])
# TODO(segurança): precisa de token (access OU refresh) → @jwt_required(verify_type=False)
def logout() -> Any:
    return jsonify({"mensagem": "Logout fake (sem JWT e sem blocklist)."})


@auth_api_bp.route("/eu", methods=["GET"])
# TODO(segurança): rota protegida → @jwt_required()
def eu() -> Any:
    return jsonify({"aviso": "Rota /eu aberta — qualquer um consulta. Proteja com @jwt_required()."})


@auth_api_bp.route("/senha", methods=["POST"])
# TODO(segurança): troca de senha exige token FRESH → @jwt_required(fresh=True)
def senha() -> Any:
    dados = _json()
    try:
        trocar_senha(current_user, dados.get("senha_atual"), dados.get("senha_nova"))
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    return jsonify({"mensagem": "Senha atualizada."})
