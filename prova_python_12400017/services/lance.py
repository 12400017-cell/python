# Service de webscraping — notícias de futebol no Lance.com.br (HTML + BeautifulSoup).
# Modelo: Aula 19 (flightaware.py) — requests → BeautifulSoup → lista estruturada.

from __future__ import annotations

from typing import TypedDict
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

URL_LANCE: str = "https://www.lance.com.br/"
TIMEOUT: int = 20
USER_AGENT: str = "Mozilla/5.0 (compatible; TecTI-ProvaA/1.0; +aula-educacional)"

MODOS_VALIDOS: frozenset[str] = frozenset({"futebol", "todos"})

# Seções da home que NÃO são futebol (usadas no filtro modo=futebol).
SECOES_EXCLUIDAS: frozenset[str] = frozenset(
    {
        "tenis",
        "lutas",
        "sites-de-apostas",
        "mais-esportes",
        "nba",
        "basquete",
        "volei",
        "formula-1",
        "automobilismo",
        "olimpiadas",
        "rio-2016-10-anos",
        "e-sports",
        "esports",
    }
)

# Palavras que reforçam classificação como futebol (título ou URL).
PALAVRAS_FUTEBOL: tuple[str, ...] = (
    "futebol",
    "brasileirao",
    "brasileirão",
    "libertadores",
    "copa",
    "gol",
    "time",
    "clube",
    "selecao",
    "seleção",
    "flamengo",
    "corinthians",
    "palmeiras",
    "sao-paulo",
    "são-paulo",
    "santos",
    "vasco",
    "botafogo",
    "fluminense",
    "gremio",
    "grêmio",
    "internacional",
    "atletico",
    "atlético",
    "cruzeiro",
    "bahia",
    "fortaleza",
    "champions",
    "premier",
    "la-liga",
    "serie-a",
    "série-a",
)


class NoticiaItem(TypedDict):
    """Uma notícia extraída do HTML."""

    titulo: str
    url: str
    secao: str | None


class ResultadoBusca(TypedDict):
    """Pacote devolvido pelo scraping."""

    fonte: str
    modo_busca: str
    total: int
    noticias: list[NoticiaItem]


def _secao_da_url(url: str) -> str | None:
    """Extrai o primeiro segmento do path (ex.: /flamengo/... → flamengo)."""
    path = urlparse(url).path
    partes = [p for p in path.split("/") if p]
    return partes[0] if partes else None


def _parece_noticia(url: str, titulo: str) -> bool:
    """Heurística: link interno do Lance com título longo e página .html."""
    if "lance.com.br" not in url:
        return False
    if len(titulo.strip()) < 20:
        return False
    if ".html" not in url.lower():
        return False
    # Evita links de utilidade / área logada genéricos.
    bloqueados = ("/tag/", "/autor/", "/busca", "/login", "/assine")
    return not any(b in url.lower() for b in bloqueados)


def _eh_futebol(url: str, titulo: str, secao: str | None) -> bool:
    """
    Decide se a matéria é de futebol.
    Exclui seções claramente de outros esportes; aceita clubes / futebol-* /
    ou títulos/URLs com palavras típicas.
    """
    secao_l = (secao or "").lower()
    if secao_l in SECOES_EXCLUIDAS:
        return False

    texto = f"{secao_l} {titulo} {url}".lower()
    if secao_l.startswith("futebol"):
        return True
    if secao_l in {
        "fora-de-campo",
        "onde-assistir",
        "lance-negocios",
        "mercado-da-bola",
    }:
        return True
    return any(p in texto for p in PALAVRAS_FUTEBOL)


def buscar_noticias(modo: str = "futebol") -> ResultadoBusca:
    """
    Função principal do scraping:
    1) baixa a home do Lance
    2) percorre os links com BeautifulSoup
    3) devolve notícias (modo=futebol filtra só futebol; modo=todos traz .html da home)
    """
    modo_n = (modo or "futebol").strip().lower()
    if modo_n not in MODOS_VALIDOS:
        raise ValueError("Parâmetro modo deve ser 'futebol' ou 'todos'.")

    try:
        resposta = requests.get(
            URL_LANCE,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )
        resposta.raise_for_status()
    except requests.RequestException as erro:
        raise ConnectionError(f"Não foi possível acessar o Lance: {erro}") from erro

    resposta.encoding = resposta.apparent_encoding or "utf-8"
    soup = BeautifulSoup(resposta.text, "html.parser")

    vistos: set[tuple[str, str]] = set()
    noticias: list[NoticiaItem] = []

    for tag in soup.find_all("a", href=True):
        titulo = tag.get_text(" ", strip=True)
        url = urljoin(URL_LANCE, tag["href"]).split("#")[0].split("?")[0]
        if not _parece_noticia(url, titulo):
            continue

        secao = _secao_da_url(url)
        if modo_n == "futebol" and not _eh_futebol(url, titulo, secao):
            continue

        chave = (titulo[:200], url)
        if chave in vistos:
            continue
        vistos.add(chave)

        noticias.append(
            NoticiaItem(
                titulo=titulo,
                url=url,
                secao=secao,
            )
        )

    return ResultadoBusca(
        fonte=URL_LANCE,
        modo_busca=modo_n,
        total=len(noticias),
        noticias=noticias,
    )
