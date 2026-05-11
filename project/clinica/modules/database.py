"""
database.py — Camada de Persistência (Repository Pattern)

Responsável por leitura/escrita em JSON e cache em memória.
Centraliza toda a lógica de persistência do sistema.
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict

from modules.models import Agendamento, Paciente, Profissional, Especialidade
from modules.utils import gerar_id_agendamento


class Database:
    """Gerencia persistência de dados em JSON com cache em memória."""
    
    def __init__(self, dados_dir: str = "dados"):
        """
        Inicializa o banco de dados.
        
        Args:
            dados_dir: Diretório onde os arquivos JSON serão armazenados
        """
        self.dados_dir = Path(dados_dir)
        self.backup_dir = self.dados_dir / "backup"
        
        # Garantir que diretórios existem
        self.dados_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Caminhos dos arquivos
        self.arquivo_agendamentos = self.dados_dir / "agendamentos.json"
        self.arquivo_pacientes = self.dados_dir / "pacientes.json"
        self.arquivo_profissionais = self.dados_dir / "profissionais.json"
        self.arquivo_especialidades = self.dados_dir / "especialidades.json"
        
        # Cache em memória
        self._agendamentos: Optional[List[dict]] = None
        self._pacientes: Optional[List[dict]] = None
        self._profissionais: Optional[List[dict]] = None
        self._especialidades: Optional[List[dict]] = None
        
        # Contadores para IDs auto-incremento
        self._proximo_id_agendamento = None
        self._proximo_id_paciente = None
        self._proximo_id_profissional = None
        self._proximo_id_especialidade = None
        
        # Inicializar arquivos se não existirem
        self._inicializar_arquivos()
        
        # Carregar dados
        self._carregar_dados()
    
    # =========================================================================
    # INICIALIZAÇÃO
    # =========================================================================
    
    def _inicializar_arquivos(self):
        """Cria arquivos JSON vazios se não existirem."""
        if not self.arquivo_agendamentos.exists():
            self._escrever_json(self.arquivo_agendamentos, [])
        
        if not self.arquivo_pacientes.exists():
            self._escrever_json(self.arquivo_pacientes, [])
        
        if not self.arquivo_profissionais.exists():
            self._escrever_json(self.arquivo_profissionais, [])
        
        if not self.arquivo_especialidades.exists():
            self._escrever_json(self.arquivo_especialidades, [])
    
    def _carregar_dados(self):
        """Carrega todos os dados em memória."""
        self._agendamentos = self._ler_json(self.arquivo_agendamentos)
        self._pacientes = self._ler_json(self.arquivo_pacientes)
        self._profissionais = self._ler_json(self.arquivo_profissionais)
        self._especialidades = self._ler_json(self.arquivo_especialidades)
        
        # Calcular próximos IDs
        self._atualizar_contadores()
    
    def _atualizar_contadores(self):
        """Calcula os próximos IDs disponíveis."""
        # Agendamentos usam formato AGD-YYYY-NNNN, então contador é sequencial
        if self._agendamentos:
            ids_existentes = [
                int(a["id"].split("-")[-1]) for a in self._agendamentos
                if "id" in a
            ]
            self._proximo_id_agendamento = max(ids_existentes) + 1 if ids_existentes else 1
        else:
            self._proximo_id_agendamento = 1
        
        # Pacientes
        if self._pacientes:
            ids = [p["id"] for p in self._pacientes if "id" in p]
            self._proximo_id_paciente = max(ids) + 1 if ids else 1
        else:
            self._proximo_id_paciente = 1
        
        # Profissionais
        if self._profissionais:
            ids = [p["id"] for p in self._profissionais if "id" in p]
            self._proximo_id_profissional = max(ids) + 1 if ids else 1
        else:
            self._proximo_id_profissional = 1
        
        # Especialidades
        if self._especialidades:
            ids = [e["id"] for e in self._especialidades if "id" in e]
            self._proximo_id_especialidade = max(ids) + 1 if ids else 1
        else:
            self._proximo_id_especialidade = 1
    
    
    # =========================================================================
    # OPERAÇÕES ARQUIVO (I/O)
    # =========================================================================
    
    @staticmethod
    def _ler_json(caminho: Path) -> List[dict]:
        """Lê arquivo JSON de forma segura."""
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    @staticmethod
    def _escrever_json(caminho: Path, dados: List[dict]):
        """Escreve arquivo JSON de forma segura."""
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    def _fazer_backup(self, nome_arquivo: str) -> bool:
        """
        Faz backup de um arquivo antes de modificar.

        Args:
            nome_arquivo: Nome do arquivo a fazer backup

        Returns:
            bool: True se backup foi criado com sucesso, False caso contrário
        """
        try:
            caminho_original = self.dados_dir / nome_arquivo
            if not caminho_original.exists():
                return True

            # Criar pasta do dia
            hoje = datetime.now().strftime("%Y-%m-%d")
            backup_dia = self.backup_dir / hoje
            backup_dia.mkdir(exist_ok=True, parents=True)

            # Nome com timestamp
            timestamp = datetime.now().strftime("%H-%M-%S")
            nome_backup = f"{nome_arquivo.replace('.json', '')}_backup_{timestamp}.json"
            caminho_backup = backup_dia / nome_backup

            # Copiar arquivo
            shutil.copy2(caminho_original, caminho_backup)

            # Limpar backups antigos (> 30 dias)
            self._limpar_backups_antigos()

            return True

        except (OSError, PermissionError) as err:
            print(
                f"[DB] ⚠️ Erro ao fazer backup de {nome_arquivo}: {err}",
                file=__import__("sys").stderr,
            )
            return False
        except Exception as err:
            print(
                f"[DB] ❌ Erro inesperado no backup de {nome_arquivo}: {err}",
                file=__import__("sys").stderr,
            )
            return False
    
    def _limpar_backups_antigos(self, dias: int = 30):
        """Remove backups com mais de X dias."""
        if not self.backup_dir.exists():
            return
        
        limiar = datetime.now().timestamp() - (dias * 86400)
        
        for arquivo in self.backup_dir.rglob("*.json"):
            if arquivo.stat().st_mtime < limiar:
                arquivo.unlink()
        
        # Remover pastas vazias
        for pasta in self.backup_dir.iterdir():
            if pasta.is_dir() and not list(pasta.iterdir()):
                pasta.rmdir()
    
    # =========================================================================
    # AGENDAMENTOS
    # =========================================================================
    
    def carregar_agendamentos(self) -> List[dict]:
        """Retorna lista de agendamentos em cache."""
        return self._agendamentos or []
    
    def salvar_agendamento(self, agendamento: dict):
        """Salva novo agendamento."""
        self._fazer_backup("agendamentos.json")
        agendamento["id"] = gerar_id_agendamento(self._proximo_id_agendamento)
        self._proximo_id_agendamento += 1
        self._agendamentos.append(agendamento)
        self._escrever_json(self.arquivo_agendamentos, self._agendamentos)
    
    def atualizar_agendamento(self, id_agendamento: str, atualizacoes: dict):
        """Atualiza um agendamento existente."""
        self._fazer_backup("agendamentos.json")
        for agendamento in self._agendamentos:
            if agendamento["id"] == id_agendamento:
                agendamento.update(atualizacoes)
                agendamento["data_atualizacao"] = datetime.now().isoformat()
                break
        self._escrever_json(self.arquivo_agendamentos, self._agendamentos)
    
    def deletar_agendamento_logico(self, id_agendamento: str, motivo: str = ""):
        """Marca agendamento como cancelado (delete lógico)."""
        self._fazer_backup("agendamentos.json")
        for agendamento in self._agendamentos:
            if agendamento["id"] == id_agendamento:
                agendamento["status"] = "cancelado"
                agendamento["cancelado_em"] = datetime.now().isoformat()
                agendamento["motivo_cancelamento"] = motivo
                agendamento["data_atualizacao"] = datetime.now().isoformat()
                break
        self._escrever_json(self.arquivo_agendamentos, self._agendamentos)
    
    def obter_agendamento(self, id_agendamento: str) -> Optional[dict]:
        """Obtém um agendamento pelo ID."""
        for agendamento in self._agendamentos:
            if agendamento["id"] == id_agendamento:
                return agendamento
        return None
    
    # =========================================================================
    # PACIENTES
    # =========================================================================
    
    def carregar_pacientes(self) -> List[dict]:
        """Retorna lista de pacientes."""
        return self._pacientes or []
    
    def salvar_paciente(self, paciente_dict: dict) -> dict:
        """Salva novo paciente."""
        self._fazer_backup("pacientes.json")
        paciente_dict["id"] = self._proximo_id_paciente
        self._proximo_id_paciente += 1
        self._pacientes.append(paciente_dict)
        self._escrever_json(self.arquivo_pacientes, self._pacientes)
        return paciente_dict
    
    def obter_paciente_por_id(self, id_paciente: int) -> Optional[dict]:
        """Obtém paciente pelo ID."""
        for paciente in self._pacientes:
            if paciente["id"] == id_paciente:
                return paciente
        return None
    
    def obter_paciente_por_nome(self, nome: str) -> Optional[dict]:
        """Obtém paciente pelo nome (exato)."""
        for paciente in self._pacientes:
            if paciente["nome"].lower() == nome.lower():
                return paciente
        return None
    
    def atualizar_paciente(self, id_paciente: int, atualizacoes: dict):
        """Atualiza dados de um paciente."""
        self._fazer_backup("pacientes.json")
        for paciente in self._pacientes:
            if paciente["id"] == id_paciente:
                paciente.update(atualizacoes)
                break
        self._escrever_json(self.arquivo_pacientes, self._pacientes)
    
    # =========================================================================
    # PROFISSIONAIS
    # =========================================================================
    
    def carregar_profissionais(self) -> List[dict]:
        """Retorna lista de profissionais."""
        return self._profissionais or []
    
    def salvar_profissional(self, profissional_dict: dict) -> dict:
        """Salva novo profissional."""
        self._fazer_backup("profissionais.json")
        profissional_dict["id"] = self._proximo_id_profissional
        self._proximo_id_profissional += 1
        self._profissionais.append(profissional_dict)
        self._escrever_json(self.arquivo_profissionais, self._profissionais)
        return profissional_dict
    
    def obter_profissional(self, id_profissional: int) -> Optional[dict]:
        """Obtém profissional pelo ID."""
        for prof in self._profissionais:
            if prof["id"] == id_profissional:
                return prof
        return None
    
    # =========================================================================
    # ESPECIALIDADES
    # =========================================================================
    
    def carregar_especialidades(self) -> List[dict]:
        """Retorna lista de especialidades."""
        return self._especialidades or []
    
    def salvar_especialidade(self, especialidade_dict: dict) -> dict:
        """Salva nova especialidade."""
        self._fazer_backup("especialidades.json")
        especialidade_dict["id"] = self._proximo_id_especialidade
        self._proximo_id_especialidade += 1
        self._especialidades.append(especialidade_dict)
        self._escrever_json(self.arquivo_especialidades, self._especialidades)
        return especialidade_dict
    
    def obter_especialidade(self, id_especialidade: int) -> Optional[dict]:
        """Obtém especialidade pelo ID."""
        for esp in self._especialidades:
            if esp["id"] == id_especialidade:
                return esp
        return None
    
    # =========================================================================
    # UTILITÁRIOS
    # =========================================================================
    
    def recarregar(self):
        """Recarrega todos os dados do disco."""
        self._carregar_dados()
    
    def validar_integridade(self) -> bool:
        """
        Valida integridade dos dados.
        Retorna True se OK, False se houver problemas.
        """
        try:
            # Validar agendamentos
            for agendamento in self._agendamentos:
                assert agendamento.get("id"), "Agendamento sem ID"
                assert agendamento.get("data"), "Agendamento sem data"
                assert agendamento.get("hora"), "Agendamento sem hora"
                assert agendamento.get("status"), "Agendamento sem status"
            
            # Validar pacientes
            for paciente in self._pacientes:
                assert paciente.get("id"), "Paciente sem ID"
                assert paciente.get("nome"), "Paciente sem nome"
            
            # Validar profissionais
            for prof in self._profissionais:
                assert prof.get("id"), "Profissional sem ID"
                assert prof.get("nome"), "Profissional sem nome"
            
            # Validar especialidades
            for esp in self._especialidades:
                assert esp.get("id"), "Especialidade sem ID"
                assert esp.get("nome"), "Especialidade sem nome"
            
            return True
        except AssertionError as e:
            print(f"⚠️ Erro de integridade: {e}")
            return False
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do banco."""
        return {
            "total_agendamentos": len(self._agendamentos),
            "total_pacientes": len(self._pacientes),
            "total_profissionais": len(self._profissionais),
            "total_especialidades": len(self._especialidades),
        }
