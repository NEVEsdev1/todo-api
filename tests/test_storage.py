"""Testes unitários da classe ArmazenamentoTarefas.

Diferente dos testes de API (tests/test_api.py), aqui os testes são
unitários: exercitam a classe de armazenamento de forma isolada,
sem passar pela camada HTTP.
"""

from datetime import datetime

import pytest

from app.models import TarefaCreate, TarefaUpdate
from app.storage import ArmazenamentoTarefas, TarefaNaoEncontrada


@pytest.fixture()
def armazenamento():
    """Armazenamento limpo para cada teste unitário."""
    return ArmazenamentoTarefas()


def test_criar_atribui_id_sequencial_e_valores_padrao(armazenamento):
    primeira = armazenamento.criar(TarefaCreate(titulo="Primeira"))
    segunda = armazenamento.criar(TarefaCreate(titulo="Segunda"))

    assert primeira.id == 1
    assert segunda.id == 2
    assert primeira.concluida is False
    assert primeira.prioridade == 1  # valor padrão
    assert isinstance(primeira.criada_em, datetime)


def test_listar_sem_tarefas_retorna_lista_vazia(armazenamento):
    assert armazenamento.listar() == []


def test_filtro_por_status_no_listar(armazenamento):
    armazenamento.criar(TarefaCreate(titulo="Pendente"))
    concluida = armazenamento.criar(TarefaCreate(titulo="Concluída"))
    armazenamento.atualizar(concluida.id, TarefaUpdate(concluida=True))

    pendentes = armazenamento.listar(concluida=False)
    concluidas = armazenamento.listar(concluida=True)

    assert [t.titulo for t in pendentes] == ["Pendente"]
    assert [t.titulo for t in concluidas] == ["Concluída"]


def test_atualizar_preserva_campos_nao_informados(armazenamento):
    criada = armazenamento.criar(
        TarefaCreate(titulo="Original", descricao="Descrição antiga", prioridade=2)
    )

    atualizada = armazenamento.atualizar(criada.id, TarefaUpdate(titulo="Novo título"))

    assert atualizada.titulo == "Novo título"
    assert atualizada.descricao == "Descrição antiga"
    assert atualizada.prioridade == 2
    assert atualizada.concluida is False


def test_remover_exclui_a_tarefa_do_armazenamento(armazenamento):
    criada = armazenamento.criar(TarefaCreate(titulo="Para remover"))

    armazenamento.remover(criada.id)

    assert armazenamento.listar() == []
    with pytest.raises(TarefaNaoEncontrada):
        armazenamento.obter(criada.id)


def test_operacoes_sobre_id_inexistente_lancam_excecao(armazenamento):
    with pytest.raises(TarefaNaoEncontrada):
        armazenamento.obter(999)
    with pytest.raises(TarefaNaoEncontrada):
        armazenamento.atualizar(999, TarefaUpdate(titulo="Nada"))
    with pytest.raises(TarefaNaoEncontrada):
        armazenamento.remover(999)
