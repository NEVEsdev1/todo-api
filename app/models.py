"""Modelos de dados da API de tarefas."""

from datetime import datetime

from pydantic import BaseModel, Field


class TarefaCreate(BaseModel):
    """Dados necessários para criar uma nova tarefa."""

    titulo: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Título da tarefa",
        examples=["Estudar DevOps"],
    )
    descricao: str = Field(
        default="",
        max_length=500,
        description="Descrição detalhada da tarefa",
    )
    prioridade: int = Field(
        default=1,
        ge=1,
        le=5,
        description="Prioridade de 1 (baixa) a 5 (alta)",
    )


class TarefaUpdate(BaseModel):
    """Campos que podem ser atualizados em uma tarefa existente.

    Todos os campos são opcionais: apenas os campos informados são alterados.
    """

    titulo: str | None = Field(default=None, min_length=1, max_length=100)
    descricao: str | None = Field(default=None, max_length=500)
    prioridade: int | None = Field(default=None, ge=1, le=5)
    concluida: bool | None = None


class Tarefa(TarefaCreate):
    """Representação completa de uma tarefa já persistida."""

    id: int
    concluida: bool = False
    criada_em: datetime
