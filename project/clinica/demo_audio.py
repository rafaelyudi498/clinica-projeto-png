#!/usr/bin/env python3
"""
demo_audio.py - Demonstração do sistema de áudio funcionando
"""

import time
import sys
from modules.ui import (
    cabecalho, exibir_sucesso, exibir_erro, 
    exibir_aviso, console, pausar
)
from modules.audio_manager import audio_manager

def demo():
    """Demonstra o sistema de áudio em ação."""
    
    # Boot
    print("\n" + "="*70)
    print("DEMONSTRAÇÃO DO SISTEMA DE ÁUDIO DA CLÍNICA")
    print("="*70)
    print("\n🎵 Sistema iniciando com som de boot...\n")
    audio_manager.reproduzir("boot")
    time.sleep(2)
    
    # Sucesso
    print("\n" + "-"*70)
    print("✅ DEMONSTRAÇÃO DE SUCESSO")
    print("-"*70)
    exibir_sucesso("Agendamento criado com sucesso!")
    time.sleep(2)
    
    # Erro
    print("\n" + "-"*70)
    print("❌ DEMONSTRAÇÃO DE ERRO")
    print("-"*70)
    exibir_erro("Email inválido fornecido")
    time.sleep(2)
    
    # Aviso
    print("\n" + "-"*70)
    print("⚠️ DEMONSTRAÇÃO DE AVISO")
    print("-"*70)
    exibir_aviso("Horário fora da disponibilidade")
    time.sleep(2)
    
    # Menu
    print("\n" + "-"*70)
    print("🔔 DEMONSTRAÇÃO DE MENU")
    print("-"*70)
    print("Som de menu será tocado ao escolher uma opção válida")
    print("(Este é apenas um aviso de demonstração)")
    audio_manager.reproduzir("menu")
    time.sleep(2)
    
    # Silenciar
    print("\n" + "-"*70)
    print("🔇 TESTANDO SILENCIAR")
    print("-"*70)
    audio_manager.silenciar()
    print("Audio silenciado")
    exibir_sucesso("Este som NÃO deve ser ouvido (audio silenciado)")
    time.sleep(1)
    
    # Ativar
    print("\n" + "-"*70)
    print("🔊 ATIVANDO AUDIO NOVAMENTE")
    print("-"*70)
    audio_manager.ativar()
    print("Audio ativado")
    exibir_sucesso("Este som DEVE ser ouvido (audio ativado)")
    time.sleep(2)
    
    # Conclusão
    print("\n" + "="*70)
    print("✅ DEMONSTRAÇÃO COMPLETADA!")
    print("="*70)
    print("\n📝 RESUMO:")
    print("  • Som de BOOT ao iniciar o sistema")
    print("  • Som de SUCESSO ao confirmar operações")
    print("  • Som de ERRO ao ocorrer problemas")
    print("  • Som de MENU ao selecionar opções")
    print("  • Opção de SILENCIAR no menu principal")
    print("\n🎵 Sistema de áudio funcionando perfeitamente!\n")

if __name__ == "__main__":
    demo()
