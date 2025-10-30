import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import lfilter, freqz
from filtro_peaking_EQ import peaking_eq

# ======================================================
# CONFIGURAÇÃO INICIAL
# ======================================================

# Frequências padrão do equalizador (Hz)
bandas_freq = [20, 32, 64, 125, 250, 500, 1000, 2000, 4000, 8000, 16000, 20000]

# Lê arquivo WAV
sample_rate, audio = wavfile.read("bad-romance.wav")

# Se for estéreo, converte para mono (média dos canais)
if audio.ndim > 1:
    audio = audio.mean(axis=1)

# Normaliza entre -1 e 1
audio = audio / np.max(np.abs(audio))

print("\n=== CONFIGURAÇÃO DO EQUALIZADOR ===")
print("Intervalo de ganho: -10 dB a +10 dB (use números inteiros)\n")

# Coleta dos ganhos por banda
ganhos = []
for f in bandas_freq:
    while True:
        try:
            val = float(input(f"Ganho para {f} Hz: "))
            if -10 <= val <= 10:
                ganhos.append(val)
                break
            else:
                print("Digite um valor entre -10 e +10.")
        except ValueError:
            print("Valor inválido. Digite um número.")

# ======================================================
# PROCESSAMENTO DOS FILTROS
# ======================================================
Q = 3  # Fator de qualidade fixo, quanto maior o Q, mais estreita e intensa é a banda em torno da frequência central. Filtro mais seletivo.

# Guardar os filtros em listas
filtros = []
for f0, gain_db in zip(bandas_freq, ganhos):
    b, a = peaking_eq(f0, gain_db, Q, sample_rate)
    filtros.append((b, a))

# ----------- DIAGRAMA DE BODE-----------
w = np.logspace(np.log10(20), np.log10(22000), 2000)
h_total = np.ones_like(w, dtype=complex)
for b, a in filtros:
    _, h = freqz(b, a, worN=w, fs=sample_rate)
    h_total *= h

plt.figure(figsize=(10, 5))
plt.semilogx(w, 20 * np.log10(np.abs(h_total)))
plt.title("Diagrama de Bode - Filtro Total (12 bandas)")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Ganho [dB]")
plt.grid(which="both", linestyle="--", linewidth=0.5)
plt.ylim(-15, 15)
plt.xlim(20, 22000)
plt.show()

# ----------- FILTRAGEM DO ÁUDIO -----------
print("Aplicando filtros ao áudio...")
audio_filtrado = audio.copy()
for b, a in filtros:
    audio_filtrado = lfilter(b, a, audio_filtrado)
audio_filtrado /= np.max(np.abs(audio_filtrado))

# ======================================================
# REPRODUÇÃO PARA COMPARAÇÃO
# ======================================================
print("\nReproduzindo áudio original...")
sd.play(audio, sample_rate)
sd.wait()

print("Reproduzindo áudio filtrado...")
sd.play(audio_filtrado, sample_rate)
sd.wait()
