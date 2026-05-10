# 🔧 CORREÇÕES PRONTAS PARA IMPLEMENTAÇÃO
## Problemas Críticos - Código Corrigido

---

## 🔴 CORREÇÃO #1: Variáveis Globais Não Definidas em main.py

### ❌ CÓDIGO ATUAL (QUEBRADO)
```python
# Linhas 257-273
def menu_consultar_paciente():
    """Menu para consultar histórico de paciente."""
    cabecalho("CONSULTAR PACIENTE")
    
    nome_busca = console.input("[bold green]Nome do paciente: [/bold green]").strip()
    
    if not nome_busca:
        exibir_erro("Nome não pode ser vazio")
        pausar()
        return
    
    # Busca fuzzy
    pacientes = paciente_service.db.carregar_pacientes()  # ❌ NÃO DEFINIDO
    resultados = busca_fuzzy_dict(nome_busca, pacientes, "nome", limiar=0.5)
    
    if not resultados:
        exibir_aviso("Nenhum paciente encontrado")
        pausar()
        return
    
    # Mostrar resultados
    items_display = [{"id": p["id"], "nome": f"{p['nome']} ({p['total_consultas']} consultas)"} for _, p in resultados]
    paciente_selecionado = selecionar_de_lista(items_display, "nome", "PACIENTES ENCONTRADOS")
    
    if not paciente_selecionado:
        return
    
    # Obter paciente completo
    paciente = paciente_service.obter_paciente(paciente_selecionado["id"])  # ❌ NÃO DEFINIDO
```

### ✅ CÓDIGO CORRIGIDO
```python
# Linhas 257-273
def menu_consultar_paciente() -> None:
    """Menu para consultar histórico de paciente."""
    if app is None:
        exibir_erro("Aplicação não inicializada")
        return
    
    cabecalho("CONSULTAR PACIENTE")
    
    nome_busca = console.input("[bold green]Nome do paciente: [/bold green]").strip()
    
    if not nome_busca:
        exibir_erro("Nome não pode ser vazio")
        pausar()
        return
    
    try:
        # Busca fuzzy
        pacientes = app.paciente_service.db.carregar_pacientes()  # ✅ CORRIGIDO
        resultados = busca_fuzzy_dict(nome_busca, pacientes, "nome", limiar=0.5)
        
        if not resultados:
            exibir_aviso("Nenhum paciente encontrado")
            pausar()
            return
        
        # Mostrar resultados
        items_display = [{"id": p["id"], "nome": f"{p['nome']} ({p['total_consultas']} consultas)"} for _, p in resultados]
        paciente_selecionado = selecionar_de_lista(items_display, "nome", "PACIENTES ENCONTRADOS")
        
        if not paciente_selecionado:
            return
        
        # Obter paciente completo
        paciente = app.paciente_service.obter_paciente(paciente_selecionado["id"])  # ✅ CORRIGIDO
```

### LINHAS A SUBSTITUIR
- Linha 265: `pacientes = paciente_service.db...` → `pacientes = app.paciente_service.db...`
- Linha 271: `paciente = paciente_service.obter_paciente...` → `paciente = app.paciente_service.obter_paciente...`
- Linha 277: `historico = paciente_service.obter_historico...` → `historico = app.paciente_service.obter_historico...`

---

## 🔴 CORREÇÃO #2: Implementar `formulario_reagendar_agendamento()` em ui.py

### ❌ CÓDIGO ATUAL (INCOMPLETO)
```python
def formulario_reagendar_agendamento() -> Optional[Dict]:
    """Coleta dados para reagendar um agendamento."""
    from modules.utils import converter_para_iso
    # ❌ FUNÇÃO TRUNCADA AQUI!
```

