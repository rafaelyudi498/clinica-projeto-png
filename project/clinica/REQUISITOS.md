# 📋 LEVANTAMENTO DE REQUISITOS - SISTEMA DE AGENDAMENTO DE CONSULTAS

## 1. IDENTIFICAÇÃO DO PROJETO

**Nome:** Sistema de Agendamento de Consultas - Clínica de Psicologia  
**Versão:** 1.0  
**Data:** Maio 2026  
**Status:** Em Desenvolvimento  

---

## 2. CONTEXTO DO NEGÓCIO

A clínica de psicologia necessita de um sistema para gerenciar agendamentos de consultas de forma eficiente, evitando conflitos de horário e mantendo histórico de atendimentos.

### 2.1 Problema Atual
- Agendamentos manuais (papel ou planilha)
- Risco de double-booking (múltiplos agendamentos no mesmo horário)
- Dificuldade em recuperar histórico de pacientes
- Falta de rastreabilidade de cancelamentos

### 2.2 Solução Proposta
Sistema integrado em terminal (Rich) com:
- Agendamento com validação de conflitos
- Histórico completo de pacientes
- Gerenciamento de múltiplos profissionais
- Relatórios de ocupação

---

## 3. USUÁRIOS DO SISTEMA

### 3.1 Operador (Recepção)
- **Responsabilidades:**
  - Agendar novas consultas
  - Listar agendamentos (dia/período)
  - Consultar histórico de paciente
  - Finalizar/cancelar agendamentos
  - Adicionar notas ao atendimento

- **Frequência de Uso:** 8 horas/dia (08:00 - 18:00)
- **Competências:** Básico em informática, treinamento necessário

---

## 4. FUNCIONALIDADES PRINCIPAIS

### 4.1 Módulo 1: Gerenciamento de Agendamentos

**RF-001: Listar Agendamentos**
- [ ] Listar agendamentos do dia atual
- [ ] Filtrar por data específica
- [ ] Filtrar por período (data início - data fim)
- [ ] Filtrar por profissional
- [ ] Mostrar status (confirmado, cancelado, concluído)
- Prioridade: **ALTA**

**RF-002: Criar Novo Agendamento**
- [ ] Solicitar: nome paciente, data, horário, profissional, tipo de consulta
- [ ] Validar conflitos de horário (mesmo profissional, mesmo horário)
- [ ] Validar se profissional está disponível (dias úteis: seg-sex)
- [ ] Validar horário dentro do intervalo (08:00-18:00)
- [ ] Impedir agendamentos retroativos (data ≥ hoje)
- [ ] Exibir mensagem de confirmação
- Prioridade: **ALTA**

**RF-003: Consultar Agendamentos por Paciente**
- [ ] Buscar por nome (parcial, case-insensitive)
- [ ] Mostrar todos os agendamentos (passados e futuros)
- [ ] Exibir histórico com notas
- [ ] Mostrar taxa de comparecimento
- Prioridade: **ALTA**

**RF-004: Finalizar/Cancelar Agendamento**
- [ ] Marcar como concluído
- [ ] Marcar como cancelado com motivo
- [ ] Adicionar notas de atendimento
- [ ] Atualizar status no banco de dados
- Prioridade: **ALTA**

**RF-005: Editar Agendamento**
- [ ] Permitir alteração de data/hora (se não conflitar)
- [ ] Permitir mudança de profissional
- [ ] Manter auditoria de alterações
- Prioridade: **MÉDIA**

### 4.2 Módulo 2: Gerenciamento de Profissionais

**RF-006: Cadastrar Profissional**
- [ ] Nome completo
- [ ] Especialidade(s)
- [ ] Horários disponíveis (padrão: 08:00-18:00)
- [ ] Dias de trabalho (padrão: seg-sex)
- Prioridade: **ALTA**

**RF-007: Listar Profissionais**
- [ ] Mostrar todos os profissionais
- [ ] Status (ativo/inativo)
- [ ] Especialidades
- Prioridade: **MÉDIA**

### 4.3 Módulo 3: Gerenciamento de Especialidades

**RF-008: Cadastrar Especialidades**
- [ ] Nome da especialidade
- [ ] Descrição (opcional)
- Prioridade: **MÉDIA**

### 4.4 Módulo 4: Relatórios

**RF-009: Relatório de Agendamentos do Dia**
- [ ] Data atual
- [ ] Todos os agendamentos confirmados
- [ ] Ordenado por horário
- [ ] Mostrar: horário, paciente, profissional, especialidade
- Prioridade: **MÉDIA**

**RF-010: Relatório por Período**
- [ ] Data início - Data fim
- [ ] Filtrar por profissional (opcional)
- [ ] Mostrar: total agendado, cancelado, concluído
- [ ] Taxa de ocupação
- Prioridade: **MÉDIA**

---

## 5. REQUISITOS NÃO-FUNCIONAIS

### 5.1 Performance
- [ ] Pesquisa de paciente < 1 segundo
- [ ] Carregamento de agendamentos < 2 segundos
- [ ] Validação de conflito < 500ms

### 5.2 Segurança
- [ ] Dados salvos em JSON (criptografia local opcional - v2)
- [ ] Sem acesso à internet (offline-first)
- [ ] Validação de entrada (SQL injection prevention)

### 5.3 Usabilidade
- [ ] Interface amigável em terminal (Rich)
- [ ] Feedback visual para ações
- [ ] Mensagens de erro claras
- [ ] Sistema de correção de ortografia (fuzzy match)
- [ ] Menu com "Voltar" em todas as telas

