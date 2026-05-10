# 🗄️ ESTRUTURA DO BANCO DE DADOS - JSON

## 1. OVERVIEW

A persistência será realizada através de 4 arquivos JSON principais, armazenados em `dados/`:

```
clinica/
├── dados/
│   ├── agendamentos.json      # Core: todas as consultas
│   ├── pacientes.json         # Histórico de pacientes
│   ├── profissionais.json     # Cadastro de profissionais
│   ├── especialidades.json    # Tipos de consulta
│   └── backup/                # Backups automáticos
├── modules/
│   ├── models.py              # Data classes
│   ├── database.py            # Funções de I/O JSON
│   ├── services.py            # Lógica de negócio
│   ├── ui.py                  # Interface Rich
│   └── utils.py               # Funções auxiliares
├── main.py
├── requirements.txt
└── tests/
```

---

## 2. ESTRUTURA JSON DETALHADA

### 2.1 `especialidades.json`

Registro de todas as especialidades disponíveis.

```json
[
  {
    "id": 1,
    "nome": "Psicanálise",
    "descricao": "Abordagem psicanalítica tradicional",
    "ativo": true,
    "data_criacao": "2026-05-05T10:00:00"
  },
  {
    "id": 2,
    "nome": "Terapia Cognitivo-Comportamental",
    "descricao": "TCC para ansiedade e depressão",
    "ativo": true,
    "data_criacao": "2026-05-05T10:00:00"
  },
  {
    "id": 3,
    "nome": "Terapia de Casal",
    "descricao": "Terapia para relacionamentos",
    "ativo": true,
    "data_criacao": "2026-05-05T10:00:00"
  }
]
```

**Campos:**
- `id`: Identificador único (int, auto-incremento)
- `nome`: Nome da especialidade (string, único)
- `descricao`: Descrição breve (string)
- `ativo`: Se está disponível para agendamento (bool)
- `data_criacao`: Timestamp de criação (ISO 8601)

---

### 2.2 `profissionais.json`

Cadastro de psicólogos e profissionais.

```json
[
  {
    "id": 1,
    "nome": "Dra. Maria Silva",
    "crp": "CRP 06/123456",
    "especialidades": [1, 2],
    "horario_inicio": "08:00",
    "horario_fim": "18:00",
    "dias_trabalho": [1, 2, 3, 4, 5],
    "ativo": true,
    "data_criacao": "2026-05-05T10:00:00",
    "observacoes": "Atende também online"
  },
  {
    "id": 2,
    "nome": "Dr. João Santos",
    "crp": "CRP 06/234567",
    "especialidades": [2, 3],
    "horario_inicio": "09:00",
    "horario_fim": "17:00",
    "dias_trabalho": [1, 2, 3, 4, 5],
    "ativo": true,
    "data_criacao": "2026-05-05T10:00:00",
    "observacoes": null
  }
]
```

**Campos:**
- `id`: Identificador único (int, auto-incremento)
- `nome`: Nome completo (string)
- `crp`: Registro profissional (string, opcional)
- `especialidades`: Lista de IDs de especialidades (array)
- `horario_inicio`: Hora de início (HH:MM)
- `horario_fim`: Hora de término (HH:MM)
- `dias_trabalho`: Dias disponíveis [1=seg, 2=ter, 3=qua, 4=qui, 5=sex] (array)
- `ativo`: Disponível para agendamento (bool)
- `data_criacao`: Timestamp (ISO 8601)
- `observacoes`: Notas adicionais (string, opcional)

---

### 2.3 `pacientes.json`

Histórico de pacientes (indexação rápida).

```json
[
  {
    "id": 1,
    "nome": "João Pereira",
    "data_primeiro_contato": "2026-05-05",
    "total_consultas": 5,
    "ultima_consulta": "2026-05-20",
    "status": "ativo",
    "observacoes": "Paciente assíduo"
  },
  {
    "id": 2,
    "nome": "Maria Costa",
    "data_primeiro_contato": "2026-04-15",
    "total_consultas": 2,
    "ultima_consulta": "2026-04-30",
    "status": "inativo",
    "observacoes": null
  }
]
```

