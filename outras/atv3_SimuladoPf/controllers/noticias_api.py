# API JSON — scraping + sincronização no histórico.
from __future__ import annotations

from typing import Any

from flask import  jsonify, request, Blueprint #erro, virgola antes do jsonify e falta de import do blueprints

from services import buscar_noticias, persistir_coleta

noticias_api_bp = Blueprint("noticias_api", __name__, url_prefix="/api")


def _validar_modo() -> str | tuple[Any, int]:
    """Valida ?modo=palavra|todos. Sucesso → str; erro → (json, status)."""
    modo = request.args.get("modo", "palavra").strip().lower()
    if modo not in ("palavra", "todos"):
        return jsonify({"erro": "Parâmetro modo deve ser 'palavra' ou 'todos'"}), 400
    return modo


@noticias_api_bp.route("/noticias", methods=["GET"])
def listar_noticias() -> Any:
    """GET /api/noticias — scraping ao vivo em economia.uol.com.br (não grava)."""
    modo = _validar_modo()
    if isinstance(modo, tuple):
        return modo

    try:
        dados = buscar_noticias(modo=modo)
    except ConnectionError as erro:
        return jsonify({"erro": str(erro)}), 502
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    return jsonify(dados)


@noticias_api_bp.route("/noticias/sincronizar", methods=[""])
def sincronizar_noticias() -> Any:
    """POST /api/noticias/sincronizar — scraping + grava no historico_noticias.db."""
    modo = _validar_modo()
    if isinstance(modo, tuple):
        return modo

    try:
        dados = buscar_noticias(modo=modo)
    except ConnectionError as erro:
        return jsonify({"erro": str(erro)}), 502
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    coleta = persistir_coleta(dados)
    return jsonify(
        {
            "mensagem": "Coleta gravada no historico_noticias.db",
            "coleta_id": coleta.id,
            "dados_api": dados,
        }
    ), 201


@noticias_api_bp.route("/noticias/manual", methods=["POST"])
def cadastrar_noticia_manual() -> Any:
    """
    POST /api/noticias/manual — cadastra UMA notícia à mão (para Thunder Client).
    Body JSON:
      { "titulo": "Meu título", "url": "https://...", "secao": "manual" }
    """
    body = request.get_json(silent=True) or {}
    titulo = (body.get("titulo") or "").strip()
    url = (body.get("url") or "").strip()
    secao = (body.get("secao") or "manual").strip() or "manual"

    if not titulo or not url:
        return jsonify({"erro": "Informe 'titulo' e 'url' no JSON"}), 400

    dados = {
        "fonte": "manual",
        "modo_busca": "manual",
        "total": 1,
        "noticias": [
            {
                "titulo": titulo,
                "url": url,
                "secao": secao,
            }
        ],
    }
    coleta = persistir_coleta(dados)  # type: ignore[arg-type]
    return jsonify(
        {
            "mensagem": "Notícia manual gravada no historico_noticias.db",
            "coleta_id": coleta.id,
            "noticia": dados["noticias"][0],
        }
    ), 201
