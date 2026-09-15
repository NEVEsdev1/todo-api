# 📋 API de Tarefas

[![CI](https://github.com/NEVEsdev1/todo-api/actions/workflows/ci.yml/badge.svg)](https://github.com/NEVEsdev1/todo-api/actions/workflows/ci.yml)
[![CD](https://github.com/NEVEsdev1/todo-api/actions/workflows/cd.yml/badge.svg)](https://github.com/NEVEsdev1/todo-api/actions/workflows/cd.yml)

Projeto desenvolvido para a disciplina de **DevOps** (PUCPR), com o objetivo de praticar um fluxo completo de **CI/CD**: repositório no GitHub, branches, pull requests, code review e integração contínua com **GitHub Actions**.

## 🚀 Sobre o projeto

API REST para gerenciamento de tarefas (to-do list) construída com **Python + FastAPI**, com:

- ✅ CRUD completo de tarefas (criar, listar, buscar, atualizar e remover)
- ✅ Filtro de tarefas por status (concluídas/pendentes)
- ✅ Validação automática de dados com Pydantic
- ✅ Documentação interativa gerada pelo FastAPI (Swagger UI)
- ✅ 16 testes automatizados com pytest
- ✅ Integração contínua: os testes rodam automaticamente a cada push e pull request
- ✅ Entrega contínua: a imagem Docker da API é construída e publicada automaticamente no GitHub Container Registry

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| [Python 3.12](https://www.python.org/) | Linguagem principal |
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web da API |
| [Pydantic](https://docs.pydantic.dev/) | Modelos e validação de dados |
| [pytest](https://pytest.org/) | Testes automatizados |
| [GitHub Actions](https://github.com/features/actions) | Integração contínua (CI) |
| [Docker](https://www.docker.com/) | Empacotamento da aplicação em imagem |
| [GitHub Container Registry](https://docs.github.com/pt/packages/working-with-a-github-packages-registry/working-with-the-container-registry) | Registro de imagens (CD) |

## 📦 Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/NEVEsdev1/todo-api.git
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

## 🐳 Como rodar com Docker

A imagem mais recente da API é publicada automaticamente pelo pipeline de CD no GitHub Container Registry:

```bash
docker pull ghcr.io/nevesdev1/todo-api:latest
docker run -p 8000:8000 ghcr.io/nevesdev1/todo-api:latest
```

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

### CI — Integração contínua (`.github/workflows/ci.yml`)

O workflow de integração contínua roda automaticamente em:

- todo **push** para a branch `main`
- todo **pull request** aberto para a `main`

Em cada execução, o GitHub Actions instala as dependências em um ambiente limpo com Python 3.12 e roda a suíte completa de testes com `pytest -v`. Assim, nenhum código que quebre a API chega à branch principal sem ser detectado.

### CD — Entrega contínua (`.github/workflows/cd.yml`)

O workflow de entrega contínua completa o pipeline: constrói a **imagem Docker** da API e a publica no **GitHub Container Registry** (ghcr.io). Ele roda em:

- todo **push** para a branch `main` → publica as tags `latest`, `main` e `sha-<commit>`
- todo **pull request** para a `main` → valida o build e publica a tag `pr-<número>`

As imagens publicadas ficam disponíveis em `ghcr.io/nevesdev1/todo-api`, prontas para serem executadas em qualquer ambiente com `docker run`.

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
