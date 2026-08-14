from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .coleta_noticia import ColetaNoticia
from .noticia import Noticia

__all__ = ["db", "ColetaNoticia", "Noticia","ModeloBase" ]
