# Gabarito do professor — Atividade Aula 20

A solução completa é a pasta pai: `flask/Aula20seguranca/` (fora de `Atividade/`).

| Furo na Atividade | Onde o aluno arruma | Como fica na aula resolvida |
|-------------------|---------------------|-----------------------------|
| Senha em texto + JSON | `models/usuario.py` | `senha_hash` + werkzeug; `para_dict` sem senha |
| Cadastro escolhe papel | `a_partir_de_dict` | sempre `papel="visitante"` |
| Login sem senha | `services/auth.py` `autenticar` | `senha_confere` |
| JWT_SECRET `123`, 365 dias, query string | `app.py` | secret forte, 15 min / 1 dia, `["headers"]` |
| Sem `@jwt_required` | `controllers/auth_api.py` e `torre_api.py` | ver decorators da aula |
| Claims vazios | `jwt_config.py` `additional_claims_loader` | `papel` + `nome` |
| Admin sem checagem | `_exige_admin` | `get_jwt()["papel"] != "admin"` → 403 |
| Logout fake | `revogar_jwt_atual` + blocklist loader | grava `jti` / `TokenRevogado.esta_revogado` |
| Refresh fresh | `renovar_access` | `fresh=False` |
| Senha sem conferir atual | `trocar_senha` | confere `senha_atual` + rota `fresh=True` |

Não entregue este arquivo para a turma se quiser que eles sofram um pouco.
