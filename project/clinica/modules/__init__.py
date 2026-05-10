"""
modules — Pacote de módulos da aplicação

Contém a lógica de negócio, persistência e apresentação.
"""

from modules.models import Agendamento, Paciente, Profissional, Especialidade
from modules.database import Database
from modules.services import (
    AgendamentoService,
    PacienteService,
    ProfissionalService,
    EspecialidadeService,
    RelatorioService
)

__all__ = [
    "Agendamento",
    "Paciente",
    "Profissional",
    "Especialidade",
    "Database",
    "AgendamentoService",
    "PacienteService",
    "ProfissionalService",
    "EspecialidadeService",
    "RelatorioService",
]
