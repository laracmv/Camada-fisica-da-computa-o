import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import sounddevice as sd

# ---------------- CONFIGURAÇÃO ----------------
fs = 44100
faixas = [(9000, 12000), (12000, 15000), (15000, 18000)]
arquivos = ["audio1.wav", "audio2.wav", "audio3.wav"]

def butter_bandpass(low, high, fs, ordem=4):
    b, a = butter(ordem, [low/(fs/2), high/(fs/2)], btype='band')
    return b, a

def butter_lowpass(corte, fs, ordem=4):
    b, a = butter(ordem, corte/(fs/2), btype='low')
    return b, a

def aplicar_filtro(b, a, x): return lfilter(b, a, x)

# ---------------- EMISSOR ----------------
audios, modulados = [], []
t = None

for i, nome in enumerate(arquivos):
    fs, audio = wavfile.read(nome)
    if audio.ndim > 1: audio = audio.mean(axis=1)
    audio = audio / np.max(np.abs(audio))
    audios.append(audio)

# 🔧 Ajuste de duração (usa o menor áudio)
min_len = min(len(a) for a in audios)
audios = [a[:min_len] for a in audios]
t = np.arange(min_len) / fs

# Agora sim, modulação
for i, audio in enumerate(audios):
    f_portadora = np.mean(faixas[i])
    modulados.append((1 + audio) * np.cos(2*np.pi*f_portadora*t))

sinal_total = sum(modulados)

# ---------------- FFTS ----------------
def plot_fft(signal, title):
    N = len(signal)
    freq = np.fft.fftfreq(N, 1/fs)
    plt.plot(freq[:N//2], np.abs(np.fft.fft(signal))[:N//2])
    plt.title(title); plt.xlabel("Frequência [Hz]"); plt.ylabel("|FFT|"); plt.grid()

plt.figure(figsize=(12,8))
for i, s in enumerate(modulados):
    plt.subplot(4,1,i+1)
    plot_fft(s, f"Sinal {i+1} Modulado")
plt.subplot(4,1,4)
plot_fft(sinal_total, "Sinal Total (soma)")
plt.tight_layout(); plt.show()

# ---------------- RECEPTOR ----------------
demodulados = []
for i, faixa in enumerate(faixas):
    b_band, a_band = butter_bandpass(faixa[0], faixa[1], fs)
    extraido = aplicar_filtro(b_band, a_band, sinal_total)
    f_portadora = np.mean(faixa)
    demod = extraido * np.cos(2*np.pi*f_portadora*t)
    b_lp, a_lp = butter_lowpass(4000, fs)  # corta acima de 4 kHz
    demod_final = aplicar_filtro(b_lp, a_lp, demod)
    demod_final /= np.max(np.abs(demod_final))
    demodulados.append(demod_final)

# ---------------- FFT DOS SINAIS EXTRAÍDOS (RECEPTOR) ----------------
plt.figure(figsize=(12,8))
for i, faixa in enumerate(faixas):
    b_band, a_band = butter_bandpass(faixa[0], faixa[1], fs)
    extraido = aplicar_filtro(b_band, a_band, sinal_total)
    plt.subplot(3,1,i+1)
    plot_fft(extraido, f"Sinal {i+1} extraído (Receptor) - Faixa {faixa[0]}–{faixa[1]} Hz")
plt.tight_layout(); plt.show()


# ---------------- RESULTADOS ----------------
print("\nReproduzindo sinais originais e demodulados...\n")
for i in range(3):
    print(f"Original {i+1}")
    sd.play(audios[i], fs); sd.wait()
    print(f"Demodulado {i+1}")
    sd.play(demodulados[i], fs); sd.wait()
