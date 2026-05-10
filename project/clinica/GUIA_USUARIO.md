# 📖 GUIA DO USUÁRIO - SISTEMA DE AGENDAMENTO

## 1. INICIALIZAÇÃO

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

### Executar o Sistema

```bash
python main.py
```

A primeira vez que executar, o sistema exibirá uma sequência de boot animada.

---

## 2. MENU PRINCIPAL

O menu principal oferece 7 opções:

```
MENU PRINCIPAL
  1 → Novo Agendamento
  2 → Listar Agendamentos
  3 → Consultar Paciente
  4 → Gerenciar Profissionais
  5 → Gerenciar Especialidades
  6 → Relatórios
  7 → Sair
```

---

## 3. NOVO AGENDAMENTO (Opção 1)

### Passo a Passo

1. **Nome do Paciente:** Digite o nome completo
   - Pacientes serão automaticamente cadastrados na primeira consulta
   - Nomes duplicados serão reconhecidos automaticamente

2. **Data:** Formato `YYYY-MM-DD` (ex: 2026-05-15)
   - Apenas datas futuras (não pode agendar para o passado)
   - Apenas dias úteis (segunda a sexta)

3. **Hora:** Formato `HH:MM` em 24h (ex: 14:30)
   - Intervalo: 08:00 a 18:00
   - Consultas têm duração de 1 hora

4. **Profissional:** Escolha da lista
   - Mostra apenas profissionais ativos
   - Considera horários e dias de trabalho

5. **Especialidade:** Escolha da lista
   - Filtrada por especialidades do profissional selecionado
   - Apenas especialidades ativas

6. **Notas (opcional):** Informações extras sobre o agendamento

### Validações Automáticas

- ✅ Impede agendamento em horários fora do funcionamento
- ✅ Impede conflito (double-booking)
- ✅ Valida se profissional trabalha neste dia/hora
- ✅ Valida se profissional oferece a especialidade

### Exemplo de Fluxo Bem-Sucedido

```
Nome do paciente: João Pereira
Data (YYYY-MM-DD): 2026-05-15
Hora (HH:MM): 10:00
ID do profissional: 1
ID da especialidade: 2
Notas (opcional): Primeira consulta com queixa de ansiedade

✅ Agendamento confirmado!
   João Pereira com Dra. Maria Silva (Terapia Cognitivo-Comportamental) em 2026-05-15 às 10:00h
```

---

## 4. LISTAR AGENDAMENTOS (Opção 2)

### Filtros Disponíveis

1. **Por Data:** Digite a data específica
   - Mostra agendamentos de um dia
   - Ordenado por horário

2. **Por Profissional:** Selecione de uma lista
   - Mostra todos os agendamentos do profissional
   - Ordenado por data/hora

3. **Todos:** Exibe todos os agendamentos não-cancelados
   - Incluindo confirmados e concluídos

### Ações nos Agendamentos

Uma vez listados, você pode:

- **Finalizar:** Marca como concluído e permite adicionar notas
- **Cancelar:** Marca como cancelado e requer motivo
- **Voltar:** Retorna ao menu de filtros

### Exemplo

```
AGENDAMENTOS
┌─────────────┬────────┬────────────┬──────────────────┬──────────────────┬──────────────┐
│ DATA        │ HORA   │ PACIENTE   │ PROFISSIONAL     │ ESPECIALIDADE    │ STATUS       │
├─────────────┼────────┼────────────┼──────────────────┼──────────────────┼──────────────┤
│ 2026-05-15  │ 10:00h │ João Silva │ Dra. Maria Silva │ Psicanálise      │ ✓ Confirmado │
│ 2026-05-15  │ 14:00h │ Maria C.   │ Dr. João Santos  │ Terapia de Casal │ ✓ Concluído  │
└─────────────┴────────┴────────────┴──────────────────┴──────────────────┴──────────────┘
```

---

## 5. CONSULTAR PACIENTE (Opção 3)

### Busca de Paciente

1. Digite o nome do paciente
2. Sistema busca com tolerância (fuzzy match)
3. Selecione de uma lista de resultados

### Histórico do Paciente

Exibe todos os agendamentos (passados e futuros):
- Data, horário, profissional, status
- Notas do agendamento e anotações de atendimento

### Exemplo

```
HISTÓRICO - JOÃO PEREIRA
┌──────────────┬──────────┬───────┬──────────────────┬──────────┬────────────────────────────┐
│ ID           │ DATA     │ HORA  │ PROFISSIONAL     │ STATUS   │ NOTAS                      │
├──────────────┼──────────┼───────┼──────────────────┼──────────┼────────────────────────────┤
│ AGD-2026-0002│ 2026-05-20│ 10:00│ Dra. Maria Silva │ ✓        │ Sessão produtiva. Paciente │
│ AGD-2026-0001│ 2026-05-10│ 10:00│ Dra. Maria Silva │ ✓        │ Primeira consulta...       │
└──────────────┴──────────┴───────┴──────────────────┴──────────┴────────────────────────────┘
```

---

## 6. GERENCIAR PROFISSIONAIS (Opção 4)

