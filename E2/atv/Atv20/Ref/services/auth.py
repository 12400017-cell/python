# Regras de autenticação: hash, emitir tokens, logout (blocklist) e seed.

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
    """
    Access token (curto, opcionalmente fresh) + refresh token (longo).
    identity=usuario → user_identity_loader grava o id no claim "sub".
    """
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
    """Valida usuário/senha. Erro de credencial → ValueError (401 na API)."""
    usuario = Usuario.buscar_por_username((username or "").strip().lower())
    if not usuario or not usuario.senha_confere(senha or ""):
        raise ValueError("username ou senha incorretos")
    return usuario


def registrar(dados: dict) -> Usuario:
    """Cadastra visitante, grava no principal.db e devolve o model."""
    usuario = Usuario.a_partir_de_dict(dados)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def renovar_access(usuario: Usuario) -> dict:
    """
    Explicit Refreshing: gera um access novo, NÃO fresh.
    Operações @jwt_required(fresh=True) ainda exigem login de verdade.
    """
    access_token = create_access_token(identity=usuario, fresh=False)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "fresh": False,
        "usuario": usuario.para_dict(),
    }


def revogar_jwt_atual() -> dict:
    """
    Coloca o jti do token da requisição na blocklist (access OU refresh).
    A rota usa @jwt_required(verify_type=False) — um endpoint para os dois.
    """
    payload = get_jwt()
    usuario = get_current_user()
    registro = TokenRevogado(
        jti=payload["jti"],
        tipo=payload["type"],
        usuario_id=usuario.id if usuario else None,
    )
    db.session.add(registro)
    db.session.commit()
    tipo = payload["type"]
    return {
        "mensagem": f"{tipo.capitalize()} token revogado",
        "jti": payload["jti"],
        "tipo": tipo,
    }


def trocar_senha(usuario: Usuario, senha_atual: str, senha_nova: str) -> None:
    """Troca de senha (rota com fresh=True). Confere a senha atual antes."""
    if not usuario.senha_confere(senha_atual or ""):
        raise ValueError("senha atual incorreta")
    if not senha_nova or len(senha_nova) < 6:
        raise ValueError("senha nova deve ter pelo menos 6 caracteres")
    usuario.definir_senha(senha_nova)
    db.session.commit()


def popular_usuarios() -> None:
    """Seed da aula: admin, piloto e visitante (só se a tabela estiver vazia)."""
    if Usuario.query.count() > 0:
        return
    for username, nome, senha, papel in USUARIOS_DEMO:
        usuario = Usuario(username=username, nome=nome, papel=papel)
        usuario.definir_senha(senha)
        db.session.add(usuario)
    db.session.commit()
