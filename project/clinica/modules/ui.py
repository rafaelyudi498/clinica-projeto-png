"""
ui.py — Camada de Apresentação (UI com Rich)

Todos os menus, formulários e exibições de dados.
Inspirado no style do caixa_retro.
"""

import time
from typing import List, Optional, Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.align import Align
from rich import box

from modules.utils import email_valido, telefone_valido, nome_valido, converter_para_iso, converter_para_brasileiro
from modules.audio_manager import audio_manager

# =========================================================================
# INICIALIZAÇÃO
# =========================================================================

console = Console()

# Paleta retrô: verde no preto (compatível com caixa_retro)
ESTILO_TITULO = "bold blue on black"
ESTILO_NORMAL = "blue on black"
ESTILO_AVISO = "bold yellow on black"
ESTILO_ERRO = "bold red on black"
ESTILO_SUCESSO = "bold bright_blue on black"


# =========================================================================
# UTILITÁRIOS DE TELA
# =========================================================================

def limpar_tela():
    """Limpa a tela do terminal."""
    console.clear()


def pausar():
    """Pausa e espera o usuário pressionar ENTER."""
    console.print("\n[dim blue]Pressione ENTER para continuar...[/dim blue]")
    input()


def cabecalho(titulo: str = "CLÍNICA DE PSICOLOGIA - SISTEMA DE AGENDAMENTO"):
    """Exibe o cabeçalho da aplicação."""
    limpar_tela()
    arte = Text()
    arte.append("███╗   ███╗ ███████╗ ███╗   ██╗ ████████╗███████╗     ███████╗     ██╗   ██╗ ██╗ ██████╗   █████╗ \n", style=ESTILO_TITULO)
    arte.append("████╗ ████║ ██╔════╝ ████╗  ██║ ╚══██╔══╝██╔════╝     ██╔════╝     ██║   ██║ ██║ ██╔══██╗ ██╔══██╗\n", style=ESTILO_TITULO)
    arte.append("██╔████╔██║ █████╗   ██╔██╗ ██║    ██║   █████╗       █████╗       ██║   ██║ ██║ ██║   ██║███████║\n", style=ESTILO_TITULO)
    arte.append("██║╚██╔╝██ ║██╔══╝   ██║╚██╗██║    ██║   ██╔══╝       ██╔══╝       ╚██╗ ██╔╝ ██║ ██║   ██║██╔══██║\n", style=ESTILO_TITULO)
    arte.append("██║ ╚═╝ ██║ ███████╗ ██║ ╚████║    ██║   ███████╗     ███████╗      ╚████╔╝  ██║ ██████╔╝ ██║  ██║\n", style=ESTILO_TITULO)
    arte.append("╚═╝     ╚═╝ ╚══════╝ ╚═╝  ╚═══╝    ╚═╝   ╚══════╝     ╚══════╝       ╚═══╝   ╚═╝ ╚═════╝  ╚═╝  ╚═╝\n", style=ESTILO_TITULO)
    console.print(Panel(Align.center(arte), border_style="blue", box=box.DOUBLE))
    console.print(
        Panel(f"[bold blue]{titulo}[/bold blue]",
              border_style="blue",
              box=box.SIMPLE_HEAD,
              expand=False),
        justify="center"
    )


def linha_separadora():
    """Exibe uma linha separadora."""
    console.rule(style="blue")


def animacao_boot():
    """Sequência de boot estilo terminal retrô."""
    limpar_tela()
    console.print("\n")
    etapas = [
        "Inicializando sistema...",
        "Carregando banco de dados...",
        "Verificando integridade de dados...",
        "Preparando interface...",
        "Sistema pronto.",
    ]
    with Progress(
        SpinnerColumn(style="blue"),
        TextColumn("[blue]{task.description}"),
        BarColumn(bar_width=40, style="blue", complete_style="bright_blue"),
        console=console,
        transient=True,
    ) as progress:
        tarefa = progress.add_task("Inicializando...", total=len(etapas))
        for etapa in etapas:
            progress.update(tarefa, description=etapa, advance=1)
            time.sleep(0.5)

    console.print(
        Panel("[bold bright_blue]  SISTEMA INICIALIZADO COM SUCESSO  [/bold bright_blue]",
              border_style="bright_blue", box=box.DOUBLE),
        justify="center"
    )
    time.sleep(1)


