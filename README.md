# 📋 API de Tarefas

Projeto desenvolvido para a disciplina de **DevOps** (PUCPR), com o objetivo de praticar um fluxo completo de **CI/CD**: repositório no GitHub, branches, pull requests, code review e integração contínua com **GitHub Actions**.

## 🚀 Sobre o projeto

API REST para gerenciamento de tarefas (to-do list) construída com **Python + FastAPI**, com:

- ✅ CRUD completo de tarefas (criar, listar, buscar, atualizar e remover)
- ✅ Filtro de tarefas por status (concluídas/pendentes)
- ✅ Validação automática de dados com Pydantic
- ✅ Documentação interativa gerada pelo FastAPI (Swagger UI)
- ✅ 16 testes automatizados com pytest
- ✅ Integração contínua: os testes rodam automaticamente a cada push e pull request

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| [Python 3.12](https://www.python.org/) | Linguagem principal |
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web da API |
| [Pydantic](https://docs.pydantic.dev/) | Modelos e validação de dados |
| [pytest](https://pytest.org/) | Testes automatizados |
| [GitHub Actions](https://github.com/features/actions) | Integração contínua (CI) |

## 📦 Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/SEU-USUARIO/todo-api.git
cd todo-api

# 2. Crie e ative um ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a API
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000` e a **documentação interativa** em `http://127.0.0.1:8000/docs`.

## 🧪 Como rodar os testes

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -v
```

## 📚 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Mensagem de boas-vindas |
| `GET` | `/tarefas` | Lista todas as tarefas (filtro opcional `?concluida=true\|false`) |
| `POST` | `/tarefas` | Cria uma nova tarefa |
| `GET` | `/tarefas/{id}` | Busca uma tarefa pelo id |
| `PUT` | `/tarefas/{id}` | Atualiza os campos informados de uma tarefa |
| `DELETE` | `/tarefas/{id}` | Remove uma tarefa |

### Exemplo de requisição

```bash
curl -X POST http://127.0.0.1:8000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Estudar DevOps", "descricao": "Revisar CI/CD", "prioridade": 3}'
```

### Exemplo de resposta

```json
{
  "titulo": "Estudar DevOps",
  "descricao": "Revisar CI/CD",
  "prioridade": 3,
  "id": 1,
  "concluida": false,
  "criada_em": "2026-09-14T21:30:00.000000Z"
}
```

## 🔄 Fluxo de CI/CD

O workflow de integração contínua (`.github/workflows/ci.yml`) roda automaticamente em:

- todo **push** para a branch `main`
- todo **pull request** aberto para a `main`

Em cada execução, o GitHub Actions instala as dependências em um ambiente limpo com Python 3.12 e roda a suíte completa de testes com `pytest -v`. Assim, nenhum código que quebre a API chega à branch principal sem ser detectado.

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
