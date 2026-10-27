# Páginas HTML (render_template) — RaspaUol

from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import ColetaNoticia, db
from services import buscar_noticias, persistir_coleta

site_bp = Blueprint("site", __name__)


@site_bp.route("/") #Erro: falta de @
def home():
    """GET / — home do RaspaUol com formulário e últimas coletas."""
    coletas = ColetaNoticia.listar()[:6]
    return render_template("home.html", coletas=coletas)


@site_bp.route("/buscar", methods=["POST"])
def buscar():
    """POST /buscar — formulário HTML → scraping (+ opcional salvar) → resultado."""
    modo = (request.form.get("modo") or "palavra").strip().lower()
    salvar = request.form.get("salvar") == "1"

    try:
        dados = buscar_noticias(modo=modo)
    except ValueError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("site.home"))
    except ConnectionError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("site.home"))

    coleta_id = None
    if salvar:
        coleta = persistir_coleta(dados)
        coleta_id = coleta.id
        flash(
            f"Coleta #{coleta.id} gravada — {dados['total']} notícia(s).",
            "sucesso",
        )

    return render_template(
        "resultado.html",
        dados=dados,
        coleta_id=coleta_id,
    )


@site_bp.route("/historico")
def historico():
    """GET /historico — lista HTML das coletas salvas."""
    return render_template("historico.html", coletas=ColetaNoticia.listar())


@site_bp.route("/historico/<int:coleta_id>")
def detalhe_coleta(coleta_id: int):
    """GET /historico/<id> — detalhe HTML de uma coleta."""
    coleta = db.session.get(ColetaNoticia, coleta_id)
    if not coleta:
        flash("Coleta não encontrada.", "erro")
        return redirect(url_for("site.historico"))
    return render_template("detalhe_coleta.html", coleta=coleta)
