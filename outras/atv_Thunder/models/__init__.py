from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .viajante import Viajante
from .viagem import Viagem

__all__ = ["db", "ModeloBase", "Viajante", "Viagem"]