# =========================================================================
# MENSAGENS
# =========================================================================

def exibir_mensagem(texto: str, estilo: str = ESTILO_NORMAL):
    """Exibe uma mensagem."""
    console.print(f"[{estilo}]{texto}[/{estilo}]")


def exibir_erro(texto: str):
    """Exibe mensagem de erro."""
    console.print(f"[{ESTILO_ERRO}]❌ ERRO: {texto}[/{ESTILO_ERRO}]")
    audio_manager.reproduzir("erro")


def exibir_sucesso(texto: str):
    """Exibe mensagem de sucesso."""
    console.print(f"[{ESTILO_SUCESSO}]✅ {texto}[/{ESTILO_SUCESSO}]")
    audio_manager.reproduzir("sucesso")


def exibir_aviso(texto: str):
    """Exibe mensagem de aviso."""
    console.print(f"[{ESTILO_AVISO}]⚠️ AVISO: {texto}[/{ESTILO_AVISO}]")


# =========================================================================
# MENUS
# =========================================================================

def menu_opcoes(opcoes: List[str], titulo: str = "MENU") -> str:
    """
    Exibe menu numerado e retorna a escolha do usuário.
    
    Args:
        opcoes: Lista de opções (ex: ["Nova Venda", "Sair"])
        titulo: Título do menu
    
    Returns:
        String da opção escolhida (ex: "1", "2")
    """
    console.print(Panel(f"[bold blue]{titulo}[/bold blue]", border_style="blue", box=box.SQUARE))
    
    for i, opcao in enumerate(opcoes, 1):
        console.print(f"  [bold blue]{i}[/bold blue] → {opcao}")
    
    linha_separadora()
    
    while True:
        entrada = console.input("[bold blue]Escolha uma opção: [/bold blue]").strip()
        if entrada in [str(i) for i in range(1, len(opcoes) + 1)]:
            # Reproduzir som de menu ao selecionar (e se não for a opção "Sair")
            if entrada != str(len(opcoes)):  # Se não for última opção (geralmente "Sair")
                audio_manager.reproduzir("menu")
            return entrada
        exibir_erro(f"Opção '{entrada}' inválida")


# =========================================================================
# TABELAS
# =========================================================================

def tabela_agendamentos(agendamentos: List[dict]) -> Table:
    """Tabela formatada de agendamentos."""
    tabela = Table(
        title="[bold blue]AGENDAMENTOS[/bold blue]",
        box=box.SIMPLE_HEAD,
        border_style="blue",
        header_style="bold blue",
        show_lines=True,
    )
    tabela.add_column("DATA", style="dim blue", justify="center")
    tabela.add_column("HORA", style="blue", justify="center")
    tabela.add_column("PACIENTE", style="bright_blue", min_width=20)
    tabela.add_column("PROFISSIONAL", style="blue", min_width=20)
    tabela.add_column("ESPECIALIDADE", style="blue", min_width=20)
    tabela.add_column("STATUS", style="blue", justify="center")

    for agendamento in agendamentos:
        status_cor = (
            "[bright_blue]✓ Confirmado[/bright_blue]"
            if agendamento["status"] == "confirmado"
            else "[bright_yellow]✓ Concluído[/bright_yellow]"
            if agendamento["status"] == "concluido"
            else "[red]✗ Cancelado[/red]"
        )
        
        tabela.add_row(
            converter_para_brasileiro(agendamento["data"]),
            agendamento["hora"],
            agendamento["paciente"]["nome"],
            agendamento["profissional"]["nome"],
            agendamento["especialidade"]["nome"],
            status_cor,
        )
    
    return tabela


