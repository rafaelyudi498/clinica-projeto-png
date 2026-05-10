"""
audio_manager.py — Gerenciador de Áudio do Sistema

Controla reprodução de sons para eventos do sistema.
Usa winsound (Windows nativo) para máxima compatibilidade.
"""

import os
import sys
import numpy as np
from scipy.io import wavfile
from pathlib import Path
import threading
import winsound


# =========================================================================
# CONFIGURAÇÕES - ENCONTRAR DIRETÓRIO DE ÁUDIO
# =========================================================================

def encontrar_audio_dir():
    """Encontra o diretório de áudio com múltiplas estratégias."""
    
    # Estratégia 1: Relativo ao módulo atual
    try:
        modulo_dir = Path(__file__).parent.resolve()
        audio_dir = modulo_dir.parent / "audio"
        if audio_dir.exists():
            print(f"[AUDIO] Encontrado em (estratégia 1): {audio_dir}", file=sys.stderr)
            return audio_dir
    except Exception as e:
        print(f"[AUDIO DEBUG] Estratégia 1 falhou: {e}", file=sys.stderr)
    
    # Estratégia 2: Relativo ao diretório atual
    try:
        audio_dir = Path.cwd() / "audio"
        if audio_dir.exists():
            print(f"[AUDIO] Encontrado em (estratégia 2): {audio_dir}", file=sys.stderr)
            return audio_dir
    except Exception as e:
        print(f"[AUDIO DEBUG] Estratégia 2 falhou: {e}", file=sys.stderr)
    
    # Fallback: Criar em modules/..
    try:
        modulo_dir = Path(__file__).parent.resolve()
        audio_dir = modulo_dir.parent / "audio"
        print(f"[AUDIO] Usando fallback: {audio_dir}", file=sys.stderr)
        return audio_dir
    except:
        pass
    
    # Último fallback
    audio_dir = Path.cwd() / "audio"
    print(f"[AUDIO] Último fallback: {audio_dir}", file=sys.stderr)
    return audio_dir


AUDIO_DIR = encontrar_audio_dir()
SAMPLE_RATE = 22050


