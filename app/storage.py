"""Armazenamento em memória para as tarefas."""

from datetime import datetime, timezone

from app.models import Tarefa, TarefaCreate, TarefaUpdate


class TarefaNaoEncontrada(Exception):
    """Exceção lançada quando uma tarefa não existe no armazenamento."""


class ArmazenamentoTarefas:
    """Gerencia as tarefas em um dicionário em memória.

    A cada nova execução da aplicação o armazenamento começa vazio —
    os dados não são persistidos em banco.
    """

    def __init__(self) -> None:
        self._tarefas: dict[int, Tarefa] = {}
        self._proximo_id = 1

    def criar(self, dados: TarefaCreate) -> Tarefa:
        """Registra uma nova tarefa e retorna sua representação completa."""
        tarefa = Tarefa(
            id=self._proximo_id,
            concluida=False,
            criada_em=datetime.now(timezone.utc),
            **dados.model_dump(),
        )
        self._tarefas[tarefa.id] = tarefa
        self._proximo_id += 1
        return tarefa

    def listar(self, concluida: bool | None = None) -> list[Tarefa]:
        """Lista todas as tarefas, com filtro opcional por status."""
        tarefas = list(self._tarefas.values())
        if concluida is not None:
            tarefas = [t for t in tarefas if t.concluida is concluida]
        return tarefas

    def obter(self, tarefa_id: int) -> Tarefa:
        """Busca uma tarefa pelo id, ou levanta TarefaNaoEncontrada."""
        tarefa = self._tarefas.get(tarefa_id)
        if tarefa is None:
            raise TarefaNaoEncontrada(f"Tarefa {tarefa_id} não encontrada")
        return tarefa

    def atualizar(self, tarefa_id: int, dados: TarefaUpdate) -> Tarefa:
        """Atualiza apenas os campos informados de uma tarefa existente."""
        tarefa = self.obter(tarefa_id)
        campos = dados.model_dump(exclude_unset=True)
        tarefa_atualizada = tarefa.model_copy(update=campos)
        self._tarefas[tarefa_id] = tarefa_atualizada
        return tarefa_atualizada

    def remover(self, tarefa_id: int) -> None:
        """Remove uma tarefa pelo id, ou levanta TarefaNaoEncontrada."""
        self.obter(tarefa_id)
        del self._tarefas[tarefa_id]