### ✅ CÓDIGO COMPLETO
```python
def formulario_reagendar_agendamento() -> Optional[Dict]:
    """
    Coleta dados para reagendar um agendamento.
    
    Returns:
        Dict com 'nova_data', 'nova_hora' e 'motivo', ou None se cancelar
    """
    from modules.utils import (
        converter_para_iso, data_valida, data_futura, dia_util, 
        hora_valida, hora_no_horario
    )
    
    cabecalho("REAGENDAR AGENDAMENTO")
    
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold blue]NOVA DATA E HORÁRIO[/bold blue]")
    console.print("[dim]Preencha os dados para reagendar o atendimento[/dim]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    # Nova data
    while True:
        data_input = console.input("[bold blue]Nova data (DD/MM/YYYY): [/bold blue]").strip()
        
        if data_input.lower() == "cancelar":
            exibir_aviso("Reagendamento cancelado")
            return None
        
        if not data_valida(data_input):
            exibir_erro("Data inválida. Use formato DD/MM/YYYY")
            continue
        
        if not data_futura(data_input):
            exibir_erro("A nova data deve ser no futuro")
            continue
        
        if not dia_util(data_input):
            exibir_erro("A clínica funciona apenas seg-sex")
            continue
        
        data = converter_para_iso(data_input)
        break
    
    # Novo horário
    while True:
        hora_input = console.input("[bold blue]Novo horário (HH:MM): [/bold blue]").strip()
        
        if hora_input.lower() == "cancelar":
            exibir_aviso("Reagendamento cancelado")
            return None
        
        if not hora_valida(hora_input):
            exibir_erro("Hora inválida. Use formato HH:MM")
            continue
        
        if not hora_no_horario(hora_input, "08:00", "18:00"):
            exibir_erro("Horário fora do intervalo (08:00-18:00)")
            continue
        
        hora = hora_input
        break
    
    # Motivo (opcional)
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold blue]MOTIVO DO REAGENDAMENTO (OPCIONAL)[/bold blue]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    motivo = console.input("[bold blue]Motivo: [/bold blue]").strip()
    
    return {
        "nova_data": data,
        "nova_hora": hora,
        "motivo": motivo
    }
```

---

## 🔴 CORREÇÃO #3: Implementar `selecionar_de_lista()` em ui.py

### ❌ CÓDIGO ATUAL (NÃO EXISTE)
```python
# Função é importada mas não existe!
from modules.ui import selecionar_de_lista  # ❌ ERRO: não definida
```

### ✅ CÓDIGO A ADICIONAR (ADICIONE AO FINAL DE ui.py)
```python
def selecionar_de_lista(
    items: List[dict],
    campo_exibicao: str,
    titulo: str = "SELEÇÃO"
) -> Optional[dict]:
    """
    Permite usuário selecionar um item de uma lista.
    
    Args:
        items: Lista de dicionários
        campo_exibicao: Chave do dicionário a exibir
        titulo: Título da seleção
    
    Returns:
        Dicionário selecionado ou None se cancelar
    """
    if not items:
        exibir_aviso("Nenhum item disponível")
        return None
    
    console.print(f"\n[bold blue]{titulo}[/bold blue]")
    
    for i, item in enumerate(items, 1):
        display = item.get(campo_exibicao, "?")
        console.print(f"  [bold blue]{i}[/bold blue] → {display}")
    
    console.print(f"  [bold red]{len(items) + 1}[/bold red] → Cancelar\n")
    
    while True:
        escolha_str = console.input("[bold blue]Escolha (número): [/bold blue]").strip()
        
        if escolha_str.isdigit():
            escolha = int(escolha_str) - 1
            
            # Cancelar
            if escolha == len(items):
                return None
            
            # Seleção válida
            if 0 <= escolha < len(items):
                return items[escolha]
        
        exibir_erro("Escolha inválida")
```

---

## 🔴 CORREÇÃO #4: Validação de Telefone em services.py

### ❌ CÓDIGO ATUAL (INCOMPLETO)
```python
# Linhas 85-91
def criar_agendamento(...):
    # ...
    # 0. Nome válido?
    if not nome_valido(paciente_nome):
        return False, "❌ Nome do paciente inválido...", None
    
    # 0.1 Email válido?
    if not email_valido(email):
        return False, "❌ Email inválido...", None
    
    # ❌ FALTA AQUI: Validação de telefone
```

### ✅ CÓDIGO CORRIGIDO
```python
# Linhas 85-95
def criar_agendamento(...):
    # ...
    # 0. Nome válido?
    if not nome_valido(paciente_nome):
        return False, "❌ Nome do paciente inválido (mín. 3 caracteres, sem números)", None
    
    # 0.1 Email válido?
    if not email_valido(email):
        return False, "❌ Email inválido. Use formato: exemplo@email.com", None
    
    # 0.2 Telefone válido?
    if not telefone_valido(telefone):  # ✅ ADICIONADO
        return False, "❌ Telefone inválido (mín. 10 dígitos)", None
    
    # ===== VALIDAÇÕES =====
```

---

## 🔴 CORREÇÃO #5: Try-Except em _fazer_backup() em database.py

### ❌ CÓDIGO ATUAL (SEM PROTEÇÃO)
```python
# Linhas 117-134
def _fazer_backup(self, nome_arquivo: str):
    """Faz backup de um arquivo antes de modificar."""
    caminho_original = self.dados_dir / nome_arquivo
    if not caminho_original.exists():
        return
    
    # Criar pasta do dia
    hoje = datetime.now().strftime("%Y-%m-%d")
    backup_dia = self.backup_dir / hoje
    backup_dia.mkdir(exist_ok=True)  # ❌ Sem try-except
    
    # Nome com timestamp
    timestamp = datetime.now().strftime("%H-%M-%S")
    nome_backup = f"{nome_arquivo.replace('.json', '')}_backup_{timestamp}.json"
    caminho_backup = backup_dia / nome_backup
    
    # Copiar arquivo
    shutil.copy2(caminho_original, caminho_backup)  # ❌ Sem try-except
    
    # Limpar backups antigos (> 30 dias)
    self._limpar_backups_antigos()
```

