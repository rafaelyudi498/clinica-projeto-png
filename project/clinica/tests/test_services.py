"""
test_services.py — Testes unitários para a camada de lógica de negócio

Testes dos services com mock de database.
"""

import unittest
import tempfile
import shutil
from datetime import datetime, date, timedelta
from pathlib import Path

from modules.database import Database
from modules.services import (
    AgendamentoService, PacienteService, ProfissionalService,
    EspecialidadeService, RelatorioService
)


class TestAgendamentoService(unittest.TestCase):
    """Testes do AgendamentoService."""
    
    @classmethod
    def setUpClass(cls):
        """Cria DB temporário para testes."""
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        """Remove DB temporário."""
        shutil.rmtree(cls.temp_dir)
    
    def setUp(self):
        """Prepara o DB antes de cada teste."""
        self.db = Database(dados_dir=self.temp_dir)
        self.service = AgendamentoService(self.db)
        
        # Criar especialidades e profissionais de teste
        self.esp_dict = self.db.salvar_especialidade({
            "nome": "Psicanálise",
            "descricao": "Terapia psicanalítica",
            "ativo": True,
            "data_criacao": datetime.now().isoformat()
        })
        
        self.prof_dict = self.db.salvar_profissional({
            "nome": "Dr. João",
            "crp": "CRP 06/123456",
            "especialidades": [self.esp_dict["id"]],
            "horario_inicio": "08:00",
            "horario_fim": "18:00",
            "dias_trabalho": [1, 2, 3, 4, 5],
            "ativo": True,
            "data_criacao": datetime.now().isoformat(),
            "observacoes": None
        })
    
    def test_criar_agendamento_sucesso(self):
        """Testa criação válida de agendamento."""
        amanha = (date.today() + timedelta(days=1)).isoformat()
        
        sucesso, msg, agendamento = self.service.criar_agendamento(
            data=amanha,
            hora="10:00",
            paciente_nome="João Silva",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas="Primeira consulta"
        )
        
        self.assertTrue(sucesso)
        self.assertIn("✅", msg)
        self.assertIsNotNone(agendamento)
        self.assertEqual(agendamento["status"], "confirmado")
    
    def test_criar_agendamento_data_invalida(self):
        """Testa criação com data inválida."""
        sucesso, msg, agendamento = self.service.criar_agendamento(
            data="data-invalida",
            hora="10:00",
            paciente_nome="João",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas=""
        )
        
        self.assertFalse(sucesso)
        self.assertIn("❌", msg)
        self.assertIsNone(agendamento)
    
    def test_criar_agendamento_data_passada(self):
        """Testa criação com data no passado."""
        ontem = (date.today() - timedelta(days=1)).isoformat()
        
        sucesso, msg, agendamento = self.service.criar_agendamento(
            data=ontem,
            hora="10:00",
            paciente_nome="João",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas=""
        )
        
        self.assertFalse(sucesso)
        self.assertIn("passado", msg)
    
    def test_criar_agendamento_dia_não_util(self):
        """Testa criação em fim de semana."""
        # 2026-05-09 é sábado
        sucesso, msg, agendamento = self.service.criar_agendamento(
            data="2026-05-09",
            hora="10:00",
            paciente_nome="João",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas=""
        )
        
        self.assertFalse(sucesso)
        self.assertIn("seg-sex", msg)
    
    def test_criar_agendamento_hora_invalida(self):
        """Testa criação com hora inválida."""
        amanha = (date.today() + timedelta(days=1)).isoformat()
        
        sucesso, msg, agendamento = self.service.criar_agendamento(
            data=amanha,
            hora="25:00",
            paciente_nome="João",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas=""
        )
        
        self.assertFalse(sucesso)
        self.assertIn("inválida", msg.lower())
    
    def test_criar_agendamento_hora_fora_horario(self):
        """Testa criação fora do horário de funcionamento."""
        amanha = (date.today() + timedelta(days=1)).isoformat()
        
        sucesso, msg, agendamento = self.service.criar_agendamento(
            data=amanha,
            hora="19:00",  # Após 18:00
            paciente_nome="João",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas=""
        )
        
        self.assertFalse(sucesso)
        self.assertIn("08:00-18:00", msg)
    
    def test_criar_agendamento_profissional_inexistente(self):
        """Testa criação com profissional inválido."""
        amanha = (date.today() + timedelta(days=1)).isoformat()
        
        sucesso, msg, agendamento = self.service.criar_agendamento(
            data=amanha,
            hora="10:00",
            paciente_nome="João",
            profissional_id=9999,  # ID inexistente
            especialidade_id=self.esp_dict["id"],
            notas=""
        )
        
        self.assertFalse(sucesso)
        self.assertIn("não encontrado", msg)
    
    def test_detectar_conflito(self):
        """Testa detecção de conflito de horário."""
        amanha = (date.today() + timedelta(days=1)).isoformat()
        
        # Criar primeiro agendamento
        sucesso1, msg1, agendamento1 = self.service.criar_agendamento(
            data=amanha,
            hora="10:00",
            paciente_nome="João",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas="Primeiro"
        )
        
        self.assertTrue(sucesso1)
        
        # Tentar criar segundo no mesmo horário
        sucesso2, msg2, agendamento2 = self.service.criar_agendamento(
            data=amanha,
            hora="10:00",
            paciente_nome="Maria",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas="Segundo"
        )
        
        self.assertFalse(sucesso2)
        self.assertIn("Conflito", msg2)
    
    def test_listar_agendamentos(self):
        """Testa listagem de agendamentos."""
        amanha = (date.today() + timedelta(days=1)).isoformat()
        
        self.service.criar_agendamento(
            data=amanha,
            hora="10:00",
            paciente_nome="João",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas=""
        )
        
        agendamentos = self.service.listar_agendamentos()
        self.assertGreater(len(agendamentos), 0)
    
    def test_listar_por_data(self):
        """Testa filtragem por data."""
        amanha = (date.today() + timedelta(days=1)).isoformat()
        
        self.service.criar_agendamento(
            data=amanha,
            hora="10:00",
            paciente_nome="João",
            profissional_id=self.prof_dict["id"],
            especialidade_id=self.esp_dict["id"],
            notas=""
        )
        
        agendamentos = self.service.listar_por_data(amanha)
        self.assertEqual(len(agendamentos), 1)
        self.assertEqual(agendamentos[0]["data"], amanha)


