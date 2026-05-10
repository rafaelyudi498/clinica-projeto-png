"""
services.py — Camada de Lógica de Negócio (Business Logic)

Contém todas as regras de negócio do sistema.
Orquestra operações entre banco de dados e validações.
"""

from datetime import datetime, date, timedelta
from typing import List, Optional, Tuple, Dict

from modules.database import Database
from modules.models import Agendamento, Paciente, Profissional, Especialidade
from modules.utils import (
    data_valida, hora_valida, data_futura, dia_util,
    hora_no_horario, calcular_horario_fim, busca_fuzzy_dict,
    horas_se_sobrepõem, gerar_id_agendamento, email_valido, telefone_valido, nome_valido
)


class AgendamentoService:
    """Serviço de gerenciamento de agendamentos."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def criar_agendamento(
        self,
        data: str,
        hora: str,
        paciente_nome: str,
        telefone: str,
        email: str,
        profissional_id: int,
        especialidade_id: int,
        notas: str = ""
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Cria um novo agendamento com todas as validações.
        
        Retorna: (sucesso, mensagem, agendamento_dict)
        """
        # ===== VALIDAÇÕES DE PACIENTE =====
        
        # 0. Nome válido?
        if not nome_valido(paciente_nome):
            return False, "❌ Nome do paciente inválido (mín. 3 caracteres, sem números)", None
        
        # 0.1 Email válido?
        if not email_valido(email):
            return False, "❌ Email inválido. Use formato: exemplo@email.com", None
        
        # 0.2 Telefone válido?
        if not telefone_valido(telefone):
            return False, "❌ Telefone inválido (mín. 10 dígitos)", None
        
        # ===== VALIDAÇÕES =====
        
        # 1. Data válida?
        if not data_valida(data):
            return False, "❌ Data inválida. Use formato YYYY-MM-DD", None
        
        # 2. Data é futura?
        if not data_futura(data):
            return False, "❌ Não é possível agendar para o passado", None
        
        # 3. Dia útil?
        if not dia_util(data):
            return False, "❌ A clínica funciona apenas seg-sex", None
        
        # 4. Hora válida?
        if not hora_valida(hora):
            return False, "❌ Hora inválida. Use formato HH:MM", None
        
        # 5. Hora dentro do horário de funcionamento (08:00-18:00)?
        if not hora_no_horario(hora, "08:00", "18:00"):
            return False, "❌ Horário fora do intervalo (08:00-18:00)", None
        
        # 6. Profissional existe?
        profissional = self.db.obter_profissional(profissional_id)
        if not profissional:
            return False, "❌ Profissional não encontrado", None
        
        if not profissional.get("ativo", False):
            return False, f"❌ Profissional {profissional['nome']} inativo", None
        
        # 7. Profissional trabalha neste dia?
        dt = datetime.strptime(data, "%Y-%m-%d").date()
        dia_semana = dt.weekday() + 1  # 1=seg, 7=dom
        if dia_semana not in profissional.get("dias_trabalho", []):
            return False, f"❌ {profissional['nome']} não trabalha neste dia", None
        
        # 8. Profissional trabalha neste horário?
        h_inicio = profissional.get("horario_inicio", "08:00")
        h_fim = profissional.get("horario_fim", "18:00")
        if not hora_no_horario(hora, h_inicio, h_fim):
            return False, f"❌ Horário fora da disponibilidade ({h_inicio}-{h_fim})", None
        
        # 9. Especialidade existe?
        especialidade = self.db.obter_especialidade(especialidade_id)
        if not especialidade:
            return False, "❌ Especialidade não encontrada", None
        
        if not especialidade.get("ativo", False):
            return False, "❌ Especialidade inativa", None
        
        # 10. Profissional tem esta especialidade?
        if especialidade_id not in profissional.get("especialidades", []):
            return False, f"❌ {profissional['nome']} não oferece esta especialidade", None
        
        # 11. Existe conflito (double-booking)?
        tem_conflito, mensagem = self._verificar_conflito(profissional_id, data, hora)
        if tem_conflito:
            return False, mensagem, None
        
        # ===== CRIAR PACIENTE SE NÃO EXISTIR =====
        
        paciente = self.db.obter_paciente_por_nome(paciente_nome)
        if not paciente:
            paciente = self.db.salvar_paciente({
                "nome": paciente_nome,
                "telefone": telefone,
                "email": email,
                "data_primeiro_contato": data,
                "total_consultas": 1,
                "ultima_consulta": data,
                "status": "ativo",
                "observacoes": None
            })
        else:
            # Atualizar contador e contato do paciente
            paciente["total_consultas"] = paciente.get("total_consultas", 0) + 1
            paciente["ultima_consulta"] = data
            paciente["telefone"] = telefone
            paciente["email"] = email
            self.db.atualizar_paciente(paciente["id"], {
                "total_consultas": paciente["total_consultas"],
                "ultima_consulta": paciente["ultima_consulta"],
                "telefone": telefone,
                "email": email
            })
        
        # ===== CRIAR AGENDAMENTO =====
        
        horario_fim = calcular_horario_fim(hora, 60)
        
        agendamento_dict = {
            # ID será gerado pelo DB
            "data": data,
            "hora": hora,
            "horario_fim": horario_fim,
            "paciente": {"id": paciente["id"], "nome": paciente["nome"]},
            "profissional": {"id": profissional["id"], "nome": profissional["nome"]},
            "especialidade": {"id": especialidade["id"], "nome": especialidade["nome"]},
            "status": "confirmado",
            "notas": notas,
            "notas_atendimento": None,
            "data_criacao": datetime.now().isoformat(),
            "data_atualizacao": datetime.now().isoformat(),
            "cancelado_em": None,
            "motivo_cancelamento": None
        }
        
        self.db.salvar_agendamento(agendamento_dict)
        
        from modules.utils import converter_para_brasileiro
        data_br = converter_para_brasileiro(data)
        
        mensagem = f"✅ Agendamento confirmado!\n   {agendamento_dict['paciente']['nome']} com {agendamento_dict['profissional']['nome']} ({agendamento_dict['especialidade']['nome']}) em {data_br} às {hora}h"
        
        return True, mensagem, agendamento_dict
    
    def _verificar_conflito(self, profissional_id: int, data: str, hora: str) -> Tuple[bool, str]:
        """
        Verifica se profissional tem outra consulta no mesmo horário.
        
        Retorna: (tem_conflito, mensagem)
        """
        agendamentos = self.db.carregar_agendamentos()
        hora_fim = calcular_horario_fim(hora, 60)
        
        for agendamento in agendamentos:
            # Filtrar: mesma data, mesmo profissional, não cancelado
            if (agendamento["profissional"]["id"] == profissional_id and
                agendamento["data"] == data and
                agendamento["status"] != "cancelado"):
                
                # Verificar sobreposição de horas
                if horas_se_sobrepõem(hora, hora_fim, agendamento["hora"], agendamento["horario_fim"]):
                    return True, f"❌ Conflito: profissional já tem agendamento em {agendamento['hora']}h"
        
        return False, ""
    
    def listar_agendamentos(self) -> List[dict]:
        """Retorna todos os agendamentos (não cancelados)."""
        return [
            a for a in self.db.carregar_agendamentos()
            if a.get("status") != "cancelado"
        ]
    
    def listar_por_data(self, data: str) -> List[dict]:
        """Retorna agendamentos de uma data específica."""
        if not data_valida(data):
            return []
        
        return sorted(
            [a for a in self.listar_agendamentos() if a["data"] == data],
            key=lambda x: x["hora"]
        )
    
    def listar_por_profissional(self, profissional_id: int) -> List[dict]:
        """Retorna agendamentos de um profissional."""
        return sorted(
            [a for a in self.listar_agendamentos() if a["profissional"]["id"] == profissional_id],
            key=lambda x: (x["data"], x["hora"])
        )
    
    def listar_por_paciente(self, paciente_id: int) -> List[dict]:
        """Retorna todos os agendamentos de um paciente (inclusive cancelados)."""
        agendamentos = self.db.carregar_agendamentos()
        return sorted(
            [a for a in agendamentos if a["paciente"]["id"] == paciente_id],
            key=lambda x: (x["data"], x["hora"]),
            reverse=True  # Mais recentes primeiro
        )
    
    def obter_agendamento(self, id_agendamento: str) -> Optional[dict]:
        """Obtém um agendamento pelo ID."""
        return self.db.obter_agendamento(id_agendamento)
    
    def finalizar_agendamento(self, id_agendamento: str, notas_atendimento: str) -> Tuple[bool, str]:
        """Marca agendamento como concluído."""
        agendamento = self.db.obter_agendamento(id_agendamento)
        if not agendamento:
            return False, "❌ Agendamento não encontrado"
        
        self.db.atualizar_agendamento(id_agendamento, {
            "status": "concluido",
            "notas_atendimento": notas_atendimento
        })
        
        return True, f"✅ Agendamento marcado como concluído"
    
    def reagendar_agendamento(
        self,
        id_agendamento: str,
        nova_data: str,
        nova_hora: str,
        motivo: str = ""
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Reagenda um agendamento existente para nova data/hora.
        
        Retorna: (sucesso, mensagem, agendamento_atualizado)
        """
        # Obter agendamento original
        agendamento_original = self.db.obter_agendamento(id_agendamento)
        if not agendamento_original:
            return False, "❌ Agendamento não encontrado", None
        
        # Validar status
        if agendamento_original["status"] == "concluido":
            return False, "❌ Não é possível reagendar um agendamento concluído", None
        
        if agendamento_original["status"] == "cancelado":
            return False, "❌ Não é possível reagendar um agendamento cancelado", None
        
        # Validar nova data/hora
        if not data_valida(nova_data):
            return False, "❌ Data inválida. Use formato YYYY-MM-DD", None
        
        if not data_futura(nova_data):
            return False, "❌ A nova data deve ser no futuro", None
        
        if not dia_util(nova_data):
            return False, "❌ A clínica funciona apenas seg-sex", None
        
        if not hora_valida(nova_hora):
            return False, "❌ Hora inválida. Use formato HH:MM", None
        
        if not hora_no_horario(nova_hora, "08:00", "18:00"):
            return False, "❌ Horário fora do intervalo (08:00-18:00)", None
        
        # Validar disponibilidade do profissional
        profissional_id = agendamento_original["profissional"]["id"]
        profissional = self.db.obter_profissional(profissional_id)
        
        if not profissional or not profissional.get("ativo", False):
            return False, "❌ Profissional indisponível", None
        
        # Verificar dia de trabalho
        dt = datetime.strptime(nova_data, "%Y-%m-%d").date()
        dia_semana = dt.weekday() + 1
        if dia_semana not in profissional.get("dias_trabalho", []):
            return False, f"❌ Profissional não trabalha neste dia", None
        
        # Verificar horário de trabalho
        h_inicio = profissional.get("horario_inicio", "08:00")
        h_fim = profissional.get("horario_fim", "18:00")
        if not hora_no_horario(nova_hora, h_inicio, h_fim):
            return False, f"❌ Horário fora da disponibilidade ({h_inicio}-{h_fim})", None
        
        # Verificar conflitos (não contar com o agendamento atual)
        tem_conflito, mensagem = self._verificar_conflito_excludente(
            profissional_id, nova_data, nova_hora, id_agendamento
        )
        if tem_conflito:
            return False, mensagem, None
        
        # Atualizar agendamento
        nova_hora_fim = calcular_horario_fim(nova_hora, 60)
        
        self.db.atualizar_agendamento(id_agendamento, {
            "data": nova_data,
            "hora": nova_hora,
            "horario_fim": nova_hora_fim,
            "data_atualizacao": datetime.now().isoformat(),
            "motivo_reagendamento": motivo or ""
        })
        
        agendamento_atualizado = self.db.obter_agendamento(id_agendamento)
        
        from modules.utils import converter_para_brasileiro
        nova_data_br = converter_para_brasileiro(nova_data)
        
        mensagem = f"✅ Agendamento reagendado com sucesso para {nova_data_br} às {nova_hora}h"
        return True, mensagem, agendamento_atualizado
    
    def _verificar_conflito_excludente(
        self, profissional_id: int, data: str, hora: str, id_agendamento_excludir: str
    ) -> Tuple[bool, str]:
        """
        Verifica conflito excluindo um agendamento específico.
        Usada para reagendamento.
        
        Retorna: (tem_conflito, mensagem)
        """
        agendamentos = self.db.carregar_agendamentos()
        hora_fim = calcular_horario_fim(hora, 60)
        
        for agendamento in agendamentos:
            # Pular o agendamento que estamos reagendando
            if agendamento["id"] == id_agendamento_excludir:
                continue
            
            # Filtrar: mesma data, mesmo profissional, não cancelado
            if (agendamento["profissional"]["id"] == profissional_id and
                agendamento["data"] == data and
                agendamento["status"] != "cancelado"):
                
                # Verificar sobreposição de horas
                if horas_se_sobrepõem(hora, hora_fim, agendamento["hora"], agendamento["horario_fim"]):
                    return True, f"❌ Conflito: profissional já tem agendamento em {agendamento['hora']}h"
        
        return False, ""
    
    def cancelar_agendamento(self, id_agendamento: str, motivo: str) -> Tuple[bool, str]:
        """Cancela um agendamento."""
        agendamento = self.db.obter_agendamento(id_agendamento)
        if not agendamento:
            return False, "❌ Agendamento não encontrado"
        
        if agendamento["status"] == "cancelado":
            return False, "⚠️ Agendamento já foi cancelado"
        
        self.db.deletar_agendamento_logico(id_agendamento, motivo)
        
        return True, f"✅ Agendamento cancelado"


class PacienteService:
    """Serviço de gerenciamento de pacientes."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def buscar_por_nome(self, nome: str) -> List[dict]:
        """Busca exata de paciente."""
        pacientes = self.db.carregar_pacientes()
        return [p for p in pacientes if p["nome"].lower() == nome.lower()]
    
    def buscar_por_nome_fuzzy(self, nome: str, limiar: float = 0.6) -> List[Tuple[float, dict]]:
        """Busca fuzzy de pacientes (com score)."""
        pacientes = self.db.carregar_pacientes()
        return busca_fuzzy_dict(nome, pacientes, "nome", limiar)
    
    def obter_historico(self, paciente_id: int) -> List[dict]:
        """Retorna histórico completo de agendamentos do paciente."""
        service_agend = AgendamentoService(self.db)
        return service_agend.listar_por_paciente(paciente_id)
    
    def obter_paciente(self, paciente_id: int) -> Optional[dict]:
        """Obtém paciente pelo ID."""
        return self.db.obter_paciente_por_id(paciente_id)


class ProfissionalService:
    """Serviço de gerenciamento de profissionais."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def listar_todos(self) -> List[dict]:
        """Retorna todos os profissionais ativos."""
        return [p for p in self.db.carregar_profissionais() if p.get("ativo", False)]
    
    def listar_por_especialidade(self, especialidade_id: int) -> List[dict]:
        """Retorna profissionais que oferecem uma especialidade."""
        return [
            p for p in self.listar_todos()
            if especialidade_id in p.get("especialidades", [])
        ]
    
    def criar_profissional(
        self,
        nome: str,
        crp: str,
        especialidades: List[int],
        horario_inicio: str = "08:00",
        horario_fim: str = "18:00",
        dias_trabalho: List[int] = None,
        observacoes: str = ""
    ) -> Tuple[bool, str, Optional[dict]]:
        """Cria novo profissional com validações."""
        
        # Validações
        if not nome or len(nome) < 3:
            return False, "❌ Nome inválido", None
        
        if not hora_valida(horario_inicio) or not hora_valida(horario_fim):
            return False, "❌ Horários inválidos", None
        
        if not especialidades:
            return False, "❌ Especifique pelo menos uma especialidade", None
        
        dias_trabalho = dias_trabalho or [1, 2, 3, 4, 5]  # seg-sex
        
        # Criar
        prof_dict = {
            "nome": nome,
            "crp": crp or None,
            "especialidades": especialidades,
            "horario_inicio": horario_inicio,
            "horario_fim": horario_fim,
            "dias_trabalho": dias_trabalho,
            "ativo": True,
            "data_criacao": datetime.now().isoformat(),
            "observacoes": observacoes or None
        }
        
        resultado = self.db.salvar_profissional(prof_dict)
        
        return True, f"✅ Profissional {nome} cadastrado", resultado
    
    def obter_profissional(self, profissional_id: int) -> Optional[dict]:
        """Obtém profissional pelo ID."""
        return self.db.obter_profissional(profissional_id)


class EspecialidadeService:
    """Serviço de gerenciamento de especialidades."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def listar_todas(self) -> List[dict]:
        """Retorna todas as especialidades ativas."""
        return [e for e in self.db.carregar_especialidades() if e.get("ativo", False)]
    
    def criar_especialidade(
        self,
        nome: str,
        descricao: str = ""
    ) -> Tuple[bool, str, Optional[dict]]:
        """Cria nova especialidade."""
        
        if not nome or len(nome) < 3:
            return False, "❌ Nome inválido", None
        
        esp_dict = {
            "nome": nome,
            "descricao": descricao or "",
            "ativo": True,
            "data_criacao": datetime.now().isoformat()
        }
        
        resultado = self.db.salvar_especialidade(esp_dict)
        
        return True, f"✅ Especialidade {nome} cadastrada", resultado
    
    def obter_especialidade(self, especialidade_id: int) -> Optional[dict]:
        """Obtém especialidade pelo ID."""
        return self.db.obter_especialidade(especialidade_id)


class RelatorioService:
    """Serviço de geração de relatórios."""
    
    def __init__(self, db: Database):
        self.db = db
        self.agend_service = AgendamentoService(db)
    
    def relatorio_dia(self, data: str) -> Dict:
        """Relatório de agendamentos do dia."""
        if not data_valida(data):
            return {"erro": "Data inválida"}
        
        agendamentos = self.agend_service.listar_por_data(data)
        confirmados = [a for a in agendamentos if a["status"] == "confirmado"]
        concluidos = [a for a in agendamentos if a["status"] == "concluido"]
        
        from modules.utils import converter_para_brasileiro
        
        return {
            "data": converter_para_brasileiro(data),
            "total_agendamentos": len(agendamentos),
            "confirmados": len(confirmados),
            "concluidos": len(concluidos),
            "agendamentos": agendamentos
        }
    
    def relatorio_periodo(
        self,
        data_inicio: str,
        data_fim: str,
        profissional_id: Optional[int] = None
    ) -> Dict:
        """Relatório de agendamentos por período."""
        
        if not (data_valida(data_inicio) and data_valida(data_fim)):
            return {"erro": "Datas inválidas"}
        
        from modules.utils import converter_para_brasileiro
        
        agendamentos = self.db.carregar_agendamentos()
        
        # Filtrar por período
        agendamentos_periodo = [
            a for a in agendamentos
            if data_inicio <= a["data"] <= data_fim
        ]
        
        # Filtrar por profissional se especificado
        if profissional_id:
            agendamentos_periodo = [
                a for a in agendamentos_periodo
                if a["profissional"]["id"] == profissional_id
            ]
        
        # Contar por status
        confirmados = [a for a in agendamentos_periodo if a["status"] == "confirmado"]
        concluidos = [a for a in agendamentos_periodo if a["status"] == "concluido"]
        cancelados = [a for a in agendamentos_periodo if a["status"] == "cancelado"]
        
        # Taxa de ocupação (simplificada)
        taxa_ocupacao = (len(confirmados) + len(concluidos)) / max(len(agendamentos_periodo), 1) * 100
        
        data_inicio_br = converter_para_brasileiro(data_inicio)
        data_fim_br = converter_para_brasileiro(data_fim)
        
        return {
            "periodo": f"{data_inicio_br} a {data_fim_br}",
            "total": len(agendamentos_periodo),
            "confirmados": len(confirmados),
            "concluidos": len(concluidos),
            "cancelados": len(cancelados),
            "taxa_ocupacao": f"{taxa_ocupacao:.1f}%",
            "agendamentos": agendamentos_periodo
        }
