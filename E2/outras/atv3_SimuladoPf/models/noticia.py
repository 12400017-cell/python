# Cada linha = uma notícia capturada naquela coleta.

from . import db
from .base import ModeloBase


class Noticia(ModeloBase):
    """Notícia individual ligada a uma ColetaNoticia."""

    __bind_key__ = "historico"
    __tablename__ = "noticias"

    coleta_id = db.Column(
        db.Integer,
        db.ForeignKey("coletas_noticia.id"),
        nullable=False,
    )
    titulo = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(500), nullable=False)
    secao = db.Column(db.String(80))

    coleta = db.relationship("ColetaNoticia", back_populates="noticias")

    def para_dict(self) -> dict:
        """Serializa a notícia para dict/JSON."""
        return {
            "id": self.id,
            "coleta_id": self.coleta_id,
            "titulo": self.titulo,
            "url": self.url,
            "secao": self.secao,
            "data_criacao": str(self.data_criacao),
            "data_atualizacao": str(self.data_atualizacao),
        }
