from flask_sqlalchemy import SQLAlchemy

# Um único objeto db; Usuario fica no bind padrão e TokenRevogado no bind "seguranca".
db = SQLAlchemy()

from .base import ModeloBase
from .usuario import Usuario
from .token_revogado import TokenRevogado

__all__ = ["db", "ModeloBase", "Usuario", "TokenRevogado"]
