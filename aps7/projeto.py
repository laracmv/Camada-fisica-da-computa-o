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
bandas_freq = [31, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000, 20000]

# Lê arquivo WAV
sample_rate, audio = wavfile.read("bad-romance.wav")

# Se for estéreo, converte para mono (média dos canais)
if audio.ndim > 1:
    audio = audio.mean(axis=1)

# Normaliza entre -1 e 1
audio = audio / np.max(np.abs(audio))

print("\n=== CONFIGURAÇÃO DO EQUALIZADOR (Peaking EQ) ===")
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
                print("⚠️ Digite um valor entre -10 e +10.")
        except ValueError:
            print("⚠️ Valor inválido. Digite um número.")

# ======================================================
# PROCESSAMENTO DOS FILTROS
# ======================================================
Q = 1.0  # Fator de qualidade fixo

# Inicializa filtro equivalente (b_total, a_total)
b_total = np.array([1.0])
a_total = np.array([1.0])

print("\nCalculando filtros individuais e combinando...\n")

for f0, gain_db in zip(bandas_freq, ganhos):
    b, a = peaking_eq(f0, gain_db, Q, sample_rate)
    # Combina os filtros (produto das funções de transferência)
    b_total = np.convolve(b_total, b)
    a_total = np.convolve(a_total, a)

# ======================================================
# DIAGRAMA DE BODE
# ======================================================
w, h = freqz(b_total, a_total, fs=sample_rate)
plt.figure(figsize=(10, 5))
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title("Diagrama de Bode - Filtro Total")
plt.xlabel("Frequência [Hz]")
plt.ylabel("Ganho [dB]")
plt.grid(which="both", linestyle="--", linewidth=0.5)
plt.ylim(-15, 15)
plt.xlim(20, 22000)
plt.show()

# ======================================================
# APLICAÇÃO DOS FILTROS AO SINAL
# ======================================================
print("Aplicando filtro ao áudio...")
audio_filtrado = lfilter(b_total, a_total, audio)

# Normaliza o sinal filtrado
audio_filtrado /= np.max(np.abs(audio_filtrado))

# ======================================================
# REPRODUÇÃO PARA COMPARAÇÃO
# ======================================================
print("\n▶ Reproduzindo áudio original...")
sd.play(audio, sample_rate)
sd.wait()

print("▶ Reproduzindo áudio filtrado...")
sd.play(audio_filtrado, sample_rate)
sd.wait()

# ======================================================
# GRÁFICOS NO DOMÍNIO DO TEMPO
# ======================================================
plt.figure(figsize=(10, 4))
plt.plot(audio[:5000], label="Original", alpha=0.7)
plt.plot(audio_filtrado[:5000], label="Filtrado", alpha=0.7)
plt.legend()
plt.title("Sinais no tempo (primeiros 5000 samples)")
plt.xlabel("Amostras")
plt.ylabel("Amplitude")
plt.show()

print("\n✅ Processamento concluído com sucesso!")
