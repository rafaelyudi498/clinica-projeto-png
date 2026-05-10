"""
main.py — Ponto de Entrada da Aplicação

Orquestra os menus principais e fluxos do sistema.
Utiliza padrão de container de dependências para injeção de services.
"""

from typing import Optional
from datetime import date

# Imports - Stdlib
# (nenhum adicional necessário)

# Imports - Third-party
# (nenhum adicional necessário)

# Imports - Local
from modules.database import Database
from modules.services import (
    AgendamentoService,
    PacienteService,
    ProfissionalService,
    EspecialidadeService,
    RelatorioService,
)
from modules.audio_manager import audio_manager
from modules.ui import (
    cabecalho,
    menu_opcoes,
    animacao_boot,
    exibir_erro,
    exibir_sucesso,
    exibir_aviso,
    pausar,
    console,
    linha_separadora,
    tabela_agendamentos,
    tabela_paciente_historico,
    tabela_profissionais,
    tabela_especialidades,
    formulario_novo_agendamento,
    formulario_finalizar_agendamento,
    formulario_cancelar_agendamento,
    formulario_reagendar_agendamento,
    selecionar_de_lista,
    exibir_relatorio_dia,
    exibir_relatorio_periodo,
    exibir_relatorio_agendamento,
)
from modules.utils import busca_fuzzy_dict


# =========================================================================
# CONSTANTES
# =========================================================================

DADOS_DIR: str = "dados"


# =========================================================================
# CONTAINER DE DEPENDÊNCIAS
# =========================================================================

class AppContext:
    """Container centralizado para todas as dependências da aplicação."""

    def __init__(self, dados_dir: str = DADOS_DIR) -> None:
        """
        Inicializa o contexto da aplicação.

        Args:
            dados_dir: Diretório onde os dados serão armazenados
        """
        self.db: Database = Database(dados_dir=dados_dir)
        self.agendamento_service: AgendamentoService = AgendamentoService(self.db)
        self.paciente_service: PacienteService = PacienteService(self.db)
        self.profissional_service: ProfissionalService = (
            ProfissionalService(self.db)
        )
        self.especialidade_service: EspecialidadeService = (
            EspecialidadeService(self.db)
        )
        self.relatorio_service: RelatorioService = RelatorioService(self.db)


# =========================================================================
# VARIÁVEL GLOBAL (Singleton)
# =========================================================================

app: Optional[AppContext] = None


# =========================================================================
# INICIALIZAÇÃO
# =========================================================================

def inicializar_sistema() -> AppContext:
    """
    Inicializa o sistema e retorna o contexto da aplicação.

    Returns:
        AppContext contendo todos os services inicializados
    """
    global app
    app = AppContext(dados_dir=DADOS_DIR)
    return app


# =========================================================================
# MENUS SECUNDÁRIOS
# =========================================================================

def menu_novo_agendamento() -> None:
    """Menu para criar novo agendamento com relatório final."""
    if app is None:
        exibir_erro("Aplicação não inicializada")
        return

    # Obter dados
    profissionais = app.profissional_service.listar_todos()
    especialidades = app.especialidade_service.listar_todas()
    pacientes_recentes = app.paciente_service.db.carregar_pacientes()[-10:]

    if not profissionais:
        exibir_erro("Nenhum profissional cadastrado")
        pausar()
        return

    if not especialidades:
        exibir_erro("Nenhuma especialidade cadastrada")
        pausar()
        return

    # Mostrar formulário otimizado
    dados = formulario_novo_agendamento(profissionais, especialidades, pacientes_recentes)

    if not dados:
        exibir_aviso("Agendamento cancelado")
        pausar()
        return

    # Criar agendamento (com validações no service)
    sucesso, mensagem, agendamento = app.agendamento_service.criar_agendamento(
        data=dados["data"],
        hora=dados["hora"],
        paciente_nome=dados["nome_paciente"],
        telefone=dados["telefone"],
        email=dados["email"],
        profissional_id=dados["profissional_id"],
        especialidade_id=dados["especialidade_id"],
        notas=dados["notas"],
    )

    if sucesso:
        # Obter dados do paciente para o relatório
        paciente = app.paciente_service.db.obter_paciente_por_nome(
            dados["nome_paciente"]
        )
        # Exibir relatório do agendamento
        exibir_relatorio_agendamento(agendamento, paciente)
    else:
        exibir_erro(mensagem)
        pausar()


