# Sistema de Reagendamento - Documentação

## ✅ Implementações Realizadas

### 1. **Correção do Sistema de Áudio**

#### Problema Identificado
- O aviso estava reproduzindo o som de erro
- Sons de sucesso e erro podiam tocar simultaneamente, gerando conflito
- Menu sem opções válidas não deveria tocar nenhum som

#### Soluções Implementadas

**Em `modules/audio_manager.py`:**
- Adicionado sincronização com `threading.Lock()` e flag `_som_em_execucao`
- Apenas um som toca por vez, esperando o anterior terminar
- Evita sobreposição de áudio

**Em `modules/ui.py`:**
- Removido som de erro da função `exibir_aviso()` 
- Agora avisos não fazem barulho, apenas alertas visuais
- Mantém som de erro apenas para erros reais

---

### 2. **Sistema de Reagendamento de Consultas**

Permite que pacientes alterem data/horário de agendamentos confirmados sem precisar cancelar e remarcar.

#### Novas Funcionalidades em `modules/services.py`

**Método `reagendar_agendamento()`**
```python
def reagendar_agendamento(
    self,
    id_agendamento: str,
    nova_data: str,
    nova_hora: str,
    motivo: str = ""
) -> Tuple[bool, str, Optional[dict]]:
```

**Validações Incluídas:**
- ✅ Agendamento não pode estar concluído ou cancelado
- ✅ Nova data deve ser futura
- ✅ Nova data deve ser dia útil (seg-sex)
- ✅ Novo horário dentro do intervalo de funcionamento (08:00-18:00)
- ✅ Profissional disponível na nova data/hora
- ✅ Sem conflitos com outros agendamentos
- ✅ Horário compatível com agenda do profissional

**Método auxiliar `_verificar_conflito_excludente()`**
- Verifica disponibilidade do profissional
- Exclui o agendamento sendo reagendado da verificação
- Evita falsos positivos de conflito

#### Novas Funcionalidades em `modules/ui.py`

**Função `formulario_reagendar_agendamento()`**
- Coleta nova data (YYYY-MM-DD)
- Coleta novo horário (HH:MM)
- Coleta motivo (opcional)
- Retorna dicionário com dados validados

#### Integração em `main.py`

**Menu de Ações Expandido:**
- Opção 1: Finalizar agendamento
- Opção 2: Cancelar agendamento
- **Opção 3: Reagendar agendamento** (NOVO)
- Opção 4: Voltar

**Fluxo:**
1. Listar agendamentos (com filtros)
2. Selecionar agendamento
3. Escolher ação (incluindo "Reagendar")
4. Preencher novo período
5. Sistema valida e confirma com sucesso/erro

---

## 🔧 Melhorias Técnicas

### Sincronização de Áudio
```python
# Novo gerenciador com lock para evitar conflito
self._som_em_execucao = False
self._lock = threading.Lock()
```

### Tratamento de Erros Robusto
- Reagendamento mantém rastreabilidade com `motivo_reagendamento`
- Campo `data_atualizacao` registra quando foi alterado
- Validações impedem estados inconsistentes

### User Experience
- Aviso sem som reduz ruído da interface
- Reagendamento sem cancelar mantém histórico
- Mensagens claras indicam problema e solução

---

## 📋 Como Usar

### Reagendar um Agendamento

1. **Menu Principal** → Opção 2 (Listar Agendamentos)
2. Escolha filtro: Por data, por profissional ou todos
3. Selecione o agendamento na tabela
4. **Menu de Ação** → Opção 3 (Reagendar agendamento)
5. Informe:
   - Nova data (exemplo: 2026-05-15)
   - Novo horário (exemplo: 14:30)
   - Motivo (opcional - exemplo: "Conflito de trabalho")
6. Sistema confirma ou indica problema

---

## 🐛 Correções de Bugs

### Audio Manager
- ✅ Sincronização de threads
- ✅ Aviso sem som desnecessário
- ✅ Lock para evitar race conditions

### Menu
- ✅ Opção inválida toca erro e repete (não mais som duplo)
- ✅ Aviso informativo sem som

---

## 📊 Estrutura de Dados

Agendamento com novos campos:
```json
{
  "id": "AGD-2026-0001",
  "data": "2026-05-15",
  "hora": "14:30",
  "horario_fim": "15:30",
  "status": "confirmado",
  "motivo_reagendamento": "Conflito de trabalho",
  "data_atualizacao": "2026-05-10T10:30:00.000000",
  ...
}
```

---

## ✨ Benefícios

1. **Para Pacientes:** Flexibilidade para alterar consultas
2. **Para Clínica:** Menos cancelamentos/redúções
3. **Para Sistema:** Histórico completo e rastreável
4. **Interface:** Áudio mais limpo e previsível

---

## 🔄 Próximas Melhorias (Sugestões)

- Notificação automática de reagendamento (email/SMS)
- Limite de reagendamentos por paciente
- Dashboard de reagendamentos realizados
- Sincronização com calendário do profissional
- Relatório de motivos de reagendamento