def tabela_paciente_historico(paciente: dict, agendamentos: List[dict]) -> Table:
    """Tabela do histórico de um paciente."""
    tabela = Table(
        title=f"[bold blue]HISTÓRICO - {paciente['nome'].upper()}[/bold blue]",
        box=box.SIMPLE_HEAD,
        border_style="blue",
        header_style="bold blue",
        show_lines=True,
    )
    tabela.add_column("ID", style="dim blue", justify="left", width=12)
    tabela.add_column("DATA", style="blue", justify="center")
    tabela.add_column("HORA", style="blue", justify="center")
    tabela.add_column("PROFISSIONAL", style="bright_blue", min_width=20)
    tabela.add_column("STATUS", style="blue", justify="center")
    tabela.add_column("NOTAS", style="dim blue", min_width=30)

    for agendamento in agendamentos:
        status_cor = (
            "[bright_blue]✓[/bright_blue]"
            if agendamento["status"] == "confirmado"
            else "[bright_yellow]✓[/bright_yellow]"
            if agendamento["status"] == "concluido"
            else "[red]✗[/red]"
        )
        
        notas = agendamento.get("notas_atendimento") or agendamento.get("notas", "-")
        notas = notas[:30] + "..." if len(notas) > 30 else notas
        
        tabela.add_row(
            agendamento["id"],
            converter_para_brasileiro(agendamento["data"]),
            agendamento["hora"],
            agendamento["profissional"]["nome"],
            status_cor,
            notas,
        )
    
    return tabela


def tabela_profissionais(profissionais: List[dict], especialidades: List[dict]) -> Table:
    """Tabela de profissionais."""
    tabela = Table(
        title="[bold blue]PROFISSIONAIS[/bold blue]",
        box=box.SIMPLE_HEAD,
        border_style="blue",
        header_style="bold blue",
        show_lines=True,
    )
    tabela.add_column("ID", style="dim blue", justify="center")
    tabela.add_column("NOME", style="bright_blue", min_width=20)
    tabela.add_column("ESPECIALIDADES", style="blue", min_width=30)
    tabela.add_column("HORÁRIO", style="blue", justify="center")
    tabela.add_column("DIAS", style="blue", justify="center")

    # Mapa de especialidades para busca rápida
    esp_map = {e["id"]: e["nome"] for e in especialidades}
    dias_nome = {1: "seg", 2: "ter", 3: "qua", 4: "qui", 5: "sex"}

    for prof in profissionais:
        esp_nomes = ", ".join(
            esp_map.get(esp_id, "?") for esp_id in prof.get("especialidades", [])
        )
        dias_work = ", ".join(
            dias_nome.get(d, "?") for d in prof.get("dias_trabalho", [])
        )
        
        tabela.add_row(
            str(prof["id"]),
            prof["nome"],
            esp_nomes,
            f"{prof['horario_inicio']}-{prof['horario_fim']}",
            dias_work,
        )
    
    return tabela


def tabela_especialidades(especialidades: List[dict]) -> Table:
    """Tabela de especialidades."""
    tabela = Table(
        title="[bold blue]ESPECIALIDADES[/bold blue]",
        box=box.SIMPLE_HEAD,
        border_style="blue",
        header_style="bold blue",
    )
    tabela.add_column("ID", style="dim blue", justify="center")
    tabela.add_column("NOME", style="bright_blue", min_width=25)
    tabela.add_column("DESCRIÇÃO", style="blue", min_width=40)

    for esp in especialidades:
        tabela.add_row(
            str(esp["id"]),
            esp["nome"],
            esp.get("descricao", ""),
        )
    
    return tabela


# =========================================================================
# FORMULÁRIOS
# =========================================================================

