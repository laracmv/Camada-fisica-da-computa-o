# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 10:20:31 2025

@author: RodrigoC5
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt

try:
    from scipy.io import wavfile
    SCIPY_AVAILABLE = True
except Exception:
    SCIPY_AVAILABLE = False

def compute_fft(x, fs, window=None, nfft=None, return_complex=False):
    """
    Calcula FFT unilateral (frequências positivas) e retorna frequências, magnitude linear,
    magnitude em dB, e (opcional) o espectro complexo.
    - x: sinal no tempo (1D numpy)
    - fs: taxa de amostragem (Hz)
    - window: None ou string: 'hann', 'hamming', 'blackman'
    - nfft: número de pontos para FFT (zero-padding se > len(x))
    """
    x = np.asarray(x, dtype=float)
    N = x.size

    # janela
    if window is None:
        w = np.ones(N)
    else:
        if window.lower() == 'hann':
            w = np.hanning(N)
        elif window.lower() == 'hamming':
            w = np.hamming(N)
        elif window.lower() == 'blackman':
            w = np.blackman(N)
        else:
            raise ValueError("Janela desconhecida: use 'hann', 'hamming', 'blackman' ou None")

    xw = x * w

    # nfft
    if nfft is None:
        nfft = N
    elif nfft < N:
        raise ValueError("nfft deve ser >= N (ou None)")

    # FFT unilateral com numpy.rfft
    X = np.fft.rfft(xw, n=nfft)
    freqs = np.fft.rfftfreq(nfft, d=1.0/fs)

    # normalização: dividir por soma da janela para preservar amplitude
    # (ou por N para uma normalização simples). Aqui usamos soma da janela:
    scale = np.sum(w) if np.sum(w) != 0 else N
    magnitude = np.abs(X) / scale

    # ajustar fator 2 para termos positivos (exceto DC e Nyquist se presentes)
    # Porque rfft retorna só metade do espectro — para conservar energia dobramos componentes não-DC/Nyquist
    # Identificar indices a dobrar:
    if nfft % 2 == 0:
        # mesmo nfft -> índice de Nyquist existe (último índice)
        magnitude[1:-1] *= 2.0
    else:
        magnitude[1:] *= 2.0

    # evitar log(0)
    eps = 1e-12
    magnitude_db = 20.0 * np.log10(magnitude + eps)

    if return_complex:
        return freqs, magnitude, magnitude_db, X
    else:
        return freqs, magnitude, magnitude_db

def plot_time_and_spectrum(t, x, fs, freqs, magnitude, magnitude_db, x_label_time='Tempo (s)'):
    """Plota sinal no tempo e espectros (linear + dB)."""
    plt.figure(figsize=(10, 3.2))
    plt.plot(t, x)
    plt.xlabel(x_label_time)
    plt.ylabel('Amplitude')
    plt.title('Sinal no domínio do tempo')
    plt.grid(True)
    plt.tight_layout()

    plt.figure(figsize=(10, 3.2))
    plt.plot(freqs, magnitude)
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Magnitude (linear)')
    plt.title('Espectro de frequência (magnitude)')
    plt.xlim(0, fs / 2)
    plt.grid(True)
    plt.tight_layout()

    plt.figure(figsize=(10, 3.2))
    plt.plot(freqs, magnitude_db)
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Espectro de frequência (dB)')
    plt.xlim(0, fs / 2)
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def generate_example_signal(fs=1000.0, T=1.0):
    """Gera sinal de exemplo: soma de senóides + ruído."""
    N = int(fs * T)
    t = np.linspace(0, T, N, endpoint=False)
    x = 1.0 * np.sin(2*np.pi*50.0*t) + 0.6 * np.sin(2*np.pi*120.0*t)
    np.random.seed(0)
    x += 0.2 * np.random.normal(size=t.shape)
    return t, x


def main():
    fs=1000
    T=1.0
    t, x = generate_example_signal(fs, T)
    freqs, magnitude, magnitude_db = compute_fft(x, fs, window=None, nfft=None, return_complex=False)
    plot_time_and_spectrum(t, x, fs , freqs, magnitude, magnitude_db, x_label_time='Tempo (s)')
    plt.show()

if __name__ == "__main__":
    main()