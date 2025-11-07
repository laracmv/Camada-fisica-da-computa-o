import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import sounddevice as sd

# ======== LEITURA DOS ÁUDIOS =========
fs1, audio1 = wavfile.read("audio1.wav")
fs2, audio2 = wavfile.read("audio2.wav")
fs3, audio3 = wavfile.read("audio3.wav")

# converte para mono (média dos canais se for estéreo)
if audio1.ndim > 1:
    audio1 = audio1.mean(axis=1)
if audio2.ndim > 1:
    audio2 = audio2.mean(axis=1)
if audio3.ndim > 1:
    audio3 = audio3.mean(axis=1)

# normaliza entre -1 e 1
audio1 = audio1 / np.max(np.abs(audio1))
audio2 = audio2 / np.max(np.abs(audio2))
audio3 = audio3 / np.max(np.abs(audio3))

# garante mesmo tamanho
N = min(len(audio1), len(audio2), len(audio3))
audio1, audio2, audio3 = audio1[:N], audio2[:N], audio3[:N]

# ======== FIXA TAXA DE AMOSTRAGEM ========
fs = 44100   # pode mudar para 44800 se quiser
t = np.arange(N) / fs

# ======== MODULAÇÃO =========
fcentral1, fcentral2, fcentral3 = 10500, 13500, 16500
m1 = audio1 * np.cos(2*np.pi*fcentral1*t)
m2 = audio2 * np.cos(2*np.pi*fcentral2*t)
m3 = audio3 * np.cos(2*np.pi*fcentral3*t)

# ======== SOMA =========
s = m1 + m2 + m3

# ======== FFTs =========
def plot_fft(sig, fs, titulo):
    N = len(sig)
    f = np.fft.fftfreq(N, 1/fs)
    S = np.fft.fft(sig)
    plt.plot(f[:N//2]/1000, np.abs(S[:N//2]))
    plt.title(titulo)
    plt.xlabel("Frequência (kHz)")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()

plot_fft(m1, fs, "Sinal Modulado 1")
plot_fft(m2, fs, "Sinal Modulado 2")
plot_fft(m3, fs, "Sinal Modulado 3")
plot_fft(s, fs, "Soma dos 3 Sinais")

# ======== FILTROS =========
def butter_bandpass(low, high, fs, ordem=6):
    b, a = butter(ordem, [low/(fs/2), high/(fs/2)], btype='band')
    return b, a

def butter_lowpass(corte, fs, ordem=6):
    b, a = butter(ordem, corte/(fs/2), btype='low')
    return b, a

# ======== EXTRAÇÃO =========
b1, a1f = butter_bandpass(9000, 12000, fs)
b2, a2f = butter_bandpass(12000, 15000, fs)
b3, a3f = butter_bandpass(15000, 18000, fs)
x1 = lfilter(b1, a1f, s)
x2 = lfilter(b2, a2f, s)
x3 = lfilter(b3, a3f, s)

plot_fft(x1, fs, "Sinal Extraído 1")
plot_fft(x2, fs, "Sinal Extraído 2")
plot_fft(x3, fs, "Sinal Extraído 3")

# ======== DEMODULAÇÃO =========
d1 = x1 * np.cos(2*np.pi*fcentral1*t)
d2 = x2 * np.cos(2*np.pi*fcentral2*t)
d3 = x3 * np.cos(2*np.pi*fcentral3*t)

b_lp, a_lp = butter_lowpass(4000, fs)
d1 = lfilter(b_lp, a_lp, d1)
d2 = lfilter(b_lp, a_lp, d2)
d3 = lfilter(b_lp, a_lp, d3)

# ======== FFTs DOS DEMODULADOS =========
plot_fft(d1, fs, "Sinal Demodulado 1 (lado receptor)")
plot_fft(d2, fs, "Sinal Demodulado 2 (lado receptor)")
plot_fft(d3, fs, "Sinal Demodulado 3 (lado receptor)")

# ======== REPRODUÇÃO =========
print("Reproduzindo áudio original 1...")
sd.play(audio1, fs); sd.wait()
print("Reproduzindo áudio demodulado 1...")
sd.play(d1, fs); sd.wait()

print("Reproduzindo áudio original 2...")
sd.play(audio2, fs); sd.wait()
print("Reproduzindo áudio demodulado 2...")
sd.play(d2, fs); sd.wait()

print("Reproduzindo áudio original 3...")
sd.play(audio3, fs); sd.wait()
print("Reproduzindo áudio demodulado 3...")
sd.play(d3, fs); sd.wait()
