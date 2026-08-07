from flask import Blueprint, jsonify, request

from models import Viajante, Viagem, db
from services import buscar_clima_destino

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/viajantes", methods=["GET"])
def listar_viajantes():
    return jsonify([v.para_dict() for v in Viajante.listar()])


@api_bp.route("/viajantes/<int:viajante_id>", methods=["GET"])
def detalhe_viajante(viajante_id):
    viajante = db.session.get(Viajante, viajante_id)
    if not viajante:
        return jsonify({"erro": "Viajante não encontrado"}), 404
    return jsonify(viajante.para_dict(com_viagens=True))


@api_bp.route("/viajantes", methods=["POST"])
def criar_viajante():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body (Content-Type: application/json)"}), 400

    try:
        viajante = Viajante.a_partir_de_dict(dados)
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    if Viajante.query.filter_by(nome=viajante.nome).first():
        return jsonify({"erro": f"Viajante '{viajante.nome}' já cadastrado"}), 409

    db.session.add(viajante)
    db.session.commit()
    return jsonify(viajante.para_dict()), 201


@api_bp.route("/viajantes/<int:viajante_id>", methods=["DELETE"])
def excluir_viajante(viajante_id):
    viajante = db.session.get(Viajante, viajante_id)
    if not viajante:
        return jsonify({"erro": "Viajante não encontrado"}), 404

    db.session.delete(viajante)
    db.session.commit()
    return "", 204


@api_bp.route("/clima/<path:destino>", methods=["GET"])
def consultar_clima(destino):
    try:
        return jsonify(buscar_clima_destino(destino))
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404
    except Exception as erro:
        return jsonify({"erro": f"Falha ao consultar clima: {erro}"}), 502


@api_bp.route("/viagens", methods=["GET"])
def listar_viagens():
    return jsonify([v.para_dict() for v in Viagem.listar()])


@api_bp.route("/viagens/<int:viagem_id>", methods=["GET"])
def detalhe_viagem(viagem_id):
    viagem = db.session.get(Viagem, viagem_id)
    if not viagem:
        return jsonify({"erro": "Viagem não encontrada"}), 404
    return jsonify(viagem.para_dict())


@api_bp.route("/viagens", methods=["POST"])
def criar_viagem():
    """
    Body JSON:
    {
      "viajante_id": 1,          # ou "nome": "Peter Parker Watson"
      "destino": "Londres"
    }
    Busca o clima na Open-Meteo e grava a viagem no SQLite.
    """
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body (Content-Type: application/json)"}), 400

    destino = str(dados.get("destino", "")).strip()
    if not destino:
        return jsonify({"erro": "Campo obrigatório: destino"}), 400

    viajante = None
    if dados.get("viajante_id") is not None:
        viajante = db.session.get(Viajante, int(dados["viajante_id"]))
    elif dados.get("nome"):
        nome = str(dados["nome"]).strip()
        viajante = Viajante.query.filter_by(nome=nome).first()
        if not viajante:
            viajante = Viajante(nome=nome)
            db.session.add(viajante)
            db.session.flush()

    if not viajante:
        return jsonify({"erro": "Informe viajante_id ou nome"}), 400

    try:
        clima = buscar_clima_destino(destino)
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404
    except Exception as erro:
        return jsonify({"erro": f"Falha ao consultar clima: {erro}"}), 502

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

    resposta = viagem.para_dict()
    resposta["hourly"] = clima.get("hourly", [])
    return jsonify(resposta), 201


@api_bp.route("/viagens/<int:viagem_id>", methods=["DELETE"])
def excluir_viagem(viagem_id):
    viagem = db.session.get(Viagem, viagem_id)
    if not viagem:
        return jsonify({"erro": "Viagem não encontrada"}), 404

    db.session.delete(viagem)
    db.session.commit()
    return "", 204