def formulario_novo_agendamento(
    profissionais: List[dict],
    especialidades: List[dict],
    pacientes_recentes: List[dict] = None
) -> Optional[Dict]:
    """
    Formulário otimizado para novo agendamento.
    - Escolhe especialidade PRIMEIRO
    - Filtra profissionais por especialidade
    - Permite voltar em qualquer etapa
    - Usa formato DD/MM/YYYY
    """
    cabecalho("NOVO AGENDAMENTO")
    
    # 1. ESPECIALIDADE
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold blue]1️⃣ ESCOLHA A ESPECIALIDADE[/bold blue]")
    console.print("[dim]A área de atendimento (ex: Psicologia Clínica, TCC, etc)[/dim]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    for i, esp in enumerate(especialidades, 1):
        console.print(f"  [bold blue]{i}[/bold blue] → {esp['nome']}")
        if esp.get('descricao'):
            console.print(f"     [dim]{esp['descricao']}[/dim]")
    console.print(f"  [bold red]{len(especialidades) + 1}[/bold red] → Cancelar agendamento\n")
    
    while True:
        esp_escolha_str = console.input("[bold blue]Escolha a especialidade (número): [/bold blue]").strip()
        if esp_escolha_str.isdigit():
            esp_escolha = int(esp_escolha_str) - 1
            if esp_escolha == len(especialidades):  # Cancelar
                return None
            if 0 <= esp_escolha < len(especialidades):
                especialidade_escolhida = especialidades[esp_escolha]
                esp_id = especialidade_escolhida["id"]
                break
        exibir_erro("Escolha inválida")
    
    # 2. PROFISSIONAL (filtrado por especialidade)
    profs_filtrados = [p for p in profissionais if esp_id in p.get("especialidades", [])]
    
    if not profs_filtrados:
        exibir_erro(f"Nenhum profissional disponível para {especialidade_escolhida['nome']}")
        pausar()
        return None
    
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold blue]2️⃣ ESCOLHA O PROFISSIONAL[/bold blue]")
    console.print(f"[dim]Profissional disponível para {especialidade_escolhida['nome']}[/dim]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    for i, prof in enumerate(profs_filtrados, 1):
        horario = f"{prof.get('horario_inicio', '08:00')}-{prof.get('horario_fim', '18:00')}"
        dias = " (Seg-Sex)" if set(prof.get('dias_trabalho', [])) == {1,2,3,4,5} else ""
        console.print(f"  [bold blue]{i}[/bold blue] → {prof['nome']} ({prof.get('crp', 'N/A')})")
        console.print(f"     [dim]Horário: {horario}{dias}[/dim]")
    console.print(f"  [bold red]{len(profs_filtrados) + 1}[/bold red] → Voltar\n")
    
    while True:
        prof_escolha_str = console.input("[bold blue]Escolha o profissional (número): [/bold blue]").strip()
        if prof_escolha_str.isdigit():
            prof_escolha = int(prof_escolha_str) - 1
            if prof_escolha == len(profs_filtrados):  # Voltar
                return formulario_novo_agendamento(profissionais, especialidades, pacientes_recentes)
            if 0 <= prof_escolha < len(profs_filtrados):
                prof_selecionado = profs_filtrados[prof_escolha]
                prof_id = prof_selecionado["id"]
                break
        exibir_erro("Escolha inválida")
    
    # 3. DATA DA CONSULTA
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold blue]3️⃣ ESCOLHA A DATA DA CONSULTA[/bold blue]")
    console.print("[dim]Data em que você deseja agendar (formato: DD/MM/YYYY)[/dim]")
    console.print("[dim]Exemplo: 15/05/2026 (segunda a sexta)[/dim]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    from modules.utils import data_valida, data_futura, dia_util, converter_para_iso
    
    while True:
        data_input = console.input("[bold blue]Data (DD/MM/YYYY): [/bold blue]").strip()
        
        if data_input.lower() == "voltar":
            return formulario_novo_agendamento(profissionais, especialidades, pacientes_recentes)
        
        if not data_valida(data_input):
            exibir_erro("Data inválida. Use formato DD/MM/YYYY (exemplo: 15/05/2026)")
            continue
        
        if not data_futura(data_input):
            exibir_erro("A data deve ser no futuro")
            continue
        
        if not dia_util(data_input):
            exibir_erro("A clínica funciona apenas de segunda a sexta")
            continue
        
        data = converter_para_iso(data_input)
        break
    
    # 4. HORÁRIO
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold blue]4️⃣ ESCOLHA O HORÁRIO[/bold blue]")
    console.print(f"[dim]Horário disponível para consulta (formato: HH:MM)[/dim]")
    console.print(f"[dim]Disponibilidade do(a) {prof_selecionado['nome']}: {prof_selecionado.get('horario_inicio', '08:00')}-{prof_selecionado.get('horario_fim', '18:00')}[/dim]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    from modules.utils import hora_valida, hora_no_horario
    
    while True:
        hora_input = console.input("[bold blue]Horário (HH:MM): [/bold blue]").strip()
        
        if hora_input.lower() == "voltar":
            return formulario_novo_agendamento(profissionais, especialidades, pacientes_recentes)
        
        if not hora_valida(hora_input):
            exibir_erro("Horário inválido. Use formato HH:MM (exemplo: 14:30)")
            continue
        
        if not hora_no_horario(hora_input, prof_selecionado.get('horario_inicio', '08:00'), prof_selecionado.get('horario_fim', '18:00')):
            exibir_erro(f"Horário fora da disponibilidade ({prof_selecionado.get('horario_inicio', '08:00')}-{prof_selecionado.get('horario_fim', '18:00')})")
            continue
        
        hora = hora_input
        break
    
    # 5. DADOS DO PACIENTE
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold blue]5️⃣ SEUS DADOS PESSOAIS[/bold blue]")
    console.print("[dim]Informações de contato para confirmação da consulta[/dim]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    # Nome do paciente
    while True:
        nome_paciente = console.input("[bold blue]Nome completo: [/bold blue]").strip()
        if nome_valido(nome_paciente):
            break
        exibir_erro("Nome deve ter no mínimo 3 caracteres (sem números)")
    
    # Telefone
    while True:
        telefone = console.input("[bold blue]Telefone (com DDD, ex: (11) 98765-4321): [/bold blue]").strip()
        if telefone_valido(telefone):
            break
        exibir_erro("Telefone inválido (mínimo 10 dígitos)")
    
    # Email
    while True:
        email = console.input("[bold blue]Email (ex: seu@email.com): [/bold blue]").strip()
        if email_valido(email):
            break
        exibir_erro("Email inválido (use formato: seu@email.com)")
    
    # 6. NOTAS (opcional)
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold blue]6️⃣ OBSERVAÇÕES (OPCIONAL)[/bold blue]")
    console.print("[dim]Qualquer informação adicional que o profissional precise saber[/dim]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    notas = console.input("[bold blue]Notas (deixe em branco se não houver): [/bold blue]").strip()
    
    return {
        "nome_paciente": nome_paciente,
        "telefone": telefone,
        "email": email,
        "data": data,
        "data_display": data_input,
        "hora": hora,
        "profissional_id": prof_id,
        "especialidade_id": esp_id,
        "notas": notas
    }


def formulario_finalizar_agendamento() -> str:
    """Coleta notas para finalizar agendamento."""
    console.print("[bold blue]Notas do atendimento (opcional):[/bold blue]")
    notas = console.input("[bold blue]>>> [/bold blue]").strip()
    return notas


def formulario_cancelar_agendamento() -> str:
    """Coleta motivo do cancelamento."""
    console.print("[bold blue]Motivo do cancelamento:[/bold blue]")
    motivo = console.input("[bold blue]>>> [/bold blue]").strip()
    return motivo


def formulario_reagendar_agendamento() -> Optional[Dict]:
    """Coleta dados para reagendar um agendamento."""
    from modules.utils import converter_para_iso
    
    cabecalho("REAGENDAR AGENDAMENTO")
    
    console.print("[bold blue]Insira os novos dados para reagendamento[/bold blue]\n")
    
    # Nova data
    while True:
        nova_data_input = console.input("[bold blue]Nova data (DD/MM/YYYY): [/bold blue]").strip()
        if nova_data_input:
            nova_data = converter_para_iso(nova_data_input)
            if nova_data:
                break
            exibir_erro("Data inválida. Use o formato DD/MM/YYYY")
        else:
            exibir_erro("Data não pode ser vazia")
    
    # Nova hora
    while True:
        nova_hora = console.input("[bold blue]Novo horário (HH:MM): [/bold blue]").strip()
        if nova_hora:
            break
        exibir_erro("Horário não pode ser vazio")
    
    # Motivo (opcional)
    motivo = console.input("[bold blue]Motivo do reagendamento (opcional): [/bold blue]").strip()
    
    return {
        "nova_data": nova_data,
        "nova_hora": nova_hora,
        "motivo": motivo
    }


def exibir_relatorio_agendamento(agendamento: dict, paciente: dict) -> None:
    """Exibe relatório detalhado do agendamento criado."""
    cabecalho("AGENDAMENTO CONFIRMADO")
    
    console.print("\n[bold bright_green]✅ Sua consulta foi agendada com sucesso![/bold bright_green]\n")
    
    # Criar tabela de confirmação
    tabela = Table(
        title="[bold blue]DADOS DO SEU AGENDAMENTO[/bold blue]",
        box=box.ROUNDED,
        border_style="blue",
        header_style="bold blue",
        show_lines=True
    )
    
    tabela.add_column("Campo", style="dim blue", width=20)
    tabela.add_column("Informação", style="bright_blue", min_width=40)
    
    # Adicionar linhas com os dados
    tabela.add_row("ID Agendamento", agendamento.get("id", "N/A"))
    tabela.add_row("Nome do Paciente", paciente.get("nome", "N/A"))
    tabela.add_row("Telefone", paciente.get("telefone", "N/A"))
    tabela.add_row("Email", paciente.get("email", "N/A"))
    
    tabela.add_row("[bold]Profissional[/bold]", agendamento["profissional"]["nome"])
    tabela.add_row("[bold]Especialidade[/bold]", agendamento["especialidade"]["nome"])
    
    tabela.add_row("[bold]Data da Consulta[/bold]", converter_para_brasileiro(agendamento["data"]))
    tabela.add_row("[bold]Horário[/bold]", f"{agendamento['hora']}h")
    tabela.add_row("[bold]Duração[/bold]", "1 hora")
    
    if agendamento.get("notas"):
        tabela.add_row("[bold]Observações[/bold]", agendamento["notas"])
    
    tabela.add_row("[bold]Status[/bold]", "[bright_green]Confirmado[/bright_green]")
    
    console.print(tabela)
    
    console.print("\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[yellow]📌 IMPORTANTE:[/yellow]")
    console.print("   • Chegue 10 minutos antes do horário agendado")
    console.print("   • Leve um documento de identificação")
    console.print("   • Em caso de impedimento, entre em contato para reagendar")
    console.print(f"   • Confirmaremos sua consulta via {paciente.get('email', 'email')}")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]\n")
    
    pausar()