class AudioManager:
    """Gerenciador centralizado de áudio."""
    
    def __init__(self):
        """Inicializa o gerenciador de áudio."""
        self.ativo = True
        self.sons = {}
        
        print(f"[AUDIO] Inicializando AudioManager...", file=sys.stderr)
        print(f"[AUDIO] Diretório: {AUDIO_DIR}", file=sys.stderr)
        
        # Criar pasta se não existir
        AUDIO_DIR.mkdir(exist_ok=True, parents=True)
        
        # Gerar sons
        self._gerar_sons()
        
        # Carregar sons
        self._carregar_sons()
        
        print(f"[AUDIO] AudioManager pronto. Sons: {list(self.sons.keys())}", file=sys.stderr)
    
    def _gerar_sons(self):
        """Gera arquivos WAV."""
        sons = {
            "sucesso": self._criar_som_sucesso,
            "erro": self._criar_som_erro,
            "menu": self._criar_som_menu,
            "boot": self._criar_som_boot,
        }
        
        for nome, func in sons.items():
            caminho = AUDIO_DIR / f"{nome}.wav"
            if not caminho.exists():
                try:
                    print(f"[AUDIO] Gerando: {nome}", file=sys.stderr)
                    func(str(caminho))
                except Exception as e:
                    print(f"[AUDIO ERRO] {nome}: {e}", file=sys.stderr)
    
    @staticmethod
    def _onda_sen(freq, duracao, sr):
        """Cria onda senoidal."""
        t = np.linspace(0, duracao, int(sr * duracao))
        return np.sin(2 * np.pi * freq * t)
    
    @staticmethod
    def _criar_som_sucesso(caminho):
        """Som de sucesso: Dó → Lá (ascendente)."""
        sr = SAMPLE_RATE
        som = np.array([])
        
        # Primeira nota
        som = np.concatenate([som, AudioManager._onda_sen(262, 0.15, sr)])
        som = np.concatenate([som, np.zeros(int(sr * 0.05))])
        
        # Segunda nota
        som = np.concatenate([som, AudioManager._onda_sen(440, 0.15, sr)])
        
        # Fade out
        fade = np.linspace(1, 0, int(sr * 0.05))
        som[-len(fade):] *= fade
        
        # Normalizar com MÁXIMO VOLUME (90%)
        som = (som * 0.9 / np.max(np.abs(som) + 1e-10)).astype(np.int16)
        wavfile.write(caminho, sr, som)
    
    @staticmethod
    def _criar_som_erro(caminho):
        """Som de erro: Lá → Dó (descendente)."""
        sr = SAMPLE_RATE
        som = np.array([])
        
        # Primeira nota
        som = np.concatenate([som, AudioManager._onda_sen(440, 0.2, sr)])
        som = np.concatenate([som, np.zeros(int(sr * 0.1))])
        
        # Segunda nota
        som = np.concatenate([som, AudioManager._onda_sen(262, 0.2, sr)])
        
        # Fade out
        fade = np.linspace(1, 0, int(sr * 0.1))
        som[-len(fade):] *= fade
        
        # Normalizar com MÁXIMO VOLUME (90%)
        som = (som * 0.9 / np.max(np.abs(som) + 1e-10)).astype(np.int16)
        wavfile.write(caminho, sr, som)
    
    @staticmethod
    def _criar_som_menu(caminho):
        """Som de menu: tom simples."""
        sr = SAMPLE_RATE
        som = AudioManager._onda_sen(800, 0.2, sr)
        
        # Fade in/out
        fade_len = int(sr * 0.05)
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = np.linspace(1, 0, fade_len)
        
        som[:fade_len] *= fade_in
        som[-fade_len:] *= fade_out
        
        # Normalizar com MÁXIMO VOLUME (90%)
        som = (som * 0.9 / np.max(np.abs(som) + 1e-10)).astype(np.int16)
        wavfile.write(caminho, sr, som)
    
    @staticmethod
    def _criar_som_boot(caminho):
        """Som de boot: Dó → Mi → Lá (ascendente)."""
        sr = SAMPLE_RATE
        som = np.array([])
        
        for freq in [262, 330, 440]:
            som = np.concatenate([som, AudioManager._onda_sen(freq, 0.1, sr)])
            som = np.concatenate([som, np.zeros(int(sr * 0.02))])
        
        # Fade out
        fade = np.linspace(1, 0, int(sr * 0.05))
        som[-len(fade):] *= fade
        
        # Normalizar com MÁXIMO VOLUME (90%)
        som = (som * 0.9 / np.max(np.abs(som) + 1e-10)).astype(np.int16)
        wavfile.write(caminho, sr, som)
    
    def _carregar_sons(self):
        """Carrega caminhos dos sons."""
        for nome in ["sucesso", "erro", "menu", "boot"]:
            try:
                caminho = AUDIO_DIR / f"{nome}.wav"
                if caminho.exists():
                    caminho_absoluto = str(caminho.resolve())
                    self.sons[nome] = caminho_absoluto
                    print(f"[AUDIO] Carregado: {nome}", file=sys.stderr)
                else:
                    print(f"[AUDIO] NÃO ENCONTRADO: {caminho}", file=sys.stderr)
            except Exception as e:
                print(f"[AUDIO ERRO] Carregar {nome}: {e}", file=sys.stderr)
    
    def reproduzir(self, tipo_som: str):
        """Reproduz som (bloqueante para garantir que toca)."""
        if not self.ativo or tipo_som not in self.sons:
            return
        
        caminho = self.sons[tipo_som]
        print(f"[AUDIO] Reproduzindo: {tipo_som} ({caminho})", file=sys.stderr)
        
        # BLOQUEANTE (não em thread) para garantir que toca
        try:
            print(f"[AUDIO] Iniciando reprodução bloqueante de {tipo_som}...", file=sys.stderr)
            winsound.PlaySound(caminho, winsound.SND_FILENAME)
            print(f"[AUDIO] ✅ SOM TOCADO: {tipo_som}", file=sys.stderr)
        except Exception as e:
            print(f"[AUDIO ERRO] {tipo_som}: {e}", file=sys.stderr)
    
    # Método removido - reprodução agora é bloqueante acima
    
    def silenciar(self):
        """Desativa sons."""
        self.ativo = False
    
    def ativar(self):
        """Ativa sons."""
        self.ativo = True
    
    def is_ativo(self):
        """Retorna se está ativo."""
        return self.ativo
    
    def toggle(self):
        """Alterna ativo/silencioso."""
        self.ativo = not self.ativo
        return self.ativo


# Criar instância global
print(f"[AUDIO] Criando AudioManager global...", file=sys.stderr)
audio_manager = AudioManager()
print(f"[AUDIO] AudioManager criado!", file=sys.stderr)