### ✅ CÓDIGO CORRIGIDO
```python
# Linhas 117-145
def _fazer_backup(self, nome_arquivo: str):
    """
    Faz backup de um arquivo antes de modificar.
    
    Não interrompe a operação principal se backup falhar.
    """
    try:
        caminho_original = self.dados_dir / nome_arquivo
        if not caminho_original.exists():
            return
        
        # Criar pasta do dia
        hoje = datetime.now().strftime("%Y-%m-%d")
        backup_dia = self.backup_dir / hoje
        
        try:
            backup_dia.mkdir(exist_ok=True, parents=True)
        except (OSError, PermissionError) as e:
            print(f"⚠️ Aviso: Não foi possível criar pasta de backup: {e}")
            return
        
        # Nome com timestamp
        timestamp = datetime.now().strftime("%H-%M-%S")
        nome_backup = f"{nome_arquivo.replace('.json', '')}_backup_{timestamp}.json"
        caminho_backup = backup_dia / nome_backup
        
        # Copiar arquivo
        try:
            shutil.copy2(caminho_original, caminho_backup)
        except (OSError, IOError, PermissionError) as e:
            print(f"⚠️ Aviso: Falha ao fazer backup de {nome_arquivo}: {e}")
            # Não interrompe operação principal
            return
        
        # Limpar backups antigos (> 30 dias)
        self._limpar_backups_antigos()
        
    except Exception as e:
        print(f"⚠️ Erro inesperado em _fazer_backup(): {e}")
        # Continua mesmo se backup falhar
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

Siga esta ordem para aplicar as correções:

### [ ] Fase 1 - Correções Críticas (2-3 horas)

1. [ ] **main.py** - Corrigir variáveis globais
   - Substituir `paciente_service` por `app.paciente_service` (linhas 257, 265, 271, 277)
   - Substituir `profissional_service` por `app.profissional_service` (linha 285)
   - Substituir `especialidade_service` por `app.especialidade_service` (linha 293)
   - Substituir `relatorio_service` por `app.relatorio_service` (linhas 302, 306, 318)

2. [ ] **ui.py** - Completar `formulario_reagendar_agendamento()`
   - Localizar função incompleta (final do arquivo)
   - Substituir pelo código completo acima

3. [ ] **ui.py** - Implementar `selecionar_de_lista()`
   - Adicionar função ao final de ui.py
   - Testar que é importada corretamente em main.py

4. [ ] **services.py** - Adicionar validação de telefone
   - Adicionar linhas 92-94 (validação de telefone)
   - Confirmar que `telefone_valido` é importado

5. [ ] **database.py** - Proteger `_fazer_backup()`
   - Substituir método `_fazer_backup()` (linhas 117-134)
   - Usar código corrigido com try-except

### [ ] Fase 2 - Testes

```bash
# No terminal, execute:
python run_tests.py

# Teste manual cada menu:
python main.py

# Testes específicos:
# - Novo Agendamento
# - Listar Agendamentos
# - Consultar Paciente
# - Gerenciar Profissionais
# - Gerenciar Especialidades
# - Relatórios
# - Reagendar Agendamento
```

### [ ] Fase 3 - Validação

- [ ] Todos os testes passam
- [ ] Nenhuma erro de `NameError` ou `AttributeError`
- [ ] Todos os menus funcionam
- [ ] Nenhuma mensagem de warning de backup

---

## 🚀 PRÓXIMAS CORREÇÕES (Após Fase 1)

Após implementar as correções críticas, implemente estas melhorias:

### [ ] Adicionar Type Hints
```python
# Exemplos:
def menu_consultar_paciente() -> None:
def menu_gerenciar_profissionais() -> None:
def menu_relatorios() -> None:
```

### [ ] Remover Duplicatas
```bash
# Deletar estes arquivos:
rm modules/audio_manager_backup_wav.py
rm modules/audio_manager_wav.py

# Manter apenas:
# modules/audio_manager.py
```

### [ ] Implementar Caching
Adicionar índices em `Database.__init__()` para buscas O(1)

### [ ] Logging
Importar `logging` e substituir `print()` por `logger.error()`

---

**Status:** 📋 Pronto para implementação  
**Prioridade:** 🔴 URGENTE  
**Tempo Estimado:** 2-3 horas