# =========================================================================
# SELEÇÃO
# =========================================================================

def selecionar_de_lista(items: List[Dict], chave_display: str, titulo: str = "SELEÇÃO") -> Optional[Dict]:
    """
    Permite usuário selecionar um item de uma lista.
    
    Args:
        items: Lista de dicionários
        chave_display: Chave a usar para exibição (ex: "nome")
        titulo: Título da seleção
    
    Returns:
        Dict selecionado ou None
    """
    if not items:
        exibir_aviso("Nenhum item disponível")
        return None
    
    cabecalho(titulo)
    
    for i, item in enumerate(items, 1):
        display = item.get(chave_display, "?")
        console.print(f"  [bold blue]{i}[/bold blue] → {display}")
    
    linha_separadora()
    
    while True:
        escolha_str = console.input("[bold blue]Escolha um número: [/bold blue]").strip()
        if escolha_str.isdigit():
            escolha = int(escolha_str) - 1
            if 0 <= escolha < len(items):
                return items[escolha]
        exibir_erro("Opção inválida")


# =========================================================================
# RELATÓRIOS
# =========================================================================

def exibir_relatorio_dia(relatorio: Dict):
    """Exibe relatório do dia."""
    cabecalho(f"RELATÓRIO DO DIA - {relatorio['data']}")
    
    console.print(f"\n[bold blue]Total de agendamentos: {relatorio['total_agendamentos']}[/bold blue]")
    console.print(f"[bright_blue]Confirmados: {relatorio['confirmados']}[/bright_blue]")
    console.print(f"[yellow]Concluídos: {relatorio['concluidos']}[/yellow]")
    
    if relatorio["agendamentos"]:
        linha_separadora()
        console.print(tabela_agendamentos(relatorio["agendamentos"]))
    else:
        exibir_aviso("Nenhum agendamento para este dia")
    
    pausar()


def exibir_relatorio_periodo(relatorio: Dict):
    """Exibe relatório de período."""
    cabecalho(f"RELATÓRIO - {relatorio['periodo']}")
    
    console.print(f"\n[bold blue]Total de agendamentos: {relatorio['total']}[/bold blue]")
    console.print(f"[bright_blue]Confirmados: {relatorio['confirmados']}[/bright_blue]")
    console.print(f"[yellow]Concluídos: {relatorio['concluidos']}[/yellow]")
    console.print(f"[red]Cancelados: {relatorio['cancelados']}[/red]")
    console.print(f"[bold blue]Taxa de ocupação: {relatorio['taxa_ocupacao']}[/bold blue]")
    
    if relatorio["agendamentos"]:
        linha_separadora()
        console.print(tabela_agendamentos(relatorio["agendamentos"]))
    else:
        exibir_aviso("Nenhum agendamento neste período")
    
    pausar()
