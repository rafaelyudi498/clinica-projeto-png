"""
utils.py — Funções auxiliares e utilitários

Contém funções puras para validação, formatação, busca fuzzy, etc.
Sem dependências de banco de dados ou UI.
"""

from datetime import datetime, date, timedelta
from difflib import SequenceMatcher
import re
from typing import List, Tuple, Optional


# ============================================================================
# VALIDAÇÕES DE DATA E HORA
# ============================================================================

def data_valida(data_str: str) -> bool:
    """Valida se string é uma data válida em formato DD/MM/YYYY ou YYYY-MM-DD."""
    try:
        # Tentar formato DD/MM/YYYY
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        try:
            # Tentar formato YYYY-MM-DD
            datetime.strptime(data_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False


def hora_valida(hora_str: str) -> bool:
    """Valida se string é uma hora válida em formato HH:MM."""
    try:
        datetime.strptime(hora_str, "%H:%M")
        return True
    except ValueError:
        return False


def data_futura(data_str: str) -> bool:
    """Verifica se data é futura (> hoje). Suporta DD/MM/YYYY ou YYYY-MM-DD."""
    if not data_valida(data_str):
        return False
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
    return data_obj > date.today()


def data_no_passado(data_str: str) -> bool:
    """Verifica se data é no passado (< hoje). Suporta DD/MM/YYYY ou YYYY-MM-DD."""
    if not data_valida(data_str):
        return False
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
    return data_obj < date.today()


def data_hoje_ou_futura(data_str: str) -> bool:
    """Verifica se data é hoje ou no futuro (>= hoje). Suporta DD/MM/YYYY ou YYYY-MM-DD."""
    if not data_valida(data_str):
        return False
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
    return data_obj >= date.today()


def dia_util(data_str: str) -> bool:
    """Verifica se data é dia útil (seg=1 até sex=5). Suporta DD/MM/YYYY ou YYYY-MM-DD."""
    if not data_valida(data_str):
        return False
    try:
        data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()
    dia_semana = data_obj.weekday()  # 0=seg, 6=dom
    return 0 <= dia_semana <= 4  # Segunda a Sexta


def hora_no_horario(hora_str: str, inicio: str, fim: str) -> bool:
    """Verifica se hora está dentro do intervalo [inicio, fim)."""
    if not (hora_valida(hora_str) and hora_valida(inicio) and hora_valida(fim)):
        return False
    
    h = datetime.strptime(hora_str, "%H:%M").time()
    h_inicio = datetime.strptime(inicio, "%H:%M").time()
    h_fim = datetime.strptime(fim, "%H:%M").time()
    
    return h_inicio <= h < h_fim


# ============================================================================
# CÁLCULOS DE HORÁRIO
# ============================================================================

def calcular_horario_fim(hora_inicio: str, intervalo_min: int = 60) -> str:
    """Calcula hora de término baseado em duração (default 1 hora)."""
    if not hora_valida(hora_inicio):
        return None
    
    h = datetime.strptime(hora_inicio, "%H:%M")
    h_fim = h + timedelta(minutes=intervalo_min)
    return h_fim.strftime("%H:%M")


def horarios_disponiveis(
    hora_inicio: str,
    hora_fim: str,
    intervalo_min: int = 60,
    agendamentos_dia: List[dict] = None
) -> List[str]:
    """
    Retorna lista de horários disponíveis em um dia.
    
    Exemplo:
        horarios_disponiveis("08:00", "18:00", 60, [])
        → ["08:00", "09:00", "10:00", ..., "17:00"]
    """
    if not (hora_valida(hora_inicio) and hora_valida(hora_fim)):
        return []
    
    agendamentos_dia = agendamentos_dia or []
    horarios_ocupados = {a["hora"] for a in agendamentos_dia if a["status"] != "cancelado"}
    
    horarios = []
    h = datetime.strptime(hora_inicio, "%H:%M")
    h_fim = datetime.strptime(hora_fim, "%H:%M")
    
    while h < h_fim:
        hora_str = h.strftime("%H:%M")
        if hora_str not in horarios_ocupados:
            horarios.append(hora_str)
        h += timedelta(minutes=intervalo_min)
    
    return horarios


# ============================================================================
# BUSCA FUZZY
# ============================================================================

def busca_fuzzy(
    termo: str,
    lista: List[str],
    limiar: float = 0.6
) -> List[Tuple[float, str]]:
    """
    Busca fuzzy em lista de strings.
    Retorna lista de tuples (score, valor) ordenada por score DESC.
    
    Exemplo:
        busca_fuzzy("joao", ["João Silva", "Pedro Costa"], 0.5)
        → [(0.85, "João Silva")]
    """
    termo_lower = termo.lower()
    resultados = []
    
    for item in lista:
        item_lower = item.lower()
        score = SequenceMatcher(None, termo_lower, item_lower).ratio()
        if score >= limiar:
            resultados.append((score, item))
    
    return sorted(resultados, key=lambda x: x[0], reverse=True)


def busca_fuzzy_dict(
    termo: str,
    lista: List[dict],
    campo: str,
    limiar: float = 0.6
) -> List[Tuple[float, dict]]:
    """
    Busca fuzzy em lista de dicionários.
    
    Exemplo:
        busca_fuzzy_dict("joao", pacientes, "nome", 0.6)
        → [(0.85, {id: 1, nome: "João Silva"})]
    """
    termo_lower = termo.lower()
    resultados = []
    
    for item in lista:
        valor = item.get(campo, "")
        valor_lower = str(valor).lower()
        score = SequenceMatcher(None, termo_lower, valor_lower).ratio()
        if score >= limiar:
            resultados.append((score, item))
    
    return sorted(resultados, key=lambda x: x[0], reverse=True)


# ============================================================================
# FORMATAÇÃO
# ============================================================================

def converter_para_iso(data_str: str) -> str:
    """Converte DD/MM/YYYY para YYYY-MM-DD (ISO 8601)."""
    if not data_str:
        return None
    try:
        dt = datetime.strptime(data_str, "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        # Se já está em YYYY-MM-DD, retorna como está
        if data_valida(data_str):
            return data_str
        return None


def converter_para_brasileiro(data_str: str) -> str:
    """Converte YYYY-MM-DD para DD/MM/YYYY."""
    if not data_str:
        return None
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        # Se já está em DD/MM/YYYY, retorna como está
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            return data_str
        except ValueError:
            return None


def formatar_data(data_str: str, formato: str = "%d/%m/%Y") -> str:
    """Converte YYYY-MM-DD para formato legível."""
    if not data_valida(data_str):
        return "Data inválida"
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d")
    except ValueError:
        dt = datetime.strptime(data_str, "%d/%m/%Y")
    return dt.strftime(formato)


def formatar_data_completa(data_str: str) -> str:
    """Converte para formato completo com dia da semana."""
    if not data_valida(data_str):
        return "Data inválida"
    dt = datetime.strptime(data_str, "%Y-%m-%d")
    dias = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    return f"{dias[dt.weekday()]}, {dt.strftime('%d/%m/%Y')}"


def formatar_hora(hora_str: str) -> str:
    """Formata hora com 'h' no final."""
    if not hora_valida(hora_str):
        return "Hora inválida"
    return f"{hora_str}h"


def formatar_datetime(dt_str: str) -> str:
    """Formata ISO 8601 para readable: '2026-05-05T14:30:00' → '05/05/2026 14:30'"""
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return "Data inválida"


# ============================================================================
# GERAÇÃO DE IDs
# ============================================================================

def gerar_id_agendamento(contador: int) -> str:
    """Gera ID sequencial para agendamento: AGD-2026-0001."""
    ano = datetime.now().year
    return f"AGD-{ano}-{contador:04d}"


# ============================================================================
# VALIDAÇÕES GENÉRICAS
# ============================================================================

def nao_vazio(texto: str) -> bool:
    """Verifica se string não é vazia ou só espaços."""
    return texto is not None and texto.strip() != ""


def nome_valido(nome: str) -> bool:
    """Validação básica de nome (mínimo 3 caracteres, sem números)."""
    if not nao_vazio(nome):
        return False
    nome = nome.strip()
    if len(nome) < 3:
        return False
    # Permite espaços e hífens, não permite números
    if any(c.isdigit() for c in nome):
        return False
    return True


def email_valido(email: str) -> bool:
    """Validação básica de email usando regex."""
    if not nao_vazio(email):
        return False
    # Padrão regex simples para email
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, email.strip()))


