#!/usr/bin/env python3
"""
teste_audio.py - Script de teste para o sistema de áudio
"""

import time
import sys
from modules.audio_manager import audio_manager

print("\n" + "="*60)
print("  TESTE DO SISTEMA DE ÁUDIO")
print("="*60 + "\n")

# Teste 1: Som de boot
print("📢 Teste 1: SOM DE BOOT")
print("Deve tocar 3 notas ascendentes...\n")
audio_manager.reproduzir("boot")
time.sleep(2)

# Teste 2: Som de sucesso
print("\n📢 Teste 2: SOM DE SUCESSO")
print("Deve tocar 2 tons subindo...\n")
audio_manager.reproduzir("sucesso")
time.sleep(2)

# Teste 3: Som de erro
print("\n📢 Teste 3: SOM DE ERRO")
print("Deve tocar 2 tons descendo...\n")
audio_manager.reproduzir("erro")
time.sleep(2)

# Teste 4: Som de menu
print("\n📢 Teste 4: SOM DE MENU")
print("Deve tocar 1 tom simples...\n")
audio_manager.reproduzir("menu")
time.sleep(2)

# Teste 5: Silenciar
print("\n📢 Teste 5: SILENCIANDO")
audio_manager.silenciar()
print("Audio silenciado. Tentando reproduzir som...")
audio_manager.reproduzir("sucesso")
print("Nenhum som deve ter tocado.\n")
time.sleep(2)

# Teste 6: Ativar
print("\n📢 Teste 6: ATIVANDO")
audio_manager.ativar()
print("Audio ativado. Tentando reproduzir som...")
audio_manager.reproduzir("menu")
print("Som deve softer tocado.\n")
time.sleep(2)

print("\n" + "="*60)
print("  TESTES CONCLUÍDOS!")
print("="*60 + "\n")

print("✅ Se você ouviu todos os sons acima, o sistema está funcionando!")
print("❌ Se não ouviu, verifique:")
print("  - Volume do sistema")
print("  - Headphones/caixas de som conectados")
print("  - Permissões do Windows\n")
