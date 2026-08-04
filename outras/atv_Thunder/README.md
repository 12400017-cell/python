# Aula Extra — Thunder Client: API de Viagens & Clima

Projeto Flask com **camadas separadas** (Model, Service, Controller, View), banco SQLite e integração com a [Open-Meteo](https://open-meteo.com/).

## Objetivo

- Cadastrar **viajantes** (nome)
- Registrar uma **viagem** para um destino (ex.: Londres)
- Consultar o **clima atual** na Open-Meteo e **persistir** no banco
- Testar a API no **Thunder Client** (POST/GET JSON)

Exemplo de resumo gerado:

> Peter Parker Watson viajará para London, United Kingdom. Em 2026-08-03T19:45 a temperatura é 18.2°C (Nublado), vento 12.5 km/h, umidade 72%.

## Estrutura

```
Aula18Thunder/
├── models/                 ← Viajante + Viagem (SQLite)
├── services/               ← Open-Meteo (geocode + forecast)
├── controllers/
│   ├── viagens_controller.py   ← site HTML
│   └── api/viagens_api.py      ← REST JSON (Thunder Client)
├── views/
│   ├── templates/
│   └── static/css/
├── app.py
├── THUNDER_CLIENT.md
└── requirements.txt
```

## Como rodar

```powershell
cd flask/Aula18Thunder
pip install -r requirements.txt
python app.py
```

Abra: http://127.0.0.1:5000

## Fluxo

1. Cadastre o viajante (`POST /api/viajantes` ou formulário web)
2. Crie a viagem com o destino (`POST /api/viagens`)
3. A API geocodifica a cidade → busca clima na Open-Meteo → grava no SQLite
4. Resposta JSON traz temperatura, vento, umidade e o `resumo` em português

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/viajantes` | Lista viajantes |
| POST | `/api/viajantes` | Cadastra viajante `{ "nome": "..." }` |
| GET | `/api/viajantes/<id>` | Detalhe + viagens |
| DELETE | `/api/viajantes/<id>` | Remove viajante |
| GET | `/api/clima/<destino>` | Clima ao vivo (sem gravar) |
| GET | `/api/viagens` | Lista viagens salvas |
| POST | `/api/viagens` | Cria viagem + consulta clima |
| GET | `/api/viagens/<id>` | Detalhe da viagem |
| DELETE | `/api/viagens/<id>` | Remove viagem |

### POST viagem (Thunder Client)

```json
POST /api/viagens
Content-Type: application/json

{
  "nome": "Peter Parker Watson",
  "destino": "Londres"
}
```

Ou, se o viajante já existe:

```json
{
  "viajante_id": 1,
  "destino": "Londres"
}
```

## Open-Meteo usada

Geocoding:

```
https://geocoding-api.open-meteo.com/v1/search?name=Londres&count=1
```

Forecast (como no exemplo da aula):

```
https://api.open-meteo.com/v1/forecast?latitude=...&longitude=...&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m
```

Roteiro passo a passo: [THUNDER_CLIENT.md](THUNDER_CLIENT.md)