**Campos:**
- `id`: Identificador único (int, auto-incremento)
- `nome`: Nome do paciente (string)
- `data_primeiro_contato`: Data do primeiro agendamento (YYYY-MM-DD)
- `total_consultas`: Contador de consultas (int)
- `ultima_consulta`: Data da última consulta (YYYY-MM-DD)
- `status`: "ativo" | "inativo" (string)
- `observacoes`: Notas gerais (string, opcional)

**Nota:** A verdadeira história é mantida em `agendamentos.json`

---

### 2.4 `agendamentos.json` (CORE)

Registro completo de todos os agendamentos.

```json
[
  {
    "id": "AGD-2026-0001",
    "data": "2026-05-10",
    "hora": "10:00",
    "horario_fim": "11:00",
    "paciente": {
      "id": 1,
      "nome": "João Pereira"
    },
    "profissional": {
      "id": 1,
      "nome": "Dra. Maria Silva"
    },
    "especialidade": {
      "id": 2,
      "nome": "Terapia Cognitivo-Comportamental"
    },
    "status": "confirmado",
    "notas": "Primeira consulta, paciente com ansiedade",
    "notas_atendimento": null,
    "data_criacao": "2026-05-05T14:30:00",
    "data_atualizacao": "2026-05-05T14:30:00",
    "cancelado_em": null,
    "motivo_cancelamento": null
  },
  {
    "id": "AGD-2026-0002",
    "data": "2026-05-10",
    "hora": "15:00",
    "horario_fim": "16:00",
    "paciente": {
      "id": 2,
      "nome": "Maria Costa"
    },
    "profissional": {
      "id": 2,
      "nome": "Dr. João Santos"
    },
    "especialidade": {
      "id": 3,
      "nome": "Terapia de Casal"
    },
    "status": "concluido",
    "notas": "Sessão com cônjuge",
    "notas_atendimento": "Abordado temas de comunicação. Resultado positivo.",
    "data_criacao": "2026-05-03T09:00:00",
    "data_atualizacao": "2026-05-10T16:30:00",
    "cancelado_em": null,
    "motivo_cancelamento": null
  },
  {
    "id": "AGD-2026-0003",
    "data": "2026-05-08",
    "hora": "14:00",
    "horario_fim": "15:00",
    "paciente": {
      "id": 1,
      "nome": "João Pereira"
    },
    "profissional": {
      "id": 1,
      "nome": "Dra. Maria Silva"
    },
    "especialidade": {
      "id": 1,
      "nome": "Psicanálise"
    },
    "status": "cancelado",
    "notas": "Agendamento confirmado",
    "notas_atendimento": null,
    "data_criacao": "2026-05-02T11:00:00",
    "data_atualizacao": "2026-05-07T09:00:00",
    "cancelado_em": "2026-05-07T09:00:00",
    "motivo_cancelamento": "Paciente solicitou cancelamento por questões pessoais"
  }
]
```

**Campos:**
- `id`: ID único (formato: AGD-YYYY-NNNN, ex: AGD-2026-0001)
- `data`: Data da consulta (YYYY-MM-DD)
- `hora`: Hora de início (HH:MM, 24h)
- `horario_fim`: Hora de término (HH:MM, calculado automaticamente)
- `paciente`: Object {id, nome}
- `profissional`: Object {id, nome}
- `especialidade`: Object {id, nome}
- `status`: "confirmado" | "concluido" | "cancelado"
- `notas`: Notas iniciais do agendamento (string)
- `notas_atendimento`: Anotações do atendimento (string, null se não concluído)
- `data_criacao`: Timestamp (ISO 8601)
- `data_atualizacao`: Timestamp (ISO 8601)
- `cancelado_em`: Timestamp de cancelamento (null se não cancelado)
- `motivo_cancelamento`: Razão do cancelamento (string, null)

---

## 3. REGRAS DE NEGÓCIO NA PERSISTÊNCIA

### 3.1 Validações no Carregamento

```python
def validar_integridade_dados():
    """
    ✓ Verifica se IDs de profissional/especialidade existem
    ✓ Valida formato de datas (YYYY-MM-DD)
    ✓ Valida formato de horas (HH:MM)
    ✓ Verifica consistência de timestamps
    ✓ Remove agendamentos duplicados
    ✓ Corrige status inconsistentes
    """
```

### 3.2 Prevenção de Conflitos

**Regra:** Nenhum profissional pode ter 2+ consultas no mesmo horário

