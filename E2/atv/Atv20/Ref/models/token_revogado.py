# JWT Revoking / Blocklist (docs): jti de tokens inválidos após logout.
# Vive no segundo banco SQLite (bind seguranca) — ver app.py.

from . import db
from .base import ModeloBase


class TokenRevogado(ModeloBase):
    """
    Um JWT revogado (access ou refresh).
    O callback token_in_blocklist_loader consulta esta tabela pelo jti.
    """

    __bind_key__ = "seguranca"
    __tablename__ = "tokens_revogados"

    # jti = JWT ID — identificador único do token (docs: index para busca rápida).
    jti = db.Column(db.String(36), nullable=False, index=True)
    tipo = db.Column(db.String(16), nullable=False)
    # Sem ForeignKey: Usuario está em outro arquivo .db (bind diferente).
    usuario_id = db.Column(db.Integer, nullable=True)

    @classmethod
    def esta_revogado(cls, jti: str) -> bool:
        """True se o jti já foi colocado na blocklist (query no bind seguranca)."""
        return cls.query.filter_by(jti=jti).first() is not None

    @classmethod
    def listar(cls):
        """Lista tokens revogados, do mais recente ao mais antigo."""
        return cls.query.order_by(cls.data_criacao.desc()).all()

    def para_dict(self) -> dict:
        """Serializa o registro da blocklist para JSON."""
        return {
            "id": self.id,
            "jti": self.jti,
            "tipo": self.tipo,
            "usuario_id": self.usuario_id,
            "data_criacao": str(self.data_criacao),
        }
