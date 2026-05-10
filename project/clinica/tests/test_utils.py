"""
test_utils.py — Testes unitários para funções utilitárias

Testes de funções puras (sem dependências de BD ou UI).
"""

import unittest
from datetime import date, timedelta
from modules.utils import (
    data_valida, hora_valida, data_futura, data_no_passado, dia_util,
    hora_no_horario, calcular_horario_fim, busca_fuzzy, gerar_id_agendamento,
    nao_vazio, nome_valido, dias_numeros_para_nomes, horas_se_sobrepõem,
    formatar_data
)


class TestValidacaoDatas(unittest.TestCase):
    """Testes de validação de datas."""
    
    def test_data_valida_formato_correto(self):
        self.assertTrue(data_valida("2026-05-05"))
    
    def test_data_valida_formato_incorreto(self):
        self.assertFalse(data_valida("05/05/2026"))
        self.assertFalse(data_valida("2026-13-01"))
        self.assertFalse(data_valida("2026-05-32"))
    
    def test_data_futura(self):
        amanha = (date.today() + timedelta(days=1)).isoformat()
        self.assertTrue(data_futura(amanha))
        
        ontem = (date.today() - timedelta(days=1)).isoformat()
        self.assertFalse(data_futura(ontem))
    
    def test_data_no_passado(self):
        ontem = (date.today() - timedelta(days=1)).isoformat()
        self.assertTrue(data_no_passado(ontem))
        
        amanha = (date.today() + timedelta(days=1)).isoformat()
        self.assertFalse(data_no_passado(amanha))
    
    def test_dia_util(self):
        # 2026-05-05 é uma segunda-feira (dia útil)
        self.assertTrue(dia_util("2026-05-05"))
        
        # 2026-05-09 é um sábado (não útil)
        self.assertFalse(dia_util("2026-05-09"))
        
        # 2026-05-10 é um domingo (não útil)
        self.assertFalse(dia_util("2026-05-10"))


class TestValidacaoHoras(unittest.TestCase):
    """Testes de validação de horas."""
    
    def test_hora_valida_formato_correto(self):
        self.assertTrue(hora_valida("10:30"))
        self.assertTrue(hora_valida("00:00"))
        self.assertTrue(hora_valida("23:59"))
    
    def test_hora_valida_formato_incorreto(self):
        self.assertFalse(hora_valida("10-30"))
        self.assertFalse(hora_valida("25:00"))
        self.assertFalse(hora_valida("10:60"))
    
    def test_hora_no_horario(self):
        self.assertTrue(hora_no_horario("10:00", "08:00", "18:00"))
        self.assertTrue(hora_no_horario("08:00", "08:00", "18:00"))
        self.assertFalse(hora_no_horario("18:00", "08:00", "18:00"))
        self.assertFalse(hora_no_horario("19:00", "08:00", "18:00"))
    
    def test_calcular_horario_fim(self):
        self.assertEqual(calcular_horario_fim("10:00", 60), "11:00")
        self.assertEqual(calcular_horario_fim("14:30", 60), "15:30")
        self.assertEqual(calcular_horario_fim("09:00", 30), "09:30")


class TestBuscaFuzzy(unittest.TestCase):
    """Testes de busca fuzzy."""
    
    def test_busca_fuzzy_match_perfeito(self):
        lista = ["João Silva", "Maria Costa", "Pedro Santos"]
        resultado = busca_fuzzy("João Silva", lista, limiar=0.5)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0][1], "João Silva")
        self.assertGreater(resultado[0][0], 0.9)
    
    def test_busca_fuzzy_match_parcial(self):
        lista = ["João Silva", "Maria Costa", "João Pedro"]
        resultado = busca_fuzzy("joão", lista, limiar=0.5)
        self.assertEqual(len(resultado), 2)
    
    def test_busca_fuzzy_case_insensitive(self):
        lista = ["João Silva"]
        resultado = busca_fuzzy("JOÃO SILVA", lista, limiar=0.5)
        self.assertEqual(len(resultado), 1)
    
    def test_busca_fuzzy_sem_resultado(self):
        lista = ["João", "Maria", "Pedro"]
        resultado = busca_fuzzy("xyz", lista, limiar=0.8)
        self.assertEqual(len(resultado), 0)


class TestValidaçãoTexto(unittest.TestCase):
    """Testes de validação de texto."""
    
    def test_nao_vazio(self):
        self.assertTrue(nao_vazio("João"))
        self.assertFalse(nao_vazio(""))
        self.assertFalse(nao_vazio("   "))
        self.assertFalse(nao_vazio(None))
    
    def test_nome_valido(self):
        self.assertTrue(nome_valido("João Silva"))
        self.assertTrue(nome_valido("Maria-José"))
        self.assertFalse(nome_valido("Jo"))  # Muito curto
        self.assertFalse(nome_valido("João123"))  # Números
        self.assertFalse(nome_valido(""))


class TestGeracaoIds(unittest.TestCase):
    """Testes de geração de IDs."""
    
    def test_gerar_id_agendamento(self):
        id1 = gerar_id_agendamento(1)
        self.assertEqual(id1, "AGD-2026-0001")
        
        id100 = gerar_id_agendamento(100)
        self.assertEqual(id100, "AGD-2026-0100")
    
    def test_gerar_id_agendamento_padrao(self):
        id1 = gerar_id_agendamento(1)
        self.assertTrue(id1.startswith("AGD-"))
        self.assertTrue(len(id1) >= 10)


class TestComparacoes(unittest.TestCase):
    """Testes de comparações de horários."""
    
    def test_horas_se_sobrepõem_true(self):
        # 10:00-11:00 sobrepõe com 10:30-11:30
        self.assertTrue(horas_se_sobrepõem("10:00", "11:00", "10:30", "11:30"))
        
        # 10:00-11:00 é igual a 10:00-11:00
        self.assertTrue(horas_se_sobrepõem("10:00", "11:00", "10:00", "11:00"))
    
    def test_horas_se_sobrepõem_false(self):
        # 10:00-11:00 não sobrepõe com 11:00-12:00
        self.assertFalse(horas_se_sobrepõem("10:00", "11:00", "11:00", "12:00"))
        
        # 10:00-11:00 não sobrepõe com 09:00-10:00
        self.assertFalse(horas_se_sobrepõem("10:00", "11:00", "09:00", "10:00"))


class TestFormatacao(unittest.TestCase):
    """Testes de formatação."""
    
    def test_formatar_data(self):
        resultado = formatar_data("2026-05-05")
        self.assertEqual(resultado, "05/05/2026")
    
    def test_dias_numeros_para_nomes(self):
        resultado = dias_numeros_para_nomes([1, 2, 3])
        self.assertIn("seg", resultado)
        self.assertIn("ter", resultado)
        self.assertIn("qua", resultado)


if __name__ == "__main__":
    unittest.main()
