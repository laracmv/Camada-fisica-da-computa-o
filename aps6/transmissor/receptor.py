import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import threading
from FFT import compute_fft, plot_time_and_spectrum

# Dicionário com os acordes e suas frequências características 
# Cada acorde é composto por três frequências fundamentais
ACORDES = {
    "do_maior":     [523.25, 659.25, 783.99],
    "re_menor":     [587.33, 698.46, 880.00],
    "mi_menor":     [659.25, 783.99, 987.77],
    "fa_maior":     [698.46, 880.00, 1046.50],
    "sol_maior":    [783.99, 987.77, 1174.66],
    "la_menor":     [880.00, 1046.50, 1318.51],
    "si_menor_5b":  [493.88, 587.33, 698.46]
}


# Função que compara as frequências detectadas pela FFT com
# as frequências esperadas de cada acorde
def identificar_acorde(freqs_detectadas, tolerancia=10):
    # Percorre o dicionário de acordes
    for nome, freq_ref in ACORDES.items():
        coincidencias = 0
        # Para cada frequência do acorde de referência
        for f_ref in freq_ref:
            # Compara com todas as frequências detectadas pela FFT
            for f_det in freqs_detectadas:
                # Se a diferença entre elas for menor que a tolerância, considera que aquela nota foi encontrada
                if abs(f_ref - f_det) <= tolerancia:
                    coincidencias += 1
                    break  
        # Se pelo menos 3 frequências coincidirem, o acorde é identificado
        if coincidencias >= 3:
            return nome
  
    return "Acorde não identificado"

def main():
    fs = 44100        # taxa de amostragem
    duracao = 4.0     

    print("=== RECEPTOR DE ACORDES ===")
    print("Gravando áudio... (toque o som agora!)")

    # Grava o áudio do microfone usando a biblioteca sounddevice
    # channels=1: um único canal
    # dtype='float64' define o tipo de dado do vetor gravado
    gravacao = sd.rec(int(fs * duracao), samplerate=fs, channels=1, dtype='float64')
    sd.wait() 
    print("Gravação concluída!\n")

    
    x = gravacao.flatten()

    # Normaliza o sinal para o intervalo -1 a 1
    # Isso garante que o volume captado não cause saturação no cálculo da FFT
    x = x / np.max(np.abs(x))

    # Calcula a Transformada Rápida de Fourier (FFT) para obter o espectro de frequências
    freqs, mag, mag_db = compute_fft(x, fs)

    # Identifica as frequências mais intensas
    peaks, props = find_peaks(mag, height=np.max(mag) * 0.05, distance=100)
    freq_picos = freqs[peaks]           # Frequências correspondentes aos picos
    alturas = props["peak_heights"]     # Altura dos picos detectados

    # Seleciona as 5 frequências com maiores amplitudes
    indices_top = np.argsort(alturas)[-5:]
    principais = np.sort(freq_picos[indices_top])

    # Compara as frequências principais com as do dicionário e identifica o acorde
    nome_acorde = identificar_acorde(principais)

    # Exibe imediatamente o resultado da identificação no terminal
    print(f"Acorde identificado: {nome_acorde.upper()}")
    print("Principais picos (Hz):", np.round(principais, 2))

    # Abre os gráficos do sinal e do espectro em uma thread separada
    threading.Thread(
        target=plot_time_and_spectrum,
        args=(np.linspace(0, duracao, len(x)), x, fs, freqs, mag, mag_db)
    ).start()


if __name__ == "__main__":
    main()