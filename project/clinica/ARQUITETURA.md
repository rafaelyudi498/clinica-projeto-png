# 🏗️ ARQUITETURA DO SISTEMA

## 1. VISÃO GERAL

O sistema segue uma arquitetura **em camadas** (Layered Architecture) com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────┐
│          INTERFACE (UI LAYER)                   │
│  modules/ui.py → Rich Components & Terminal    │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│       BUSINESS LOGIC (SERVICE LAYER)            │
│  modules/services.py → Regras de Negócio       │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│        DATA ACCESS (REPOSITORY LAYER)           │
│  modules/database.py → Leitura/Escrita JSON    │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│    PERSISTENCE (DATA LAYER)                     │
│  dados/*.json → Arquivos JSON                  │
└─────────────────────────────────────────────────┘
```

---

## 2. COMPONENTES E RESPONSABILIDADES

### 2.1 Layer 1: Presentation (UI)

**Arquivo:** `modules/ui.py`

**Responsabilidades:**
- Exibir menus no terminal (Rich)
- Capturar entrada do usuário
- Formatar saída em tabelas/painéis
- Validar dados de entrada (básico)
- Tratamento de erros para o usuário

**Funções Principais:**
```python
def cabecalho(titulo)
def menu_principal()
def menu_agendamentos()
def menu_consultar_paciente()
def formulario_novo_agendamento()
def listar_agendamentos_tabela(agendamentos)
def listar_paciente_historico(paciente, agendamentos)
def exibir_confirmacao(resultado)
def exibir_erro(mensagem)
```

**Dependências:**
- rich (Console, Panel, Table, etc.)
- services.py (apenas chamadas)

---

### 2.2 Layer 2: Business Logic (Services)

**Arquivo:** `modules/services.py`

**Responsabilidades:**
- Validação de regras de negócio
- Orquestração de operações
- Tratamento de conflitos
- Cálculos (datas, horários, etc.)
- Busca fuzzy

**Classes/Funções:**

```python
class AgendamentoService:
    def criar_agendamento(data, hora, paciente, prof_id, esp_id, notas)
    def listar_por_data(data)
    def listar_por_profissional(prof_id)
    def listar_por_paciente(nome)
    def editar_agendamento(id, **kwargs)
    def finalizar_agendamento(id, notas_atendimento)
    def cancelar_agendamento(id, motivo)
    def verificar_conflito(prof_id, data, hora)

class PacienteService:
    def buscar_por_nome(nome) → List[Paciente]
    def buscar_por_nome_fuzzy(nome, limiar) → List[Paciente]
    def criar_paciente(nome) → Paciente
    def obter_historico(paciente_id) → List[Agendamento]

class ProfissionalService:
    def listar_todos() → List[Profissional]
    def listar_por_especialidade(esp_id) → List[Profissional]
    def criar_profissional(nome, crp, especialidades, horarios)
    def validar_disponibilidade(prof_id, data, hora) → bool

class EspecialidadeService:
    def listar_todas() → List[Especialidade]
    def criar_especialidade(nome, descricao)

class RelatorioService:
    def relatorio_dia(data) → dict
    def relatorio_periodo(data_inicio, data_fim, prof_id=None) → dict
```

**Dependências:**
- database.py (read/write)
- models.py (data classes)
- utils.py (fuzzy, datas, etc.)

---

### 2.3 Layer 3: Data Access (Repository)

**Arquivo:** `modules/database.py`

**Responsabilidades:**
- Ler/escrever JSON
- Manter cache em memória
- Garantir integridade de dados
- Gerar backups automáticos
- Recuperação de erros

**Funções:**

```python
class Database:
    def __init__(self)
    def carregar_agendamentos() → List[dict]
    def salvar_agendamentos(agendamentos)
    def carregar_pacientes() → List[dict]
    def salvar_pacientes(pacientes)
    def carregar_profissionais() → List[dict]
    def salvar_profissionais(profissionais)
    def carregar_especialidades() → List[dict]
    def salvar_especialidades(especialidades)
    
    def fazer_backup(tipo) → bool
    def validar_integridade() → bool
    def recuperar_erro()
    
    @property
    def agendamentos_por_data(self) → dict
    @property
    def agendamentos_por_profissional(self) → dict
```

**Dependências:**
- json (Python stdlib)
- os, pathlib (Python stdlib)
- utils.py (validação, encoding)

---

### 2.4 Layer 4: Models (Data Structures)

**Arquivo:** `modules/models.py`

**Responsabilidades:**
- Definir estruturas de dados
- Type hints para o projeto

**Classes:**

```python
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Especialidade:
    id: int
    nome: str
    descricao: str
    ativo: bool
    data_criacao: str

@dataclass
class Profissional:
    id: int
    nome: str
    crp: Optional[str]
    especialidades: List[int]
    horario_inicio: str
    horario_fim: str
    dias_trabalho: List[int]
    ativo: bool
    data_criacao: str
    observacoes: Optional[str] = None

@dataclass
class Paciente:
    id: int
    nome: str
    data_primeiro_contato: str
    total_consultas: int
    ultima_consulta: Optional[str]
    status: str  # "ativo" | "inativo"
    observacoes: Optional[str] = None

@dataclass
class Agendamento:
    id: str
    data: str
    hora: str
    horario_fim: str
    paciente: dict  # {id, nome}
    profissional: dict  # {id, nome}
    especialidade: dict  # {id, nome}
    status: str  # "confirmado" | "concluido" | "cancelado"
    notas: str
    notas_atendimento: Optional[str]
    data_criacao: str
    data_atualizacao: str
    cancelado_em: Optional[str] = None
    motivo_cancelamento: Optional[str] = None
```

---

### 2.5 Layer 5: Utilities

**Arquivo:** `modules/utils.py`

**Responsabilidades:**
- Funções de data/hora
- Busca fuzzy
- Validações genéricas
- Formatações

**Funções:**

```python
def data_valida(data_str: str) -> bool
def hora_valida(hora_str: str) -> bool
def data_futura(data_str: str) -> bool
def dia_util(data_str: str) -> bool

def horarios_disponiveis(prof_id, data) -> List[str]
def calcular_horario_fim(hora_inicio: str, intervalo_min: int) -> str

def busca_fuzzy(termo: str, lista: List[str], limiar: float = 0.6) -> List[tuple]

def formatar_data(data_str: str) -> str  # YYYY-MM-DD → 10/05/2026
def formatar_hora(hora_str: str) -> str  # 10:00 → 10:00h
def gerar_id_agendamento() -> str  # AGD-2026-0001

def centralizar_texto(texto: str, largura: int) -> str
def criar_tabela_dados(dados: List[dict], colunas: List[str]) -> Table
```

---

### 2.6 Layer 6: Main Entry Point

**Arquivo:** `main.py`

**Responsabilidades:**
- Inicializar sistema
- Orquestrar fluxos principais
- Menu principal
- Tratamento de exceções top-level

**Estrutura:**

```python
def main():
    # 1. Inicializar banco de dados
    # 2. Exibir animação boot
    # 3. Menu loop
    
def menu_principal():
    while True:
        opcao = exibir_menu_principal()
        match opcao:
            case "1": menu_novo_agendamento()
            case "2": menu_listar_agendamentos()
            case "3": menu_consultar_paciente()
            case "4": menu_gerenciar_profissionais()
            case "5": menu_relatorios()
            case "6": return
```

---

## 3. FLUXOS DE DADOS

### 3.1 Fluxo: Novo Agendamento

```
┌─────────────────┐
│  UI.formulario  │ ← Usuário digita dados
└────────┬────────┘
         │
         ▼
┌──────────────────────────────┐
│ Validação Básica (UI Layer)  │ ← Formato, campos vazios
│ - Data válida?               │
│ - Hora válida?               │
│ - Nome paciente não vazio?   │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Service.criar_agendamento()  │ ← Regras de negócio
│ - Dia útil?                  │
│ - Horário dentro range?      │
│ - Prof tem especialidade?    │
│ - Conflito de horário?       │
└────────┬─────────────────────┘
         │
    Sem erro ▼
┌──────────────────────────────┐
│ Database.salvar()            │ ← Persistence
│ - Append em JSON             │
│ - Auto-increment ID          │
│ - Fazer backup               │
│ - Update cache               │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ UI.exibir_confirmacao()      │ ← Feedback ao usuário
│ Agendamento #AGD-2026-0001   │
│ confirmado com sucesso!      │
└──────────────────────────────┘
```

### 3.2 Fluxo: Consultar Paciente

```
┌──────────────────────┐
│ UI.input("Nome")     │ ← Usuário digita
└─────────┬────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│ Service.buscar_paciente_fuzzy()      │ ← Busca flexível
│ - SequenceMatcher (difflib)          │
│ - Retorna top 3 matches              │
└─────────┬────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│ UI.listar_resultados()               │ ← Menu para selecionar
│ 1. João Pereira (85% match)          │
│ 2. João Pedro (70% match)            │
│ 3. João Silva (68% match)            │
└─────────┬────────────────────────────┘
          │
          ▼ Usuário seleciona
┌──────────────────────────────────────┐
│ Service.obter_historico(paciente_id) │ ← Busca agendamentos
│ - Filter por paciente_id             │
│ - Order by data DESC                 │
└─────────┬────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│ UI.exibir_historico_tabela()         │ ← Mostra tabela
│ Data | Hora | Prof | Status | Notas │
└──────────────────────────────────────┘
```

---

## 4. ESTRUTURA DE PASTAS

```
clinica/
├── main.py                    # Entry point
├── requirements.txt           # Dependências
├── REQUISITOS.md             # Especificação funcional
├── BANCO_DADOS.md            # Design JSON
├── ARQUITETURA.md            # Este arquivo
│
├── modules/
│   ├── __init__.py
│   ├── models.py             # Dataclasses
│   ├── database.py           # Persistência
│   ├── services.py           # Lógica de negócio
│   ├── ui.py                 # Interface Rich
│   └── utils.py              # Funções auxiliares
│
├── dados/
│   ├── agendamentos.json     # Core data
│   ├── pacientes.json        # Histórico
│   ├── profissionais.json    # Cadastro profissionais
│   ├── especialidades.json   # Tipos de consulta
│   └── backup/               # Backups automáticos
│       └── YYYY-MM-DD/
│           └── *.json
│
├── tests/
│   ├── __init__.py
│   ├── test_services.py      # Testes unitários
│   ├── test_database.py      # Testes de persistência
│   ├── test_utils.py         # Testes de utilidades
│   └── test_integration.py   # Testes de integração
│
└── docs/
    ├── GUIA_USUARIO.md       # Manual do operador
    └── CHANGELOG.md          # Histórico de versões
```

---

## 5. PADRÕES DE DESIGN

### 5.1 Service Layer Pattern

```python
# Isolamento de lógica de negócio
class AgendamentoService:
    def __init__(self, db: Database):
        self.db = db
    
    def criar_agendamento(self, ...):
        # Validações
        # Orquestração
        # Chamadas ao DB
```

### 5.2 Repository Pattern

```python
# Abstração de persistência
class Database:
    def salvar_agendamento(self, agendamento):
        # Encapsula lógica de JSON
        # Permite trocar por SQL depois
```

### 5.3 Data Transfer Object (DTO)

```python
# Modelos para transferência entre camadas
@dataclass
class Agendamento:
    # Garante type safety
```

### 5.4 Factory Pattern

```python
def criar_agendamento_novo(...) -> Agendamento:
    """Factory method para criar novos agendamentos"""
    id = gerar_id_agendamento()
    timestamp = datetime.now().isoformat()
    return Agendamento(
        id=id,
        data_criacao=timestamp,
        ...
    )
```

---

## 6. DEPENDÊNCIAS E IMPORTS

```python
# main.py
from modules.ui import animar_boot, menu_principal
from modules.database import Database

# modules/ui.py
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from modules.services import AgendamentoService, PacienteService

# modules/services.py
from modules.database import Database
from modules.models import Agendamento, Paciente, Profissional
from modules.utils import busca_fuzzy, data_valida, verificar_conflito

# modules/database.py
import json
import os
from pathlib import Path
from datetime import datetime
from modules.models import Agendamento, Paciente
from modules.utils import validar_integridade

# modules/utils.py
from datetime import datetime, date, timedelta
from difflib import SequenceMatcher
import re
```

---

## 7. DECISÕES ARQUITETURAIS

| Decisão | Justificativa |
|---------|---------------|
| **Layered Architecture** | Clareza, manutenibilidade, testabilidade |
| **JSON em vez de SQL** | Requisito do cliente (offline-first) |
| **Cache em memória** | Performance para buscas frequentes |
| **Service Layer** | Isolação de regras de negócio |
| **Dataclasses** | Type hints nativos (Python 3.7+) |
| **Rich para UI** | Requerido, aparência retrô |
| **Sem frameworks web** | Terminal local, offline |

---

## 8. CONSIDERAÇÕES DE PERFORMANCE

### 8.1 Leitura/Escrita JSON

- **Problema:** Ler/escrever JSON inteiro a cada operação é lento
- **Solução:** Cache em memória durante sessão
- **Trade-off:** Uso de RAM vs velocidade

### 8.2 Busca de Pacientes

- **Problema:** Sem índices, busca linear é O(n)
- **Solução:** Pre-index nomes em lowercase
- **Resultado:** Busca O(1) em média

### 8.3 Verificação de Conflitos

- **Problema:** Iterar todos agendamentos é lento
- **Solução:** Índice por profissional + data
- **Performance:** < 100ms para 5000 registros

---

## 9. SEGURANÇA

- ✅ Validação de entrada (contra SQL injection, mesmo com JSON)
- ✅ Backup automático (recovery de falhas)
- ✅ Sem acesso à internet (offline)
- ✅ Sem autenticação (confiança local) - v1
- ⚠️ Sem criptografia (v2)
- ⚠️ Sem logs de auditoria (v2)

---

## 10. TESTABILIDADE

Cada layer é testável:

```python
# Test Service (sem UI, sem I/O)
def test_criar_agendamento_sucesso():
    service = AgendamentoService(mock_db)
    result = service.criar_agendamento(...)
    assert result.status == "confirmado"

# Test Database (com arquivos temporários)
def test_salvar_agendamento():
    db = Database(temp_dir)
    db.salvar_agendamento(agendamento)
    assert os.path.exists(temp_dir / "agendamentos.json")

# Test Utils (funções puras)
def test_data_valida():
    assert data_valida("2026-05-10") == True
    assert data_valida("2026-13-01") == False
```

---

**Arquitetura:** Layered 3-Tier  
**Versão:** 1.0  
**Autor:** Arquiteto de Software Sênior  
**Data:** Maio 2026