### 5.4 Confiabilidade
- [ ] Backup automático de dados JSON
- [ ] Validação de integridade de dados
- [ ] Recovery de inconsistências

### 5.5 Manutenibilidade
- [ ] Código limpo (PEP 8)
- [ ] Documentação inline
- [ ] Cobertura de testes ≥ 80%
- [ ] Separação de camadas (models, services, UI)

---

## 6. DETALHES FUNCIONAIS - ESPECIFICAÇÃO

### 6.1 Horário de Funcionamento
- **Horas:** 08:00 às 18:00
- **Dias Úteis:** Segunda a Sexta
- **Intervalo entre Consultas:** 1 hora

### 6.2 Dados Mínimos do Paciente
- **Nome** (obrigatório)
- Historicamente guardado com anotações

### 6.3 Dados de Consulta
- **ID** (UUID ou sequencial)
- **Paciente:** nome
- **Profissional:** nome
- **Especialidade:** tipo
- **Data:** YYYY-MM-DD
- **Hora:** HH:MM
- **Status:** agendado | concluído | cancelado
- **Notas:** texto livre
- **Data de Criação:** timestamp
- **Data de Alteração:** timestamp

### 6.4 Fluxo de Agendamento

```
1. Operador acessa menu principal
2. Escolhe "Novo Agendamento"
3. Sistema pede:
   - Nome do paciente (busca fuzzy em existentes)
   - Data desejada (validação: seg-sex, futuro)
   - Horário desejado (08:00-18:00)
   - Profissional (lista filtrada por disponibilidade)
   - Especialidade (lista filtrada por profissional)
   - Notas (opcional)
4. Sistema valida conflitos
5. Se OK → salva e exibe confirmação
6. Se conflito → mostra horários alternativos
```

### 6.5 Fluxo de Consulta de Paciente

```
1. Operador acessa "Consultar Paciente"
2. Digita nome (autocomplete fuzzy)
3. Sistema mostra todos os agendamentos do paciente
4. Exibe histórico completo com notas
5. Opção de ver detalhes de cada consulta
```

### 6.6 Fluxo de Finalizar/Cancelar

```
1. Operador acessa "Listar Agendamentos"
2. Seleciona um agendamento
3. Escolhe: "Finalizar" ou "Cancelar"
4. Se Finalizar:
   - Solicita notas do atendimento
   - Marca status como "concluído"
5. Se Cancelar:
   - Solicita motivo
   - Marca status como "cancelado"
6. Salva alterações
```

---

## 7. REQUISITOS DE INTERFACE (Rich)

### 7.1 Estilos
- Paleta retrô: **Verde no Preto** (como caixa_retro)
- Fonte: Terminal padrão
- Bordas: DOUBLE ou SIMPLE_HEAD
- Ícones: Unicode ✓, ✗, ⚠, ⏱

### 7.2 Componentes Principais
- **Menu Numerado:** opções interativas com validação
- **Tabelas:** agendamentos, profissionais, histórico
- **Painéis:** confirmações, avisos, erros
- **Progress Bar:** carregamento de dados
- **Spinner:** processamento

### 7.3 Fluxo de Navegação
```
Menu Principal
├── 1. Novo Agendamento → Formulário → Confirmação
├── 2. Listar Agendamentos → Tabela → Detalhes/Editar
├── 3. Consultar Paciente → Busca → Histórico
├── 4. Finalizar/Cancelar → Seleção → Formulário
├── 5. Gerenciar Profissionais → CRUD
├── 6. Relatórios → Menu Relatórios
│   ├── Agendamentos do Dia
│   └── Agendamentos por Período
└── 7. Sair

```

---

## 8. REQUISITOS DE PERSISTÊNCIA

### 8.1 Estrutura JSON
- **Arquivo 1:** `agendamentos.json` - todas as consultas
- **Arquivo 2:** `pacientes.json` - histórico de pacientes
- **Arquivo 3:** `profissionais.json` - base de profissionais
- **Arquivo 4:** `especialidades.json` - tipos de consulta

### 8.2 Backup
- Auto-backup antes de cada alteração
- Pasta: `dados/backup/`
- Padrão: `agendamentos_backup_YYYYMMDD_HHMMSS.json`

---

## 9. RESTRIÇÕES E LIMITAÇÕES

- ✅ **Sem banco de dados SQL** (usar JSON apenas)
- ✅ **Sem API/servidor** (offline, terminal local)
- ✅ **Sem multi-usuário** (1 operador por vez)
- ✅ **Sem autenticação** (confiança local)
- ⚠️ **Performance:** até 1000 agendamentos/ano

---

## 10. CRITÉRIO DE ACEIÇÃO

- [ ] Sistema liga sem erros
- [ ] Impede double-booking
- [ ] Busca de paciente funciona (fuzzy)
- [ ] Histórico completo visível
- [ ] Relatórios gerados corretamente
- [ ] Testes cobrem 80%+ do código
- [ ] Interface limpa e responsiva
- [ ] Backup automático funciona

---

## 11. ROADMAP PÓS-LANÇAMENTO (v2.0)

- [ ] Email/SMS de confirmação
- [ ] Criptografia de dados sensíveis
- [ ] Suporte a múltiplos operadores com login
- [ ] Integração com calendário (iCal)
- [ ] Relatórios em PDF
- [ ] Sistema de fila/waitlist
- [ ] Avaliação de satisfação
- [ ] Dashboard web (Django/FastAPI)

---

**Documento Assinado por:** Arquiteto de Software Sênior  
**Data de Aprovação:** Maio 2026  
**Versão:** 1.0