def telefone_valido(telefone: str) -> bool:
    """Validação básica de telefone (10 ou 11 dígitos, com opção de formatação)."""
    if not nao_vazio(telefone):
        return False
    # Remove espaços, hífens, parênteses e outros caracteres especiais
    telefone_limpo = re.sub(r"\D", "", telefone.strip())
    # Aceita 10 dígitos (formato 8 dígitos) ou 11 dígitos (celular com 9)
    return len(telefone_limpo) >= 10


def crp_valido(crp: str) -> bool:
    """Validação básica de CRP (ex: CRP 06/123456)."""
    if not nao_vazio(crp):
        return True  # Opcional
    # Formato esperado: CRP XX/XXXXXX
    return bool(re.match(r"CRP\s+\d{2}/\d{6}", crp))


# ============================================================================
# CONVERSÕES
# ============================================================================

def stringizar_lista_inteiros(lista: List[int], separador: str = ", ") -> str:
    """Converte [1, 2, 3] para '1, 2, 3'."""
    return separador.join(map(str, lista))


def dia_numero_para_nome(dia: int) -> str:
    """1 → 'segunda', 2 → 'terça', etc."""
    dias = {
        1: "segunda",
        2: "terça",
        3: "quarta",
        4: "quinta",
        5: "sexta",
        6: "sábado",
        7: "domingo"
    }
    return dias.get(dia, "dia desconhecido")


