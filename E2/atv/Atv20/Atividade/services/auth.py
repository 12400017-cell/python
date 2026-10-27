# ATIVIDADE — regras de auth quebradas. Arrume senha, fresh, blocklist.

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt,
)

from models import TokenRevogado, Usuario, db

USUARIOS_DEMO = [
    ("admin", "Admin da Torre", "admin123", "admin"),
    ("piloto", "Piloto da Sala", "piloto123", "piloto"),
    ("visitante", "Visitante do Hangar", "visitante123", "visitante"),
]


def emitir_tokens(usuario: Usuario, fresh: bool = True) -> dict:
    access_token = create_access_token(identity=usuario, fresh=fresh)
    refresh_token = create_refresh_token(identity=usuario)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "fresh": fresh,
        "usuario": usuario.para_dict(),
    }


def autenticar(username: str, senha: str) -> Usuario:
    # TODO(segurança): hoje entra SÓ com o username, sem conferir a senha.
    usuario = Usuario.buscar_por_username((username or "").strip().lower())
    if not usuario:
        raise ValueError("username ou senha incorretos")
    return usuario


def registrar(dados: dict) -> Usuario:
    usuario = Usuario.a_partir_de_dict(dados)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def renovar_access(usuario: Usuario) -> dict:
    # TODO(segurança): refresh NÃO pode gerar token fresh. Use fresh=False.
    access_token = create_access_token(identity=usuario, fresh=True)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "fresh": True,
        "usuario": usuario.para_dict(),
    }


def revogar_jwt_atual() -> dict:
    # TODO(segurança): logout de mentira — não grava o jti na blocklist.
    payload = get_jwt()
    return {
        "mensagem": "Logout fake: o token continua válido",
        "jti": payload.get("jti"),
        "tipo": payload.get("type"),
    }


def trocar_senha(usuario: Usuario, senha_atual: str, senha_nova: str) -> None:
    # TODO(segurança): troca a senha SEM conferir a senha atual.
    usuario.definir_senha(senha_nova or "123")
    db.session.commit()


def popular_usuarios() -> None:
    if Usuario.query.count() > 0:
        return
    for username, nome, senha, papel in USUARIOS_DEMO:
        usuario = Usuario(username=username, nome=nome, papel=papel)
        usuario.definir_senha(senha)
        db.session.add(usuario)
    db.session.commit()
