import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

CODIGOS_CLIMA = {
    0: "Céu limpo",
    1: "Principalmente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Neblina",
    48: "Neblina com geada",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa intensa",
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte",
    71: "Neve fraca",
    73: "Neve moderada",
    75: "Neve forte",
    80: "Pancadas de chuva",
    81: "Pancadas moderadas",
    82: "Pancadas fortes",
    95: "Tempestade",
    96: "Tempestade com granizo",
    99: "Tempestade forte com granizo",
}


def _descricao(codigo):
    if codigo is None:
        return ""
    return CODIGOS_CLIMA.get(int(codigo), f"Código {codigo}")


def geocodificar_cidade(destino):
    """Busca latitude/longitude do destino no geocoding da Open-Meteo."""
    nome = str(destino or "").strip()
    if not nome:
        raise ValueError("Destino não pode ser vazio")

    resposta = requests.get(
        GEOCODE_URL,
        params={
            "name": nome,
            "count": 1,
            "language": "pt",
            "format": "json",
        },
        timeout=10,
    )
    resposta.raise_for_status()
    resultados = resposta.json().get("results") or []

    if not resultados:
        raise ValueError(f"Destino '{nome}' não encontrado")

    local = resultados[0]
    return {
        "destino": local.get("name", nome),
        "pais": local.get("country", ""),
        "admin1": local.get("admin1", ""),
        "latitude": float(local["latitude"]),
        "longitude": float(local["longitude"]),
        "timezone": local.get("timezone", "auto"),
    }


def buscar_clima(latitude, longitude, timezone="auto"):
    """Consulta o clima atual na Open-Meteo."""
    resposta = requests.get(
        FORECAST_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code",
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": timezone or "auto",
            "forecast_days": 1,
        },
        timeout=10,
    )
    resposta.raise_for_status()
    dados = resposta.json()
    atual = dados.get("current") or {}
    codigo = atual.get("weather_code")

    horarios = dados.get("hourly") or {}
    horas = []
    tempos = horarios.get("time") or []
    temps = horarios.get("temperature_2m") or []
    umidades = horarios.get("relative_humidity_2m") or []
    ventos = horarios.get("wind_speed_10m") or []
    for i, hora in enumerate(tempos):
        horas.append(
            {
                "hora": hora,
                "temperatura_c": temps[i] if i < len(temps) else None,
                "umidade": umidades[i] if i < len(umidades) else None,
                "vento_kmh": ventos[i] if i < len(ventos) else None,
            }
        )

    return {
        "data_consulta": atual.get("time", ""),
        "temperatura_c": atual.get("temperature_2m"),
        "vento_kmh": atual.get("wind_speed_10m"),
        "umidade": atual.get("relative_humidity_2m"),
        "codigo_clima": codigo,
        "descricao_clima": _descricao(codigo),
        "timezone": dados.get("timezone", timezone),
        "hourly": horas,
        "fonte": "Open-Meteo",
    }


def buscar_clima_destino(destino):
    """Geocodifica o destino e retorna endereço + clima atual."""
    local = geocodificar_cidade(destino)
    clima = buscar_clima(local["latitude"], local["longitude"], local.get("timezone"))
    return {**local, **clima}