def dias_numeros_para_nomes(dias: List[int]) -> str:
    """[1, 2, 3] → 'seg, ter, qua'."""
    nomes_curtos = {1: "seg", 2: "ter", 3: "qua", 4: "qui", 5: "sex", 6: "sáb", 7: "dom"}
    return ", ".join(nomes_curtos.get(d, "?") for d in dias)


def dias_nomes_para_numeros(dias_nomes: List[str]) -> List[int]:
    """['segunda', 'terça'] → [1, 2]."""
    mapa = {
        "segunda": 1, "segunda-feira": 1, "seg": 1,
        "terça": 2, "terça-feira": 2, "ter": 2,
        "quarta": 3, "quarta-feira": 3, "qua": 3,
        "quinta": 4, "quinta-feira": 4, "qui": 4,
        "sexta": 5, "sexta-feira": 5, "sex": 5,
        "sábado": 6, "sab": 6,
        "domingo": 7, "dom": 7
    }
    resultado = []
    for dia in dias_nomes:
        num = mapa.get(dia.lower(), None)
        if num and num not in resultado:
            resultado.append(num)
    return sorted(resultado)


# ============================================================================
# COMPARAÇÕES E CONFLITOS
# ============================================================================

def horas_se_sobrepõem(h1_inicio: str, h1_fim: str, h2_inicio: str, h2_fim: str) -> bool:
    """Verifica se dois intervalos de hora se sobrepõem."""
    if not all(hora_valida(h) for h in [h1_inicio, h1_fim, h2_inicio, h2_fim]):
        return False
    
    h1_start = datetime.strptime(h1_inicio, "%H:%M").time()
    h1_end = datetime.strptime(h1_fim, "%H:%M").time()
    h2_start = datetime.strptime(h2_inicio, "%H:%M").time()
    h2_end = datetime.strptime(h2_fim, "%H:%M").time()
    
    return h1_start < h2_end and h2_start < h1_end