def menu_listar_agendamentos() -> None:
    """Menu para listar agendamentos."""
    if app is None:
        exibir_erro("Aplicação não inicializada")
        return

    from modules.utils import converter_para_iso

    while True:
        cabecalho("LISTAR AGENDAMENTOS")
        opcao = menu_opcoes(
            ["Por data", "Por profissional", "Todos", "Voltar"], titulo="FILTRO"
        )

        agendamentos: list = []

        if opcao == "1":  # Por data
            data_input = console.input("[bold green]Data (DD/MM/YYYY): [/bold green]").strip()
            data = converter_para_iso(data_input)
            if not data:
                exibir_erro("Data inválida. Use o formato DD/MM/YYYY")
                pausar()
                continue
            agendamentos = app.agendamento_service.listar_por_data(data)

        elif opcao == "2":  # Por profissional
            profissionais = app.profissional_service.listar_todos()
            prof = selecionar_de_lista(profissionais, "nome", "SELECIONE PROFISSIONAL")
            if prof:
                agendamentos = app.agendamento_service.listar_por_profissional(prof["id"])

        elif opcao == "3":  # Todos
            agendamentos = app.agendamento_service.listar_agendamentos()

        elif opcao == "4":  # Voltar
            return

        # Exibir agendamentos
        cabecalho("AGENDAMENTOS")
        if agendamentos:
            console.print(tabela_agendamentos(agendamentos))
            linha_separadora()

            # Menu de ações
            acao = menu_opcoes(
                [
                    "Finalizar agendamento",
                    "Cancelar agendamento",
                    "Reagendar agendamento",
                    "Voltar",
                ],
                titulo="AÇÃO",
            )

            if acao == "1":  # Finalizar
                agend_selecionado = selecionar_de_lista(
                    agendamentos, "id", "SELECIONE AGENDAMENTO"
                )
                if agend_selecionado:
                    notas = formulario_finalizar_agendamento()
                    sucesso, msg = app.agendamento_service.finalizar_agendamento(
                        agend_selecionado["id"], notas
                    )
                    if sucesso:
                        exibir_sucesso(msg)
                    else:
                        exibir_erro(msg)

            elif acao == "2":  # Cancelar
                agend_selecionado = selecionar_de_lista(
                    agendamentos, "id", "SELECIONE AGENDAMENTO"
                )
                if agend_selecionado:
                    motivo = formulario_cancelar_agendamento()
                    sucesso, msg = app.agendamento_service.cancelar_agendamento(
                        agend_selecionado["id"], motivo
                    )
                    if sucesso:
                        exibir_sucesso(msg)
                    else:
                        exibir_erro(msg)

            elif acao == "3":  # Reagendar
                agend_selecionado = selecionar_de_lista(
                    agendamentos, "id", "SELECIONE AGENDAMENTO"
                )
                if agend_selecionado:
                    dados_reagendamento = formulario_reagendar_agendamento()
                    if dados_reagendamento:
                        sucesso, msg, agend_atualizado = (
                            app.agendamento_service.reagendar_agendamento(
                                agend_selecionado["id"],
                                dados_reagendamento["nova_data"],
                                dados_reagendamento["nova_hora"],
                                dados_reagendamento["motivo"],
                            )
                        )
                        if sucesso:
                            exibir_sucesso(msg)
                        else:
                            exibir_erro(msg)
                    else:
                        exibir_aviso("Reagendamento cancelado")
        else:
            exibir_aviso("Nenhum agendamento encontrado")

        pausar()


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
        pacientes = app.paciente_service.db.carregar_pacientes()
        resultados = busca_fuzzy_dict(nome_busca, pacientes, "nome", limiar=0.5)

        if not resultados:
            exibir_aviso("Nenhum paciente encontrado")
            pausar()
            return

        # Mostrar resultados
        items_display = [
            {
                "id": p["id"],
                "nome": f"{p['nome']} ({p['total_consultas']} consultas)",
            }
            for _, p in resultados
        ]
        paciente_selecionado = selecionar_de_lista(
            items_display, "nome", "PACIENTES ENCONTRADOS"
        )

        if not paciente_selecionado:
            return

        # Obter paciente completo
        paciente = app.paciente_service.obter_paciente(paciente_selecionado["id"])

        # Exibir histórico
        cabecalho(f"HISTÓRICO - {paciente['nome']}")

        historico = app.paciente_service.obter_historico(paciente["id"])

        if historico:
            console.print(tabela_paciente_historico(paciente, historico))
        else:
            exibir_aviso("Nenhum agendamento encontrado para este paciente")

        pausar()

    except Exception as err:
        exibir_erro(f"Erro ao consultar paciente: {err}")
        pausar()


