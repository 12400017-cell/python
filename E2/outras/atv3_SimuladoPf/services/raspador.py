# Service de webscraping genérico por palavras-chave (HTML + BeautifulSoup).
# Modelo: Aula 19 — requests → BeautifulSoup → lista estruturada.

from __future__ import annotations

import unicodedata
from typing import TypedDict
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

URL_FONTE: str = 'https://economia.uol.com.br/'
TIMEOUT: int = 20
USER_AGENT: str = "Mozilla/5.0 (compatible; TecTI-RaspaUol/1.0; +aula-educacional)"

MODOS_VALIDOS: frozenset[str] = frozenset({"palavra", "todos"})

PALAVRAS_CHAVE: tuple[str, ...] = ('economia', 'econômico', 'economico',)


class NoticiaItem(TypedDict):
    """Uma notícia / link extraído do HTML."""

    titulo: str
    url: str
    secao: str | None


class ResultadoBusca(TypedDict):
    """Pacote devolvido pelo scraping."""

    projeto: str
    fonte: str
    modo_busca: str
    palavras_chave: list[str]
    total: int
    noticias: list[NoticiaItem]


def _sem_acento(texto: str) -> str:
    """Remove acentos para comparação case/accent-insensitive."""
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _secao_da_url(url: str) -> str | None:
    """Extrai o primeiro segmento do path."""
    path = urlparse(url).path
    partes = [p for p in path.split("/") if p]
    return partes[0] if partes else None


def _parece_candidato(url: str, titulo: str) -> bool:
    """Heurística: link com título longo o bastante."""
    if len(titulo.strip()) < 15:
        return False
    if not url.startswith("http"):
        return False
    bloqueados = ("/tag/", "/autor/", "/busca", "/login", "/assine", "javascript:")
    return not any(b in url.lower() for b in bloqueados)


def _contem_palavra(titulo: str, url: str) -> bool:
    """True se título ou URL contém alguma palavra-chave."""
    texto = _sem_acento(f"{titulo} {url}").lower()
    for p in PALAVRAS_CHAVE:
        if _sem_acento(p).lower() in texto:
            return True
    return False


def buscar_noticias(modo: str = "palavra") -> ResultadoBusca:
    """
    Função principal do scraping (economia):
    1) baixa a página fonte
    2) percorre os <a href> com BeautifulSoup
    3) modo=palavra filtra por palavras-chave; modo=todos traz candidatos
    """
    modo_n = (modo or "palavra").strip().lower()
    if modo_n not in MODOS_VALIDOS:
        raise ValueError("Parâmetro modo deve ser 'palavra' ou 'todos'.")

    try:
        resposta = requests.get(
            URL_FONTE,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
        )
        resposta.raise_for_status()
    except requests.RequestException as erro:
        raise ConnectionError(f"Não foi possível acessar a fonte: {erro}") from erro

    resposta.encoding = resposta.apparent_encoding or "utf-8"
    soup = BeautifulSoup(resposta.text, "html.parser")

    vistos: set[tuple[str, str]] = set()
    noticias: list[NoticiaItem] = []

    for tag in soup.find_all("a", href=True):
        titulo = tag.get_text(" ", strip=True)
        url = urljoin(URL_FONTE, tag["href"]).split("#")[0].split("?")[0]
        if not _parece_candidato(url, titulo):
            continue

        if modo_n == "palavra" and not _contem_palavra(titulo, url):
            continue

        secao = _secao_da_url(url)
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
        projeto='RaspaUol',
        fonte=URL_FONTE,
        modo_busca=modo_n,
        palavras_chave=list(PALAVRAS_CHAVE),
        total=len(noticias),
        noticias=noticias,
    )
