# Quem entra na torre: login, senha com hash e papel (claim extra no JWT).
# Vive no banco principal.db (bind padrão).

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .base import ModeloBase

PAPEIS = ("admin", "piloto", "visitante")


class Usuario(ModeloBase):
    """Model de um usuário autenticável (identity do Flask-JWT-Extended)."""

    __tablename__ = "usuarios"

    username = db.Column(db.String(40), nullable=False, unique=True)
    nome = db.Column(db.String(120), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    papel = db.Column(db.String(20), nullable=False, default="visitante")

    def definir_senha(self, senha: str) -> None:
        """Grava o hash da senha (nunca armazene a senha em texto puro)."""
        self.senha_hash = generate_password_hash(senha)

    def senha_confere(self, senha: str) -> bool:
        """Compara a senha digitada com o hash salvo."""
        return check_password_hash(self.senha_hash, senha)

    @classmethod
    def buscar_por_username(cls, username: str):
        """Localiza um usuário pelo login (ou None)."""
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def listar(cls):
        """Lista usuários sem expor o hash da senha."""
        return cls.query.order_by(cls.username).all()

    @classmethod
    def a_partir_de_dict(cls, dados: dict):
        """
        Monta um Usuario a partir de JSON/form.
        Papel sempre começa como visitante — ninguém se promove sozinho.
        """
        try:
            username = str(dados["username"]).strip().lower()
            nome = str(dados.get("nome") or username).strip()
            senha = str(dados["senha"])
        except (KeyError, TypeError) as erro:
            raise ValueError("Campos obrigatórios: username e senha") from erro

        if len(username) < 3 or len(username) > 40 or " " in username:
            raise ValueError("username deve ter 3 a 40 caracteres, sem espaços")
        if len(senha) < 6:
            raise ValueError("senha deve ter pelo menos 6 caracteres")
        if not nome:
            raise ValueError("nome não pode ser vazio")
        if cls.buscar_por_username(username):
            raise ValueError("username já cadastrado")

        usuario = cls(username=username, nome=nome, papel="visitante")
        usuario.definir_senha(senha)
        return usuario

    def para_dict(self) -> dict:
        """Serializa o usuário para JSON (sem senha_hash)."""
        return {
            "id": self.id,
            "username": self.username,
            "nome": self.nome,
            "papel": self.papel,
            "data_criacao": str(self.data_criacao),
        }
