# ATIVIDADE — Model inseguro. Arrume senha, papel no cadastro e o que vai no JSON.

from . import db
from .base import ModeloBase

PAPEIS = ("admin", "piloto", "visitante")


class Usuario(ModeloBase):
    """Usuario da torre. A segurança deste model está quebrada — corrija."""

    __tablename__ = "usuarios"

    username = db.Column(db.String(40), nullable=False, unique=True)
    nome = db.Column(db.String(120), nullable=False)
    # TODO(segurança): senha em texto puro. Use hash (werkzeug generate_password_hash).
    senha = db.Column(db.String(255), nullable=False)
    papel = db.Column(db.String(20), nullable=False, default="visitante")

    def definir_senha(self, senha: str) -> None:
        # TODO(segurança): não grave a senha crua.
        self.senha = senha

    def senha_confere(self, senha: str) -> bool:
        # TODO(segurança): comparar com hash (check_password_hash), não == .
        return self.senha == senha

    @classmethod
    def buscar_por_username(cls, username: str):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.username).all()

    @classmethod
    def a_partir_de_dict(cls, dados: dict):
        try:
            username = str(dados["username"]).strip().lower()
            nome = str(dados.get("nome") or username).strip()
            senha = str(dados["senha"])
            # TODO(segurança): o cliente NÃO pode escolher papel=admin.
            papel = str(dados.get("papel") or "visitante")
        except (KeyError, TypeError) as erro:
            raise ValueError("Campos obrigatórios: username e senha") from erro

        if cls.buscar_por_username(username):
            raise ValueError("username já cadastrado")

        usuario = cls(username=username, nome=nome, papel=papel)
        usuario.definir_senha(senha)
        return usuario

    def para_dict(self) -> dict:
        # TODO(segurança): NUNCA devolva a senha no JSON.
        return {
            "id": self.id,
            "username": self.username,
            "nome": self.nome,
            "papel": self.papel,
            "senha": self.senha,
            "data_criacao": str(self.data_criacao),
        }
