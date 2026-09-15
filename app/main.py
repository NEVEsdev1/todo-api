"""API de gerenciamento de tarefas desenvolvida com FastAPI."""

from fastapi import Depends, FastAPI, HTTPException, Query, status

from app.models import Tarefa, TarefaCreate, TarefaUpdate
from app.storage import ArmazenamentoTarefas, TarefaNaoEncontrada

armazenamento = ArmazenamentoTarefas()

app = FastAPI(
    title="API de Tarefas",
    description=(
        "API REST para gerenciamento de tarefas, desenvolvida para a "
        "disciplina de DevOps da PUCPR."
    ),
    version="1.0.0",
)


def obter_armazenamento() -> ArmazenamentoTarefas:
    """Fornece a instância de armazenamento utilizada pelas rotas."""
    return armazenamento


@app.get("/")
def raiz() -> dict[str, str]:
    """Endpoint inicial com uma mensagem de boas-vindas."""
    return {
        "mensagem": "Bem-vindo à API de Tarefas! Acesse /docs para ver a documentação interativa."
    }


@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas(
    concluida: bool | None = Query(
        default=None, description="Filtrar tarefas por status"
    ),
    armazenamento: ArmazenamentoTarefas = Depends(obter_armazenamento),
) -> list[Tarefa]:
    """Lista todas as tarefas, com filtro opcional por status."""
    return armazenamento.listar(concluida=concluida)


@app.post(
    "/tarefas",
    response_model=Tarefa,
    status_code=status.HTTP_201_CREATED,
)
def criar_tarefa(
    dados: TarefaCreate,
    armazenamento: ArmazenamentoTarefas = Depends(obter_armazenamento),
) -> Tarefa:
    """Cria uma nova tarefa."""
    return armazenamento.criar(dados)


@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def obter_tarefa(
    tarefa_id: int,
    armazenamento: ArmazenamentoTarefas = Depends(obter_armazenamento),
) -> Tarefa:
    """Busca uma tarefa pelo id."""
    try:
        return armazenamento.obter(tarefa_id)
    except TarefaNaoEncontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )


@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(
    tarefa_id: int,
    dados: TarefaUpdate,
    armazenamento: ArmazenamentoTarefas = Depends(obter_armazenamento),
) -> Tarefa:
    """Atualiza os campos informados de uma tarefa."""
    try:
        return armazenamento.atualizar(tarefa_id, dados)
    except TarefaNaoEncontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )


@app.delete("/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_tarefa(
    tarefa_id: int,
    armazenamento: ArmazenamentoTarefas = Depends(obter_armazenamento),
) -> None:
    """Remove uma tarefa pelo id."""
    try:
        armazenamento.remover(tarefa_id)
    except TarefaNaoEncontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada",
        )
