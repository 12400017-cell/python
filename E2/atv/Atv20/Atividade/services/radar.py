# "Radar" da torre: dados de voo de demonstração (Aula 19 sem scraping).
# Aqui o ponto da aula é o JWT, não a fonte externa.

VOOS_DEMO = [
    {
        "identificacao": "GLO1820",
        "status": "no ar",
        "rota": "SBGR → SBBR",
        "aeronave": "B737",
    },
    {
        "identificacao": "TAM3451",
        "status": "taxiando",
        "rota": "SBSP → SBCF",
        "aeronave": "A320",
    },
    {
        "identificacao": "AZU4122",
        "status": "pousou",
        "rota": "SBRJ → SBGR",
        "aeronave": "E195",
    },
    {
        "identificacao": "ONE9001",
        "status": "autorizado",
        "rota": "SBPA → SBGR",
        "aeronave": "A321",
    },
]


def listar_voos_radar() -> dict:
    """Devolve o painel da torre (protegido por JWT na API)."""
    return {
        "fonte": "demonstração da Aula 20 (sem scraping)",
        "total": len(VOOS_DEMO),
        "voos": list(VOOS_DEMO),
    }
