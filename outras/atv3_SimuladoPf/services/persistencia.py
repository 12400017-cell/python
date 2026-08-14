# Grava no banco o resultado de buscar_noticias.

from models import ColetaNoticia, Noticia, db
from services.raspador import ResultadoBusca


def persistir_coleta(dados: ResultadoBusca) -> ColetaNoticia:
    """Cria ColetaNoticia + Noticia no SQLite historico_noticias.db."""
    coleta = ColetaNoticia(
        fonte=dados["fonte"],
        modo_busca=dados["modo_busca"],
        total=dados["total"],
    )

    for item in dados["noticias"]:
        coleta.noticias.append(
            Noticia(
                titulo=item["titulo"],
                url=item["url"],
                secao=item["secao"],
            )
        )

    db.session.add(coleta)
    db.session.commit()
    return coleta
