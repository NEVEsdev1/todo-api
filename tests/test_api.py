"""Testes automatizados da API de tarefas."""

import pytest
from fastapi.testclient import TestClient

from app.main import app, obter_armazenamento
from app.storage import ArmazenamentoTarefas


@pytest.fixture()
def cliente():
    """Cliente de teste com um armazenamento limpo para cada teste."""
    armazenamento = ArmazenamentoTarefas()
    app.dependency_overrides[obter_armazenamento] = lambda: armazenamento
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def criar_tarefa(cliente: TestClient, titulo: str = "Estudar DevOps", **extras) -> dict:
    """Cria uma tarefa via API e retorna o corpo da resposta."""
    resposta = cliente.post("/tarefas", json={"titulo": titulo, **extras})
    assert resposta.status_code == 201
    return resposta.json()


def test_raiz_retorna_mensagem(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert "mensagem" in resposta.json()


def test_listar_tarefas_vazia(cliente):
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_criar_tarefa_com_sucesso(cliente):
    resposta = cliente.post(
        "/tarefas",
        json={
            "titulo": "Estudar DevOps",
            "descricao": "Revisar o conteúdo de CI/CD",
            "prioridade": 3,
        },
    )
    assert resposta.status_code == 201
    tarefa = resposta.json()
    assert tarefa["id"] == 1
    assert tarefa["titulo"] == "Estudar DevOps"
    assert tarefa["descricao"] == "Revisar o conteúdo de CI/CD"
    assert tarefa["prioridade"] == 3
    assert tarefa["concluida"] is False
    assert tarefa["criada_em"] is not None


def test_criar_tarefa_sem_titulo_retorna_erro(cliente):
    resposta = cliente.post("/tarefas", json={"descricao": "sem título"})
    assert resposta.status_code == 422


def test_criar_tarefa_com_prioridade_invalida(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "Inválida", "prioridade": 10})
    assert resposta.status_code == 422


def test_ids_sao_sequenciais(cliente):
    primeira = criar_tarefa(cliente)
    segunda = criar_tarefa(cliente, titulo="Fazer o trabalho de DevOps")
    assert primeira["id"] == 1
    assert segunda["id"] == 2


def test_obter_tarefa_existente(cliente):
    criada = criar_tarefa(cliente)
    resposta = cliente.get(f"/tarefas/{criada['id']}")
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == criada["titulo"]


def test_obter_tarefa_inexistente(cliente):
    resposta = cliente.get("/tarefas/999")
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Tarefa não encontrada"


def test_obter_tarefa_com_id_invalido(cliente):
    resposta = cliente.get("/tarefas/abc")
    assert resposta.status_code == 422


def test_listar_tarefas_retorna_todas(cliente):
    criar_tarefa(cliente)
    criar_tarefa(cliente, titulo="Segunda tarefa")
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 2


def test_filtro_por_status(cliente):
    criar_tarefa(cliente, titulo="Pendente")
    concluida = criar_tarefa(cliente, titulo="Concluída")
    cliente.put(f"/tarefas/{concluida['id']}", json={"concluida": True})

    pendentes = cliente.get("/tarefas", params={"concluida": False}).json()
    concluidas = cliente.get("/tarefas", params={"concluida": True}).json()

    assert [t["titulo"] for t in pendentes] == ["Pendente"]
    assert [t["titulo"] for t in concluidas] == ["Concluída"]


def test_atualizar_tarefa_parcialmente(cliente):
    criada = criar_tarefa(cliente, descricao="Descrição original", prioridade=2)
    resposta = cliente.put(
        f"/tarefas/{criada['id']}",
        json={"titulo": "Título atualizado", "prioridade": 5},
    )
    assert resposta.status_code == 200
    tarefa = resposta.json()
    assert tarefa["titulo"] == "Título atualizado"
    assert tarefa["prioridade"] == 5
    # Campos não informados devem ser preservados
    assert tarefa["descricao"] == "Descrição original"
    assert tarefa["concluida"] is False


def test_atualizar_tarefa_inexistente(cliente):
    resposta = cliente.put("/tarefas/999", json={"titulo": "Nada"})
    assert resposta.status_code == 404


def test_marcar_tarefa_como_concluida(cliente):
    criada = criar_tarefa(cliente)
    resposta = cliente.put(f"/tarefas/{criada['id']}", json={"concluida": True})
    assert resposta.status_code == 200
    assert resposta.json()["concluida"] is True


def test_remover_tarefa(cliente):
    criada = criar_tarefa(cliente)
    resposta = cliente.delete(f"/tarefas/{criada['id']}")
    assert resposta.status_code == 204
    assert cliente.get(f"/tarefas/{criada['id']}").status_code == 404


def test_remover_tarefa_inexistente(cliente):
    resposta = cliente.delete("/tarefas/999")
    assert resposta.status_code == 404
