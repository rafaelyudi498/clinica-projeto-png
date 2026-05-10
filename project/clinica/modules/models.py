"""
models.py — Estruturas de dados (Dataclasses)

Define as classes que representam os dados do sistema.
Todas as classes usam @dataclass para type hints e simplicidade.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Especialidade:
    """Tipo de consulta/serviço oferecido."""
    id: int
    nome: str
    descricao: str
    ativo: bool = True
    data_criacao: str = field(default_factory=lambda: datetime.now().isoformat())

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "ativo": self.ativo,
            "data_criacao": self.data_criacao
        }


@dataclass
class Profissional:
    """Psicólogo ou profissional da clínica."""
    id: int
    nome: str
    crp: Optional[str]
    especialidades: List[int]  # IDs de especialidades
    horario_inicio: str  # HH:MM
    horario_fim: str  # HH:MM
    dias_trabalho: List[int]  # [1=seg, 2=ter, 3=qua, 4=qui, 5=sex]
    ativo: bool = True
    data_criacao: str = field(default_factory=lambda: datetime.now().isoformat())
    observacoes: Optional[str] = None

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "crp": self.crp,
            "especialidades": self.especialidades,
            "horario_inicio": self.horario_inicio,
            "horario_fim": self.horario_fim,
            "dias_trabalho": self.dias_trabalho,
            "ativo": self.ativo,
            "data_criacao": self.data_criacao,
            "observacoes": self.observacoes
        }


@dataclass
class Paciente:
    """Histórico e indexação de pacientes."""
    id: int
    nome: str
    telefone: str
    email: str
    data_primeiro_contato: str  # YYYY-MM-DD
    total_consultas: int = 0
    ultima_consulta: Optional[str] = None  # YYYY-MM-DD
    status: str = "ativo"  # "ativo" | "inativo"
    observacoes: Optional[str] = None

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "data_primeiro_contato": self.data_primeiro_contato,
            "total_consultas": self.total_consultas,
            "ultima_consulta": self.ultima_consulta,
            "status": self.status,
            "observacoes": self.observacoes
        }


@dataclass
class Agendamento:
    """Registro de uma consulta agendada."""
    id: str  # AGD-YYYY-NNNN
    data: str  # YYYY-MM-DD
    hora: str  # HH:MM
    horario_fim: str  # HH:MM
    paciente: dict  # {id, nome}
    profissional: dict  # {id, nome}
    especialidade: dict  # {id, nome}
    status: str  # "confirmado" | "concluido" | "cancelado"
    notas: str
    notas_atendimento: Optional[str] = None
    data_criacao: str = field(default_factory=lambda: datetime.now().isoformat())
    data_atualizacao: str = field(default_factory=lambda: datetime.now().isoformat())
    cancelado_em: Optional[str] = None
    motivo_cancelamento: Optional[str] = None

    def para_dict(self) -> dict:
        return {
            "id": self.id,
            "data": self.data,
            "hora": self.hora,
            "horario_fim": self.horario_fim,
            "paciente": self.paciente,
            "profissional": self.profissional,
            "especialidade": self.especialidade,
            "status": self.status,
            "notas": self.notas,
            "notas_atendimento": self.notas_atendimento,
            "data_criacao": self.data_criacao,
            "data_atualizacao": self.data_atualizacao,
            "cancelado_em": self.cancelado_em,
            "motivo_cancelamento": self.motivo_cancelamento
        }

    @staticmethod
    def de_dict(data: dict) -> "Agendamento":
        """Cria Agendamento a partir de dicionário."""
        return Agendamento(
            id=data.get("id"),
            data=data.get("data"),
            hora=data.get("hora"),
            horario_fim=data.get("horario_fim"),
            paciente=data.get("paciente"),
            profissional=data.get("profissional"),
            especialidade=data.get("especialidade"),
            status=data.get("status", "confirmado"),
            notas=data.get("notas", ""),
            notas_atendimento=data.get("notas_atendimento"),
            data_criacao=data.get("data_criacao"),
            data_atualizacao=data.get("data_atualizacao"),
            cancelado_em=data.get("cancelado_em"),
            motivo_cancelamento=data.get("motivo_cancelamento")
        )
