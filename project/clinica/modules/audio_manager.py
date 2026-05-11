"""
audio_manager.py — Gerenciador de Áudio SIMPLES E FUNCIONAL

Usa winsound.Beep() para máxima compatibilidade e volume garantido.
Sem dependências extras - apenas Python nativo + threading.
"""

import winsound
import threading
import time


class AudioManager:
    """Gerenciador de áudio usando winsound.Beep()."""
    
    def __init__(self):
        """Inicializa gerenciador."""
        self.ativo = True
        self._som_em_execucao = False  # Flag para evitar sobreposição de sons
        self._lock = threading.Lock()
    
    def reproduzir(self, tipo_som: str):
        """Reproduz som usando Beep."""
        if not self.ativo:
            return
        
        # Executar em thread para não bloquear a interface
        thread = threading.Thread(
            target=self._tocar_som,
            args=(tipo_som,),
            daemon=True
        )
        thread.start()
    
    def _tocar_som(self, tipo_som: str):
        """Toca som usando winsound.Beep() com sincronização."""
        try:
            # Aguardar se outro som estiver em execução
            with self._lock:
                while self._som_em_execucao:
                    time.sleep(0.05)
                self._som_em_execucao = True
            
            if tipo_som == "sucesso":
                # Som de sucesso: Dó (262 Hz) → Lá (440 Hz) ascendente
                winsound.Beep(262, 300)  # Duração em ms
                time.sleep(0.1)
                winsound.Beep(440, 300)
            
            elif tipo_som == "erro":
                # Som de erro: Lá (440 Hz) → Dó (262 Hz) descendente
                winsound.Beep(440, 300)
                time.sleep(0.1)
                winsound.Beep(262, 300)
            
            elif tipo_som == "menu":
                # Som de menu: Tom único (800 Hz)
                winsound.Beep(800, 200)
            
            elif tipo_som == "boot":
                # Som de boot: Sequência ascendente Dó → Mi → Lá
                winsound.Beep(262, 200)  # Dó
                time.sleep(0.05)
                winsound.Beep(330, 200)  # Mi
                time.sleep(0.05)
                winsound.Beep(440, 200)  # Lá
            
        except Exception as e:
            pass
        
        finally:
            # Marcar que som terminou
            with self._lock:
                self._som_em_execucao = False
    
    def silenciar(self):
        """Desativa áudio."""
        self.ativo = False
    
    def ativar(self):
        """Ativa áudio."""
        self.ativo = True
    
    def is_ativo(self) -> bool:
        """Retorna se está ativo."""
        return self.ativo
    
    def toggle(self) -> bool:
        """Alterna ativo/silencioso."""
        self.ativo = not self.ativo
        return self.ativo


# Instância global
audio_manager = AudioManager()
