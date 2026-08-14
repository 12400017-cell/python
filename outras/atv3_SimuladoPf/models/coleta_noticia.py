# Uma "foto" de cada scraping das notícias (economia.uol.com.br).

from . import db
from .base import ModeloBase


class ColetaNoticia(ModeloBase):
    """Cabeçalho de uma sincronização salva no histórico."""

    __bind_key__ = "historico"
    __tablename__ = "coletas_noticia"

    fonte = db.Column(db.String(255), nullable=False)
    modo_busca = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Integer, nullable=False, default=0)

    noticias = db.relationship(
        "Noticia",
        back_populates="coleta",
        cascade="all, delete-orphan",
    )

    @classmethod
    def listar(cls):
        """Lista coletas da mais recente para a mais antiga."""
        return cls.query.order_by(cls.data_criacao.desc()).all()

    def para_dict(self, incluir_noticias: bool = False) -> dict:
        """Serializa a coleta para dict/JSON."""
        dados = {
            "id": self.id,
            "fonte": self.fonte,
            "modo_busca": self.modo_busca,
            "total": self.total,
            "data_criacao": str(self.data_criacao),
            "data_atualizacao": str(self.data_atualizacao),
        }
        if incluir_noticias:
            dados["noticias"] = [n.para_dict() for n in self.noticias]
        return dados
