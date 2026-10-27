# Páginas HTML (render_template) — TorreJWT
# O formulário da home não posta senha no Flask: o JS chama a API JSON.

from __future__ import annotations

from flask import Blueprint, render_template

from services import USUARIOS_DEMO

site_bp = Blueprint("site", __name__)


@site_bp.route("/")
def home():
    """GET / — home da torre: teoria JWT + playground que fala com /api/*."""
    return render_template("home.html", usuarios=USUARIOS_DEMO)


@site_bp.route("/praticas")
def praticas():
    """GET /praticas — mapa das práticas da documentação usadas nesta aula."""
    return render_template("praticas.html")