class TestPacienteService(unittest.TestCase):
    """Testes do PacienteService."""
    
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
    
    def setUp(self):
        self.db = Database(dados_dir=self.temp_dir)
        self.service = PacienteService(self.db)
    
    def test_buscar_por_nome_exato(self):
        """Testa busca exata de paciente."""
        self.db.salvar_paciente({
            "nome": "João Silva",
            "data_primeiro_contato": "2026-05-05",
            "total_consultas": 1,
            "ultima_consulta": "2026-05-05",
            "status": "ativo",
            "observacoes": None
        })
        
        resultado = self.service.buscar_por_nome("João Silva")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["nome"], "João Silva")
    
    def test_buscar_por_nome_fuzzy(self):
        """Testa busca fuzzy de paciente."""
        self.db.salvar_paciente({
            "nome": "João Silva",
            "data_primeiro_contato": "2026-05-05",
            "total_consultas": 1,
            "ultima_consulta": "2026-05-05",
            "status": "ativo",
            "observacoes": None
        })
        
        resultado = self.service.buscar_por_nome_fuzzy("joão", limiar=0.5)
        self.assertGreater(len(resultado), 0)


class TestRelatorioService(unittest.TestCase):
    """Testes do RelatorioService."""
    
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
    
    def setUp(self):
        self.db = Database(dados_dir=self.temp_dir)
        self.service = RelatorioService(self.db)
    
    def test_relatorio_dia(self):
        """Testa geração de relatório do dia."""
        hoje = date.today().isoformat()
        
        relatorio = self.service.relatorio_dia(hoje)
        
        self.assertIn("data", relatorio)
        self.assertIn("total_agendamentos", relatorio)
        self.assertEqual(relatorio["data"], hoje)
    
    def test_relatorio_periodo(self):
        """Testa geração de relatório por período."""
        data_inicio = (date.today() - timedelta(days=7)).isoformat()
        data_fim = date.today().isoformat()
        
        relatorio = self.service.relatorio_periodo(data_inicio, data_fim)
        
        self.assertIn("periodo", relatorio)
        self.assertIn("total", relatorio)
        self.assertIn("taxa_ocupacao", relatorio)


if __name__ == "__main__":
    unittest.main()
