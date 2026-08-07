import os

from flask import Flask

from controllers import api_bp, viagens_bp
from models import Viajante, db

DADOS_INICIAIS = [
    {"nome": "Peter Parker Watson"},
    {"nome": "Maria Souza"},
]


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "viagens.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "aula18-thunder-viagens-dev"

    db.init_app(app)
    app.register_blueprint(viagens_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()
        if Viajante.query.count() == 0:
            for dados in DADOS_INICIAIS:
                db.session.add(Viajante(**dados))
            db.session.commit()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