### Listar Profissionais

Mostra:
- ID, nome, especialidades, horário de trabalho, dias de trabalho

### Cadastrar Profissional

1. **Nome Completo:** ex: "Dra. Maria Silva"
2. **CRP (opcional):** ex: "CRP 06/123456"
3. **Especialidades:** Selecione várias (separadas por vírgula)
   - ex: `1,2,3`
4. **Horário:** Padrão 08:00-18:00 (configurável em v2)
5. **Dias:** Padrão segunda-sexta (configurável em v2)

### Exemplo

```
Nome completo: Dra. Maria Silva
CRP (opcional): CRP 06/123456
Selecione as especialidades (separadas por vírgula):
  1 → Psicanálise
  2 → Terapia Cognitivo-Comportamental
  3 → Terapia de Casal
IDs (ex: 1,2,3): 1,2

✅ Profissional Dra. Maria Silva cadastrado
```

---

## 7. GERENCIAR ESPECIALIDADES (Opção 5)

### Listar Especialidades

Mostra ID, nome e descrição de todas as especialidades ativas.

### Cadastrar Especialidade

1. **Nome:** ex: "Terapia Cognitivo-Comportamental"
2. **Descrição (opcional):** ex: "TCC para ansiedade e depressão"

### Exemplo

```
Nome: Terapia com Crianças
Descrição (opcional): Atendimento especializado para crianças de 4 a 12 anos

✅ Especialidade Terapia com Crianças cadastrada
```

---

## 8. RELATÓRIOS (Opção 6)

### Relatório do Dia

- Data: hoje
- Total de agendamentos
- Confirmados, concluídos, cancelados
- Lista completa de agendamentos

**Uso:** Verificar a agenda do dia de forma rápida

### Relatório por Período

- **Data Inicial e Final:** ex: 2026-05-01 a 2026-05-31
- **Profissional (opcional):** Pode filtrar por um profissional específico

**Mostra:**
- Total, confirmados, concluídos, cancelados
- **Taxa de ocupação:** % de agendamentos confirmados+concluídos
- Lista de agendamentos

**Uso:** Análise mensal, levantamento de ocupação, confirmação de agendamentos

---

## 9. DICAS E BOAS PRÁTICAS

### ✅ Recomendações

1. **Diariamente:**
   - Inicie o sistema
   - Consulte "Relatório do Dia"
   - Confirme ausências/cancelamentos

2. **Semanalmente:**
   - Verifique "Listar Agendamentos por Profissional"
   - Atualize notas de pacientes
   - Finalize agendamentos da semana anterior

3. **Mensalmente:**
   - Gere "Relatório por Período"
   - Analise taxa de ocupação
   - Identifique pacientes inativos

### ⚠️ Pontos de Atenção

- **Conflitos:** O sistema automaticamente impede double-booking
- **Fusos Horários:** Use sempre horário local (HH:MM 24h)
- **Nomes:** Busca é case-insensitive, mas aceita variações
- **Backup:** Sistema faz backup automático. Arquivos em `dados/backup/`

---

## 10. SOLUÇÃO DE PROBLEMAS

### "Agendamento não foi criado"

**Causas possíveis:**
- ❌ Data/hora em formato incorreto (use YYYY-MM-DD e HH:MM)
- ❌ Data no passado
- ❌ Fim de semana ou fora do horário
- ❌ Profissional já tem agendamento neste horário
- ❌ Profissional não oferece a especialidade

**Solução:** Verifique a mensagem de erro, corrija o dado e tente novamente.

### "Profissional não encontrado"

**Causa:** Profissional não foi cadastrado ou está inativo.

**Solução:** Vá em "Gerenciar Profissionais" → "Cadastrar profissional"

### "Nenhum agendamento encontrado"

**Possível:** Não há agendamentos para os filtros especificados.

**Solução:** Tente mudar o filtro ou criar novos agendamentos.

---

## 11. ATALHOS E COMANDOS

| Ação | Resultado |
|------|-----------|
| Pressione `Ctrl+C` | Sai do sistema imediatamente |
| Digite um número inválido | Sistema pede para repetir |
| Digite nome de paciente incompleto | Busca fuzzy encontra possibilidades |
| Cancelar agendamento futuro | Status muda para "cancelado" (não deleta) |

---

## 12. DADOS E BACKUP

### Localização dos Dados

```
clinica/
├── dados/
│   ├── agendamentos.json      (Consultas agendadas)
│   ├── pacientes.json         (Histórico de pacientes)
│   ├── profissionais.json     (Cadastro profissionais)
│   ├── especialidades.json    (Tipos de consulta)
│   └── backup/                (Backups automáticos)
```

### Backup Automático

- Realizado antes de cada alteração
- Mantém últimos 30 dias
- Localização: `dados/backup/YYYY-MM-DD/`

### Restaurar de Backup

Contate o suporte técnico para recuperar dados de uma data anterior.

---

**Versão:** 1.0  
**Data:** Maio 2026  
**Suporte:** Consulte a documentação técnica (REQUISITOS.md, BANCO_DADOS.md, ARQUITETURA.md)
