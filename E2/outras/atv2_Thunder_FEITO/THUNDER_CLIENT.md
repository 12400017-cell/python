# Thunder Client — API de Viagens & Clima

Na versão gratuita o **Import** de coleção costuma não funcionar. Monte os requests na mão.

Objetivo: cadastrar um viajante e registrar uma viagem para um destino; a API busca o clima na Open-Meteo e grava no SQLite.

## Passo 1 — Subir a API

```powershell
cd flask/Aula18Thunder
pip install -r requirements.txt
python app.py
```

Deixe rodando em `http://127.0.0.1:5000`.

## Passo 2 — Abrir o Thunder Client

1. Extensão **Thunder Client** no VS Code / Cursor
2. Ícone do raio na barra lateral
3. **New Request**

## Passo 3 — Cadastrar viajante (POST)

| Campo | Valor |
|-------|--------|
| Método | `POST` |
| URL | `http://127.0.0.1:5000/api/viajantes` |

Headers:

- `Content-Type` = `application/json`

Body → JSON:

```json
{
  "nome": "Peter Parker Watson"
}
```

**Send** → status **201**. Anote o `id` retornado (ex.: `1` ou `3`).

> O app já vem com Peter Parker Watson e Maria Souza no banco. Se der **409**, use o `viajante_id` do GET abaixo.

## Passo 4 — Listar viajantes (GET)

| Campo | Valor |
|-------|--------|
| Método | `GET` |
| URL | `http://127.0.0.1:5000/api/viajantes` |

## Passo 5 — Testar clima sem gravar (GET)

| Campo | Valor |
|-------|--------|
| Método | `GET` |
| URL | `http://127.0.0.1:5000/api/clima/Londres` |

Resposta: cidade, país, latitude, longitude, temperatura, vento, umidade e previsão horária.

## Passo 6 — Criar viagem + clima (POST)

**New Request**

| Campo | Valor |
|-------|--------|
| Método | `POST` |
| URL | `http://127.0.0.1:5000/api/viagens` |

Header: `Content-Type` = `application/json`

Body:

```json
{
  "nome": "Peter Parker Watson",
  "destino": "Londres"
}
```

**Send** → **201**. A resposta traz o `resumo`, por exemplo:

```json
{
  "viajante": "Peter Parker Watson",
  "destino": "London",
  "pais": "United Kingdom",
  "data_consulta": "2026-08-03T19:45",
  "temperatura_c": 18.2,
  "vento_kmh": 12.5,
  "umidade": 72,
  "descricao_clima": "Nublado",
  "resumo": "Peter Parker Watson viajará para London, United Kingdom. Em 2026-08-03T19:45 a temperatura é 18.2°C (Nublado), vento 12.5 km/h, umidade 72%."
}
```

## Passo 7 — Conferir no banco (GET)

| Campo | Valor |
|-------|--------|
| Método | `GET` |
| URL | `http://127.0.0.1:5000/api/viagens` |

Ou no navegador: http://127.0.0.1:5000/viagens

## Fluxo do POST /api/viagens

```
Thunder Client
  POST { nome, destino }
        ↓
  /api/viagens
        ↓
  encontra ou cria Viajante
        ↓
  geocoding Open-Meteo (cidade → lat/lon)
        ↓
  forecast Open-Meteo (temperatura, vento, umidade)
        ↓
  Viagem → SQLite
        ↓
  jsonify 201 (resumo + clima)
```

## Requests opcionais

| Método | URL | Body |
|--------|-----|------|
| GET | `/api/viajantes/1` | — |
| GET | `/api/viagens/1` | — |
| POST | `/api/viagens` | `{ "viajante_id": 1, "destino": "Tóquio" }` |
| DELETE | `/api/viagens/1` | — |
| DELETE | `/api/viajantes/1` | — |

## Erros comuns

| Situação | Causa | Solução |
|----------|--------|---------|
| `400` — Envie JSON no body | Sem header ou body vazio | `Content-Type: application/json` |
| `404` — Destino não encontrado | Nome inválido | Use cidades reais: `Londres`, `Paris`, `São Paulo` |
| `409` — Viajante já cadastrado | Nome duplicado | Use GET e o `viajante_id` no POST viagem |
| Connection refused | App parado | `python app.py` |
| `502` — Falha ao consultar clima | Sem internet / API fora | Verifique a conexão |
