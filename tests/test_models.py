"""Testes unitários dos modelos Pydantic.

Validam as regras de dados (campos obrigatórios, limites e valores
padrão) de forma isolada da API e do armazenamento.
"""

import pytest
from pydantic import ValidationError

from app.models import TarefaCreate, TarefaUpdate


def test_tarefa_create_tem_valores_padrao():
    tarefa = TarefaCreate(titulo="Somente título")

    assert tarefa.titulo == "Somente título"
    assert tarefa.descricao == ""
    assert tarefa.prioridade == 1


def test_titulo_vazio_e_rejeitado():
    with pytest.raises(ValidationError):
        TarefaCreate(titulo="")


def test_titulo_acima_do_limite_e_rejeitado():
    with pytest.raises(ValidationError):
        TarefaCreate(titulo="a" * 101)


def test_prioridade_fora_do_intervalo_e_rejeitada():
    with pytest.raises(ValidationError):
        TarefaCreate(titulo="Inválida", prioridade=0)
    with pytest.raises(ValidationError):
        TarefaCreate(titulo="Inválida", prioridade=6)


def test_tarefa_update_aceita_qualquer_combinacao_de_campos():
    so_titulo = TarefaUpdate(titulo="Novo")
    so_concluida = TarefaUpdate(concluida=True)
    vazio = TarefaUpdate()

    assert so_titulo.concluida is None
    assert so_concluida.titulo is None
    assert vazio.model_dump() == {
        "titulo": None,
        "descricao": None,
        "prioridade": None,
        "concluida": None,
    }
