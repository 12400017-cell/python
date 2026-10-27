# ATIVIDADE — radar e admin abertos. Recoloque jwt_required e a checagem de papel.

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, get_jwt, jwt_required

from models import TokenRevogado, Usuario
from services import listar_voos_radar

torre_api_bp = Blueprint("torre_api", __name__, url_prefix="/api/torre")


def _exige_admin():
    # TODO(segurança): recusar se get_jwt()["papel"] != "admin" (403).
    return None


@torre_api_bp.route("/saguao", methods=["GET"])
# TODO(segurança): rota parcial → @jwt_required(optional=True)
def saguao() -> Any:
    return jsonify({"lugar": "saguão", "logado": False, "mensagem": "Anônimo no saguão (sem optional JWT)."})


@torre_api_bp.route("/radar", methods=["GET"])
# TODO(segurança): qualquer um vê o radar. Use @jwt_required()
def radar() -> Any:
    return jsonify(
        {
            "mensagem": "Radar ABERTO (inseguro) — sem JWT",
            **listar_voos_radar(),
        }
    )


@torre_api_bp.route("/admin", methods=["GET"])
# TODO(segurança): precisa JWT + papel admin
def admin() -> Any:
    recusa = _exige_admin()
    if recusa:
        return recusa
    usuarios = [u.para_dict() for u in Usuario.listar()]
    return jsonify(
        {
            "mensagem": "Sala de controle SEM checagem de papel",
            "usuarios": usuarios,
            "total_usuarios": len(usuarios),
        }
    )


@torre_api_bp.route("/blocklist", methods=["GET"])
# TODO(segurança): só admin, com JWT
def blocklist() -> Any:
    tokens = TokenRevogado.listar()
    return jsonify({"banco": "blocklist.db", "total": len(tokens), "tokens": [t.para_dict() for t in tokens]})
