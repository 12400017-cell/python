from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Viajante, Viagem, db
from services import buscar_clima_destino

viagens_bp = Blueprint("viagens", __name__)


@viagens_bp.route("/")
def home():
    viagens = Viagem.listar()[:8]
    viajantes = Viajante.listar()
    return render_template("home.html", viagens=viagens, viajantes=viajantes)


@viagens_bp.route("/viajantes", methods=["GET", "POST"])
def viajantes():
    if request.method == "POST":
        try:
            viajante = Viajante.a_partir_de_dict(request.form)
        except ValueError as erro:
            flash(str(erro), "erro")
            return redirect(url_for("viagens.viajantes"))

        if Viajante.query.filter_by(nome=viajante.nome).first():
            flash(f"Viajante '{viajante.nome}' já cadastrado.", "erro")
            return redirect(url_for("viagens.viajantes"))

        db.session.add(viajante)
        db.session.commit()
        flash(f"{viajante.nome} cadastrado(a) com sucesso.", "sucesso")
        return redirect(url_for("viagens.viajantes"))

    return render_template("viajantes.html", viajantes=Viajante.listar())


@viagens_bp.route("/viajantes/<int:viajante_id>")
def detalhe_viajante(viajante_id):
    viajante = db.session.get(Viajante, viajante_id)
    if not viajante:
        flash("Viajante não encontrado.", "erro")
        return redirect(url_for("viagens.viajantes"))

    lista = viajante.viagens.order_by(Viagem.id.desc()).all()
    return render_template("detalhe_viajante.html", viajante=viajante, viagens=lista)


@viagens_bp.route("/nova-viagem", methods=["GET", "POST"])
def nova_viagem():
    viajantes = Viajante.listar()

    if request.method == "POST":
        viajante_id = request.form.get("viajante_id")
        destino = (request.form.get("destino") or "").strip()

        if not viajante_id or not destino:
            flash("Selecione o viajante e informe o destino.", "erro")
            return render_template("nova_viagem.html", viajantes=viajantes), 400

        viajante = db.session.get(Viajante, int(viajante_id))
        if not viajante:
            flash("Viajante não encontrado.", "erro")
            return render_template("nova_viagem.html", viajantes=viajantes), 400

        try:
            clima = buscar_clima_destino(destino)
        except ValueError as erro:
            flash(str(erro), "erro")
            return render_template("nova_viagem.html", viajantes=viajantes), 404
        except Exception:
            flash("Falha ao consultar a Open-Meteo. Tente novamente.", "erro")
            return render_template("nova_viagem.html", viajantes=viajantes), 502

        viagem = Viagem.a_partir_de_dict(
            {
                "viajante_id": viajante.id,
                "destino": clima["destino"],
                "pais": clima.get("pais", ""),
                "latitude": clima["latitude"],
                "longitude": clima["longitude"],
                "data_consulta": clima["data_consulta"],
                "temperatura_c": clima["temperatura_c"],
                "vento_kmh": clima["vento_kmh"],
                "umidade": clima.get("umidade"),
                "codigo_clima": clima.get("codigo_clima"),
                "descricao_clima": clima.get("descricao_clima", ""),
            }
        )
        db.session.add(viagem)
        db.session.commit()
        return redirect(url_for("viagens.detalhe_viagem", viagem_id=viagem.id))

    return render_template("nova_viagem.html", viajantes=viajantes)


@viagens_bp.route("/viagens")
def lista_viagens():
    return render_template("lista_viagens.html", viagens=Viagem.listar())


@viagens_bp.route("/viagens/<int:viagem_id>")
def detalhe_viagem(viagem_id):
    viagem = db.session.get(Viagem, viagem_id)
    if not viagem:
        flash("Viagem não encontrada.", "erro")
        return redirect(url_for("viagens.lista_viagens"))

    hourly = []
    try:
        clima = buscar_clima_destino(viagem.destino)
        hourly = clima.get("hourly", [])
    except Exception:
        hourly = []

    return render_template("detalhe_viagem.html", viagem=viagem, hourly=hourly)
