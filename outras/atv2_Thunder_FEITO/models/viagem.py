from . import db
from .base import ModeloBase


class Viagem(ModeloBase):
    __tablename__ = "viagens"

    viajante_id = db.Column(db.Integer, db.ForeignKey("viajantes.id"), nullable=False)
    destino = db.Column(db.String(120), nullable=False)
    pais = db.Column(db.String(80), default="")
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    data_consulta = db.Column(db.String(30), nullable=False)
    temperatura_c = db.Column(db.Float, nullable=False)
    vento_kmh = db.Column(db.Float, nullable=False)
    umidade = db.Column(db.Integer, nullable=True)
    codigo_clima = db.Column(db.Integer, nullable=True)
    descricao_clima = db.Column(db.String(80), default="")

    viajante = db.relationship("Viajante", back_populates="viagens")

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.id.desc()).all()

    @classmethod
    def a_partir_de_dict(cls, dados):
        obrigatorios = (
            "viajante_id",
            "destino",
            "latitude",
            "longitude",
            "data_consulta",
            "temperatura_c",
            "vento_kmh",
        )
        try:
            return cls(
                viajante_id=int(dados["viajante_id"]),
                destino=str(dados["destino"]).strip(),
                pais=str(dados.get("pais", "")).strip(),
                latitude=float(dados["latitude"]),
                longitude=float(dados["longitude"]),
                data_consulta=str(dados["data_consulta"]).strip(),
                temperatura_c=float(dados["temperatura_c"]),
                vento_kmh=float(dados["vento_kmh"]),
                umidade=dados.get("umidade"),
                codigo_clima=dados.get("codigo_clima"),
                descricao_clima=str(dados.get("descricao_clima", "")).strip(),
            )
        except (KeyError, ValueError, TypeError) as erro:
            campos = ", ".join(obrigatorios)
            raise ValueError(f"Campos obrigatórios: {campos}") from erro

    def resumo(self):
        nome = self.viajante.nome if self.viajante else "?"
        return (
            f"{nome} viajará para {self.destino}"
            f"{', ' + self.pais if self.pais else ''}. "
            f"Em {self.data_consulta} a temperatura é {self.temperatura_c}°C "
            f"({self.descricao_clima or 'clima atual'}), "
            f"vento {self.vento_kmh} km/h"
            + (f", umidade {self.umidade}%" if self.umidade is not None else "")
            + "."
        )

    def para_dict(self):
        return {
            "id": self.id,
            "viajante_id": self.viajante_id,
            "viajante": self.viajante.nome if self.viajante else None,
            "destino": self.destino,
            "pais": self.pais,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "data_consulta": self.data_consulta,
            "temperatura_c": self.temperatura_c,
            "vento_kmh": self.vento_kmh,
            "umidade": self.umidade,
            "codigo_clima": self.codigo_clima,
            "descricao_clima": self.descricao_clima,
            "resumo": self.resumo(),
            "data_criacao": str(self.data_criacao),
        }