```python
def verificar_conflito(profissional_id, data, hora):
    """
    Busca em agendamentos.json:
    - Mesma data
    - Mesma hora (ou sobreposição)
    - Status != "cancelado"
    """
```

### 3.3 Índices de Acesso Rápido

Para performance, cache em memória durante sessão:

```python
# Em memória (cache durante execução)
agendamentos_por_data = {}  # {data: [agendamentos]}
agendamentos_por_profissional = {}  # {prof_id: [agendamentos]}
pacientes_por_nome = {}  # {nome_lower: paciente}
```

---

## 4. OPERAÇÕES CRUD

### 4.1 CREATE (Novo Agendamento)

**Input:** {data, hora, paciente_nome, prof_id, esp_id, notas}  
**Output:** {id, confirmação}  
**Validações:**
1. Data ≥ hoje
2. Dia útil (seg-sex)
3. Hora entre 08:00-18:00
4. Sem conflito de profissional
5. Profissional tem especialidade

**Ações:**
1. Auto-increment ID
2. Append em agendamentos.json
3. Update pacientes.json (total_consultas++)
4. Backup automático

### 4.2 READ (Listar)

**Operações:**
- Todos agendamentos (com filtros opcionais)
- Por data
- Por profissional
- Por paciente
- Por status

**Performance:** < 2s para 1000 registros

### 4.3 UPDATE (Editar)

**Permitido:**
- Data/hora (se sem conflito)
- Profissional (se sem conflito)
- Status
- Notas
- Notas de atendimento

**Auditoria:** Sempre update `data_atualizacao`

### 4.4 DELETE (Lógico)

**Nunca deletar fisicamente!**  
Usar: status = "cancelado" + data_cancelamento

---

## 5. BACKUP E RECUPERAÇÃO

### 5.1 Estratégia de Backup

**Automático:**
- Antes de cada escrita em agendamentos.json
- Antes de cada escrita em pacientes.json
- Local: `dados/backup/YYYY-MM-DD/`

**Arquivo:** `agendamentos_backup_HH-MM-SS.json`

**Retenção:** Últimos 30 dias

### 5.2 Recovery

```python
def recuperar_backup(data, hora):
    """
    Permite restaurar para um ponto específico
    """
```

---

## 6. INICIALIZAÇÃO DO BANCO

### 6.1 Setup Inicial

Quando não existem arquivos:

1. Criar estrutura vazia
2. Adicionar especialidades padrão
3. Adicionar profissionais de teste (comentado)

```python
def inicializar_banco():
    criar_arquivo_vazio('especialidades.json')
    criar_arquivo_vazio('profissionais.json')
    criar_arquivo_vazio('pacientes.json')
    criar_arquivo_vazio('agendamentos.json')
```

---

## 7. EXEMPLOS DE QUERIES

### 7.1 "Listar agendamentos de hoje"

```python
hoje = date.today()
agendamentos_hoje = [
    a for a in agendamentos 
    if a['data'] == str(hoje) and a['status'] != 'cancelado'
]
```

### 7.2 "Buscar paciente por nome (fuzzy)"

```python
from difflib import SequenceMatcher

def buscar_paciente_fuzzy(nome_busca, limiar=0.6):
    resultado = []
    for p in pacientes:
        sim = SequenceMatcher(None, nome_busca.lower(), p['nome'].lower()).ratio()
        if sim >= limiar:
            resultado.append((sim, p))
    return sorted(resultado, reverse=True)
```

### 7.3 "Verificar conflito"

```python
def tem_conflito(prof_id, data, hora):
    return any(
        a['profissional']['id'] == prof_id and
        a['data'] == data and
        a['hora'] == hora and
        a['status'] != 'cancelado'
        for a in agendamentos
    )
```

---

## 8. LIMITAÇÕES E CONSIDERAÇÕES

- ⚠️ **Concorrência:** JSON não suporta lock. 1 operador por vez.
- ⚠️ **Escala:** JSON ótimo até ~5000 registros. Após, considerar SQLite.
- ✅ **Backup:** Essencial antes de v1.0 (dados críticos)
- ✅ **Validação:** Sempre validar ao carregar (dados corrompidos)

---

**Documento:** Estrutura de Banco de Dados  
**Versão:** 1.0  
**Autor:** Arquiteto de Software
