# Lê coletas já gravadas (não chama a fonte de novo).

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify

from models import ColetaNoticia, db

historico_api_bp = Blueprint("historico_api", __name__, url_prefix="/api/historico") #Erro: Antes do parenteses é nescessário colocar o blueprint


@historico_api_bp.route("/coletas", methods=[])
def listar_coletas() -> Any:
    """GET /api/historico/coletas — lista coletas salvas."""
    coletas = ColetaNoticia.listar()
    return jsonify([c.para_dict() for c in coletas])


@historico_api_bp.route("/coletas/<int:coleta_id>", methods=["GET"])
def detalhe_coleta(coleta_id: int) -> Any:
    """GET /api/historico/coletas/<id> — detalhe com notícias."""
    coleta = db.session.get(ColetaNoticia, coleta_id)
    if not coleta:
        return jsonify({"erro": "Coleta não encontrada"}), 404
    return jsonify(coleta.para_dict(incluir_noticias=True))
