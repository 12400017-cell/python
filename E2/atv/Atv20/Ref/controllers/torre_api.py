# Rotas da torre: pública parcial, protegida e admin (claims extras).

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, get_jwt, jwt_required

from models import TokenRevogado, Usuario
from services import listar_voos_radar

torre_api_bp = Blueprint("torre_api", __name__, url_prefix="/api/torre")


def _exige_admin():
    """403 se o claim papel não for admin (Storing Additional Data in JWTs)."""
    if get_jwt().get("papel") != "admin":
        return jsonify(
            {
                "erro": "Sala de controle só para papel admin",
                "papel_atual": get_jwt().get("papel"),
            }
        ), 403
    return None


@torre_api_bp.route("/saguao", methods=["GET"])
@jwt_required(optional=True)
def saguao() -> Any:
    """
    GET /api/torre/saguao — Partially protecting routes (optional=True).
    Sem JWT: visitante anônimo. Com JWT válido: cumprimento pelo current_user.
    JWT expirado/inválido ainda gera erro (não vira anônimo).
    """
    if current_user:
        return jsonify(
            {
                "lugar": "saguão",
                "logado": True,
                "mensagem": f"Olá, {current_user.nome}. Passe o crachá no radar.",
                "papel": current_user.papel,
            }
        )
    return jsonify(
        {
            "lugar": "saguão",
            "logado": False,
            "mensagem": "Você está no saguão. Faça login para entrar na torre.",
        }
    )


@torre_api_bp.route("/radar", methods=["GET"])
@jwt_required()
def radar() -> Any:
    """GET /api/torre/radar — Basic Usage: rota protegida (qualquer usuário logado)."""
    return jsonify(
        {
            "mensagem": f"Radar liberado para {current_user.nome}",
            "papel": current_user.papel,
            **listar_voos_radar(),
        }
    )


@torre_api_bp.route("/admin", methods=["GET"])
@jwt_required()
def admin() -> Any:
    """GET /api/torre/admin — só quem tem claim papel=admin."""
    recusa = _exige_admin()
    if recusa:
        return recusa

    usuarios = [u.para_dict() for u in Usuario.listar()]
    return jsonify(
        {
            "mensagem": "Sala de controle da torre",
            "admin": current_user.para_dict(),
            "usuarios": usuarios,
            "total_usuarios": len(usuarios),
        }
    )


@torre_api_bp.route("/blocklist", methods=["GET"])
@jwt_required()
def blocklist() -> Any:
    """GET /api/torre/blocklist — admin vê os jti revogados no blocklist.db."""
    recusa = _exige_admin()
    if recusa:
        return recusa

    tokens = TokenRevogado.listar()
    return jsonify(
        {
            "banco": "blocklist.db",
            "total": len(tokens),
            "tokens": [t.para_dict() for t in tokens],
        }
    )
