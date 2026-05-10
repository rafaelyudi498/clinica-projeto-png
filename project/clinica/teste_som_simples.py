#!/usr/bin/env python3
"""
teste_som_simples.py - Teste absoluto de som
"""

import winsound

print("\n" + "="*60)
print("TESTE SIMPLES DE SOM (WINSOUND PURO)")
print("="*60 + "\n")

print("⏳ Preparando para tocar som em 3 segundos...")
print("   Verifique se seu volume do Windows está LIGADO")
print("   Coloque headphones ou caixas de som perto\n")

import time
for i in range(3, 0, -1):
    print(f"   {i}...", end=" ", flush=True)
    time.sleep(1)
print("\n")

# Teste 1: Som de erro (baixo → alto)
print("🔊 TOCANDO: Som de erro (baixo para alto)")
print("   Deve soar como 'Lá → Dó' (descendo)\n")

try:
    # Som 1: Lá (440 Hz)
    print("   Primeira nota: 440 Hz (Lá)")
    winsound.Beep(440, 300)
    time.sleep(0.1)
    
    # Pausa
    time.sleep(0.2)
    
    # Som 2: Dó (262 Hz)
    print("   Segunda nota: 262 Hz (Dó)")
    winsound.Beep(262, 300)
    
    time.sleep(1)
    print("   ✅ Som de error tocado!\n")
except Exception as e:
    print(f"   ❌ ERRO: {e}\n")

# Teste 2: Som de sucesso (baixo → alto)
print("🔊 TOCANDO: Som de sucesso (baixo para alto)")
print("   Deve soar como 'Dó → Lá' (subindo)\n")

try:
    # Som 1: Dó (262 Hz)
    print("   Primeira nota: 262 Hz (Dó)")
    winsound.Beep(262, 300)
    time.sleep(0.1)
    
    # Pausa
    time.sleep(0.2)
    
    # Som 2: Lá (440 Hz)
    print("   Segunda nota: 440 Hz (Lá)")
    winsound.Beep(440, 300)
    
    time.sleep(1)
    print("   ✅ Som de sucesso tocado!\n")
except Exception as e:
    print(f"   ❌ ERRO: {e}\n")

# Teste 3: Som de menu
print("🔊 TOCANDO: Som de menu (tom único)")
print("   Deve soar como um 'toque' simples\n")

try:
    print("   Tocando: 800 Hz")
    winsound.Beep(800, 200)
    time.sleep(1)
    print("   ✅ Som de menu tocado!\n")
except Exception as e:
    print(f"   ❌ ERRO: {e}\n")

print("="*60)
print("✅ TESTES CONCLUÍDOS!")
print("="*60)
print("\n✓ Se você ouviu os 3 testes acima:")
print("  → O problema é com os arquivos WAV")
print("  → Vamos usar Beep() em vez de WAV\n")
