"""
audio_manager.py — Gerenciador de Áudio SIMPLES

Usa winsound.Beep() para máxima compatibilidade.
Sem dependências de numpy/scipy ou arquivos WAV.
"""

import sys
import winsound
import threading
import time


class AudioManager:
    """Gerenciador de áudio usando winsound.Beep()."""
    
    def __init__(self):
        """Inicializa gerenciador."""
        self.ativo = True
        print(f"[AUDIO] AudioManager inicializado (modo: Beep)", file=sys.stderr)
    
    def reproduzir(self, tipo_som: str):
        """Reproduz som usando Beep."""
        if not self.ativo:
            print(f"[AUDIO] Audio desativado - ignorando {tipo_som}", file=sys.stderr)
            return
        
        print(f"[AUDIO] Reproduzindo: {tipo_som}", file=sys.stderr)
        
        # Executar em thread para não bloquear
        thread = threading.Thread(
            target=self._tocar_som,
            args=(tipo_som,),
            daemon=True
        )
        thread.start()
    
    @staticmethod
    def _tocar_som(tipo_som: str):
        """Toca som usando winsound.Beep()."""
        try:
            print(f"[AUDIO THREAD] Tocando {tipo_som}...", file=sys.stderr)
            
            if tipo_som == "sucesso":
                # Dó (262 Hz) → Lá (440 Hz) ascendente
                winsound.Beep(262, 300)  # 300ms
                time.sleep(0.1)
                winsound.Beep(440, 300)
            
            elif tipo_som == "erro":
                # Lá (440 Hz) → Dó (262 Hz) descendente
                winsound.Beep(440, 300)
                time.sleep(0.1)
                winsound.Beep(262, 300)
            
            elif tipo_som == "menu":
                # Tom único (800 Hz)
                winsound.Beep(800, 200)
            
            elif tipo_som == "boot":
                # Sequência: Dó (262) → Mi (330) → Lá (440)
                winsound.Beep(262, 200)
                time.sleep(0.05)
                winsound.Beep(330, 200)
                time.sleep(0.05)
                winsound.Beep(440, 200)
            
            print(f"[AUDIO THREAD] ✅ TOCADO: {tipo_som}", file=sys.stderr)
            
        except Exception as e:
            print(f"[AUDIO ERRO] {tipo_som}: {e}", file=sys.stderr)
    
    def silenciar(self):
        """Desativa áudio."""
        self.ativo = False
        print("[AUDIO] Silenciado", file=sys.stderr)
    
    def ativar(self):
        """Ativa áudio."""
        self.ativo = True
        print("[AUDIO] Ativado", file=sys.stderr)
    
    def is_ativo(self) -> bool:
        """Retorna se está ativo."""
        return self.ativo
    
    def toggle(self) -> bool:
        """Alterna ativo/silencioso."""
        self.ativo = not self.ativo
        print(f"[AUDIO] Toggle para: {self.ativo}", file=sys.stderr)
        return self.ativo


# Instância global
print("[AUDIO] Criando AudioManager global...", file=sys.stderr)
audio_manager = AudioManager()
print("[AUDIO] ✅ AudioManager criado!", file=sys.stderr)
