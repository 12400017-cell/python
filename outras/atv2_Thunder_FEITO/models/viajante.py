from . import db
from .base import ModeloBase


class Viajante(ModeloBase):
    __tablename__ = "viajantes"

    nome = db.Column(db.String(120), nullable=False, unique=True)

    viagens = db.relationship(
        "Viagem",
        back_populates="viajante",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.nome).all()

    @classmethod
    def a_partir_de_dict(cls, dados):
        try:
            nome = str(dados["nome"]).strip()
        except (KeyError, TypeError) as erro:
            raise ValueError("Campo obrigatório: nome") from erro

        if not nome:
            raise ValueError("Nome não pode ser vazio")

        return cls(nome=nome)

    def para_dict(self, com_viagens=False):
        dados = {
            "id": self.id,
            "nome": self.nome,
            "data_criacao": str(self.data_criacao),
        }
        if com_viagens:
            from .viagem import Viagem

            lista = self.viagens.order_by(Viagem.id.desc()).all()
            dados["viagens"] = [v.para_dict() for v in lista]
        else:
            dados["total_viagens"] = self.viagens.count()
        return dados