def menu_gerenciar_profissionais() -> None:
    """Menu para visualizar profissionais."""
    if app is None:
        exibir_erro("Aplicação não inicializada")
        return

    cabecalho("GERENCIAR PROFISSIONAIS")
    profissionais = app.profissional_service.listar_todos()
    especialidades = app.especialidade_service.listar_todas()

    if profissionais:
        console.print(tabela_profissionais(profissionais, especialidades))
    else:
        exibir_aviso("Nenhum profissional cadastrado")

    pausar()


def menu_gerenciar_especialidades() -> None:
    """Menu para visualizar especialidades."""
    if app is None:
        exibir_erro("Aplicação não inicializada")
        return

    cabecalho("GERENCIAR ESPECIALIDADES")
    especialidades = app.especialidade_service.listar_todas()

    if especialidades:
        console.print(tabela_especialidades(especialidades))
    else:
        exibir_aviso("Nenhuma especialidade cadastrada")

    pausar()


def menu_relatorios() -> None:
    """Menu de relatórios."""
    if app is None:
        exibir_erro("Aplicação não inicializada")
        return

    from modules.utils import converter_para_iso

    while True:
        cabecalho("RELATÓRIOS")
        opcao = menu_opcoes(
            ["Agendamentos do dia", "Agendamentos por período", "Voltar"],
            titulo="RELATÓRIOS",
        )

        if opcao == "1":  # Do dia
            try:
                hoje = str(date.today())
                relatorio = app.relatorio_service.relatorio_dia(hoje)
                exibir_relatorio_dia(relatorio)
            except Exception as err:
                exibir_erro(f"Erro ao gerar relatório do dia: {err}")

        elif opcao == "2":  # Por período
            try:
                cabecalho("RELATÓRIO POR PERÍODO")

                data_inicio_input = console.input(
                    "[bold green]Data inicial (DD/MM/YYYY): [/bold green]"
                ).strip()
                data_fim_input = console.input(
                    "[bold green]Data final (DD/MM/YYYY): [/bold green]"
                ).strip()

                data_inicio = converter_para_iso(data_inicio_input)
                data_fim = converter_para_iso(data_fim_input)

                if not data_inicio or not data_fim:
                    exibir_erro(
                        "Uma ou ambas as datas estão inválidas. Use o formato DD/MM/YYYY"
                    )
                    pausar()
                    continue

                relatorio = app.relatorio_service.relatorio_periodo(
                    data_inicio, data_fim
                )

                if "erro" in relatorio:
                    exibir_erro(relatorio["erro"])
                else:
                    exibir_relatorio_periodo(relatorio)

            except Exception as err:
                exibir_erro(f"Erro ao gerar relatório por período: {err}")

        elif opcao == "3":  # Voltar
            return


# =========================================================================
# MENU PRINCIPAL
# =========================================================================

def menu_principal() -> None:
    """Menu principal do sistema."""
    while True:
        # Determinar status do áudio para exibição
        status_audio = "🔇 Silenciar" if audio_manager.is_ativo() else "🔊 Ativar Som"

        cabecalho()
        opcao = menu_opcoes(
            [
                "Novo Agendamento",
                "Listar Agendamentos",
                "Consultar Paciente",
                "Gerenciar Profissionais",
                "Gerenciar Especialidades",
                "Relatórios",
                status_audio,
                "Sair",
            ],
            titulo="MENU PRINCIPAL",
        )

        match opcao:
            case "1":
                menu_novo_agendamento()
            case "2":
                menu_listar_agendamentos()
            case "3":
                menu_consultar_paciente()
            case "4":
                menu_gerenciar_profissionais()
            case "5":
                menu_gerenciar_especialidades()
            case "6":
                menu_relatorios()
            case "7":
                # Toggle áudio
                novo_estado = audio_manager.toggle()
                status_msg = "ativado" if novo_estado else "silenciado"
                exibir_sucesso(f"Som {status_msg} com sucesso!")
                # Reproduzir som de confirmação se ativou
                if novo_estado:
                    audio_manager.reproduzir("sucesso")
            case "8":
                cabecalho("ENCERRANDO")
                console.print(
                    "\n[bold green]Sistema encerrado. Até logo![/bold green]\n"
                )
                break


# =========================================================================
# INICIALIZAÇÃO
# =========================================================================

if __name__ == "__main__":
    try:
        inicializar_sistema()
        animacao_boot()
        audio_manager.reproduzir("boot")
        menu_principal()
    except KeyboardInterrupt:
        console.print("\n[bold red]Sistema interrompido pelo usuário[/bold red]\n")
    except Exception as e:
        console.print(f"\n[bold red]ERRO CRÍTICO: {e}[/bold red]\n")
        import traceback
        traceback.print_exc()
