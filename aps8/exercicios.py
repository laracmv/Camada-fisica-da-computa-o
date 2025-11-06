"""
AM_modulation_project.py
Resolve Exercícios 1-7 e Projeto 8 conforme enunciado enviado.
Arquivos gerados nomes terão a assinatura: ChatGPT_GPT5

Autor (assinatura nos arquivos): ChatGPT — GPT-5 Thinking mini
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift
from scipy.signal import butter, sosfiltfilt, sosfilt, hilbert
import soundfile as sf
import os

# --- Configurações gerais ---
fs = 44100  # taxa de amostragem padrão
save_dir = "AM_project_outputs_ChatGPT_GPT5"
os.makedirs(save_dir, exist_ok=True)

def save_plot(fig, name):
    path = os.path.join(save_dir, name)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print("Saved:", path)

def compute_fft(x, fs):
    N = len(x)
    X = fft(x)
    freqs = fftfreq(N, 1/fs)
    # return single-sided positive freq arrays (magnitude)
    return freqs, X

def plot_signal_and_fft(t, x, fs, title_prefix, fname_prefix):
    fig, ax = plt.subplots(2,1, figsize=(8,6))
    ax[0].plot(t, x)
    ax[0].set_title(f"{title_prefix} — tempo")
    ax[0].set_xlabel("t [s]")
    ax[1].magnitude_spectrum(x, Fs=fs)
    ax[1].set_title(f"{title_prefix} — FFT (magnitude)")
    save_plot(fig, f"{fname_prefix}.png")

# --- Exercício 1 ---
def ex1():
    print("=== Exercício 1 ===")
    duration = 0.05  # curto só pra visualizar
    t = np.arange(0, duration, 1/fs)
    m_f = 2000.0
    c_f = 15000.0
    m = np.cos(2*np.pi*m_f*t)
    c = np.cos(2*np.pi*c_f*t)
    # soma (intuitiva, NÃO modulação)
    s_sum = m + c
    # FFTs e plots
    plot_signal_and_fft(t, m, fs, "m(t) = cos(2kHz)", "ex1_m_time_fft")
    plot_signal_and_fft(t, c, fs, "carrier 15kHz", "ex1_c_time_fft")
    plot_signal_and_fft(t, s_sum, fs, "soma m+c (não modulada)", "ex1_sum_time_fft")
    print("Ex1: gerados gráficos mostrando que soma NÃO encaixa estritamente na banda 12-18 kHz")
    
# --- Exercício 2 (resposta analítica) ---
def ex2_answer():
    # Para sinal m com f_m = 2kHz e carrier 15kHz -> bandas nas frequências |f_c ± f_m|
    f_c = 15000.0
    f_m = 2000.0
    band_min = f_c - f_m
    band_max = f_c + f_m
    print("=== Exercício 2 ===")
    print(f"Portadora: {f_c} Hz, sinal: {f_m} Hz -> Banda mínima: [{band_min} Hz, {band_max} Hz]")
    print("Portanto banda mínima: 13 kHz a 17 kHz (ou seja, largura = 4 kHz)")

# --- Exercício 3 ---
def ex3():
    print("=== Exercício 3 ===")
    duration = 2.0
    t = np.arange(0, duration, 1/fs)
    m = np.cos(2*np.pi*2000.0*t)
    c = np.cos(2*np.pi*15000.0*t)
    s = m * c  # modulação AM (DSB, sem portadora adicional)
    plot_signal_and_fft(t, m, fs, "m(t) 2kHz", "ex3_m_time_fft")
    plot_signal_and_fft(t, c, fs, "carrier 15kHz", "ex3_c_time_fft")
    plot_signal_and_fft(t, s, fs, "s(t)=m*c (AM)", "ex3_mod_time_fft")
    print("Ex3: modulação por multiplicação executada e gráficos salvos.")

# --- Exercício 4 (o que fazer antes da modulação) ---
def ex4_demo():
    print("=== Exercício 4 ===")
    # solução: aplicar filtro passa-baixa para remover componentes > 2k,
    # ou compressão, ou upshift por preemphasis + modulação.
    print("Sugestões: lowpass (<=2000 Hz) e possivelmente normalizar; ou usar downsampling e depois 'frequency shifting' (modulação) — aqui mostramos filtro lowpass como exemplo.")
    # exemplo: gera m(t) composta por várias sinos 20..2000
    duration = 1.0
    t = np.arange(0, duration, 1/fs)
    freqs = np.linspace(20,2000,40)
    m = np.sum([0.5*np.cos(2*np.pi*f*t + np.random.rand()*2*np.pi) for f in freqs], axis=0)
    # filtro passa-baixa com corte em 2000 Hz (já ok) - mostramos apenas o sinal
    plot_signal_and_fft(t, m, fs, "m(t) multi 20-2000Hz", "ex4_m_multisin_time_fft")
    print("Ex4: plotei exemplo de m(t) multi-senoides. Antes da modulação, garanta LPF e normalização.")

# --- Funções utilitárias para modulação/demodulação e filtros ---
def bandpass_sos(f1, f2, fs, order=6):
    nyq = 0.5*fs
    low = f1/nyq
    high = f2/nyq
    sos = butter(order, [low, high], btype='bandpass', output='sos')
    return sos

def lowpass_sos(fc, fs, order=6):
    nyq = 0.5*fs
    w = fc/nyq
    sos = butter(order, w, btype='lowpass', output='sos')
    return sos

def modulate_am(m, fc, fs):
    t = np.arange(0, len(m))/fs
    carrier = np.cos(2*np.pi*fc*t)
    return m * carrier, carrier

# --- Exercício 5 ---
def ex5_process(audio_path=None):
    print("=== Exercício 5 ===")
    # se audio_path None -> gerar um exemplo (voz/sinal)
    if audio_path is None:
        print("Nenhum áudio fornecido. Gerando um sinal exemplo (sinusoide modulada / curta).")
        duration = 3.0
        t = np.arange(0, duration, 1/fs)
        # uso soma de sinos até 3 kHz (exemplo)
        m = 0.6*np.sin(2*np.pi*440*t) + 0.3*np.sin(2*np.pi*880*t) + 0.1*np.sin(2*np.pi*1500*t)
    else:
        m, fs_file = sf.read(audio_path)
        if m.ndim>1: m = m.mean(axis=1)  # mono
        # resample if needed
        if fs_file != fs:
            raise RuntimeError("Audio sample rate mismatch; resample externally or change fs.")
        t = np.arange(0, len(m))/fs
        duration = t[-1]
    # analisar Fourier do original
    plot_signal_and_fft(t, m, fs, "audio original", "ex5_audio_orig_time_fft")
    # gerar portadora 16kHz e modular para faixa 14k-18k (portadora 16k)
    s_mod, carrier = modulate_am(m, 16000.0, fs)
    plot_signal_and_fft(t, s_mod, fs, "audio modulado (16kHz)", "ex5_mod_time_fft")
    # salvar modulado (normalizar)
    s_mod_norm = s_mod / np.max(np.abs(s_mod)) * 0.9
    sf.write(os.path.join(save_dir, "ex5_modulated_ChatGPT_GPT5.wav"), s_mod_norm, fs)
    print("Arquivo modulado salvo.")
    # demodulação síncrona: multiplicar por mesma portadora e LPF em fc ~ 3 kHz
    s_dem = s_mod * carrier  # multiplicar por portadora
    sos = lowpass_sos(3000, fs, order=8)
    recovered = sosfiltfilt(sos, s_dem) * 2.0  # ganho de correção (teórico)
    recovered = recovered / np.max(np.abs(recovered)) * 0.9
    plot_signal_and_fft(t, recovered, fs, "audio demodulado", "ex5_demod_time_fft")
    sf.write(os.path.join(save_dir, "ex5_demodulated_ChatGPT_GPT5.wav"), recovered, fs)
    print("Ex5: modulado e demodulado — arquivos salvos.")

# --- Exercícios 6 e 7 (cálculos) ---
def ex6_calc():
    print("=== Exercício 6 ===")
    # 64-QAM -> 6 bits por símbolo (pois 64 = 2^6)
    bits_per_symbol = 6
    fc = 2.4e9
    # variação a cada 2 períodos: símbolo duração Ts = 2 * (1/fc)
    Ts = 2.0*(1.0/fc)
    symbol_rate = 1.0/Ts
    bit_rate = symbol_rate * bits_per_symbol
    print(f"64-QAM: bits/símbolo = {bits_per_symbol}, símbolo rate = {symbol_rate:.3e} s^-1, taxa de bits ≈ {bit_rate:.3e} bps")
    print("Interpretação: taxa (bps) = 6 * (fc/2) = 3*fc bits/s = 3 * 2.4GHz = 7.2 Gbit/s")

def ex7_calc():
    print("=== Exercício 7 ===")
    # 256-QAM -> 8 bits por símbolo
    bits_per_symbol = 8
    fc = 2.4e9
    # variação mínima a cada 10 períodos: Ts = 10*(1/fc)
    Ts = 10.0*(1.0/fc)
    symbol_rate = 1.0/Ts
    bit_rate = symbol_rate * bits_per_symbol
    # 480 MBytes -> bits
    bytes_to_send = 480 * 1024 * 1024  # usar MBytes = 1024^2? ajustar conforme enunciado; aqui assumimos 480*2^20
    bits_to_send = bytes_to_send * 8.0
    time_seconds = bits_to_send / bit_rate
    print(f"256-QAM: bits/símbolo = {bits_per_symbol}, symbol_rate = {symbol_rate:.3e} s^-1, bit_rate ≈ {bit_rate:.3e} bps")
    print(f"Para enviar 480 MBytes (~{bytes_to_send} bytes = {bits_to_send} bits) levaria ≈ {time_seconds:.3f} s ({time_seconds/3600:.3f} h)")

# --- Projeto 8: funções principais ---
def project8_pipeline(audio_paths=None):
    """
    audio_paths: list of 3 paths to wav files (mono, fs=44100). 
                 If None, gera 3 exemplos curtos.
    Faixas:
      Faixa1: 9k-12k  -> center 10.5k
      Faixa2: 12k-15k -> center 13.5k
      Faixa3: 15k-18k -> center 16.5k
    """
    print("=== Projeto 8 pipeline ===")
    centers = [10500.0, 13500.0, 16500.0]
    band_ranges = [(9000, 12000), (12000, 15000), (15000, 18000)]
    duration = 3.0
    t = np.arange(0, duration, 1/fs)
    # carregar ou gerar 3 sinais
    signals = []
    if audio_paths is None:
        # gera 3 exemplos com conteúdo diferente
        s1 = 0.6*np.sin(2*np.pi*440*t)             # voz-like tone
        s2 = 0.4*np.sin(2*np.pi*660*t) + 0.2*np.sin(2*np.pi*880*t)
        s3 = 0.5*np.sin(2*np.pi*220*t) + 0.2*np.sin(2*np.pi*1100*t)
        originals = [s1, s2, s3]
    else:
        originals = []
        for p in audio_paths:
            x, fs_file = sf.read(p)
            if x.ndim>1: x = x.mean(axis=1)
            if fs_file != fs:
                raise RuntimeError("Resample audio to 44100 Hz first.")
            # trim/pad to duration
            if len(x) > int(duration*fs):
                x = x[:int(duration*fs)]
            else:
                pad = int(duration*fs) - len(x)
                x = np.concatenate([x, np.zeros(pad)])
            originals.append(x)
    # modular cada sinal pra sua faixa (multiplicação por portadora central)
    modulated = []
    carriers = []
    for i, m in enumerate(originals):
        fc = centers[i]
        s, c = modulate_am(m, fc, fs)
        # normalizar
        s = s / np.max(np.abs(s)) * 0.9
        modulated.append(s)
        carriers.append(c)
        sf.write(os.path.join(save_dir, f"proj8_station{i+1}_modulated_ChatGPT_GPT5.wav"), s, fs)
        plot_signal_and_fft(t, s, fs, f"Station {i+1} modulated (fc={fc} Hz)", f"proj8_station{i+1}_mod_fft")
    # somar as 3 estações (sinal no "meio físico")
    composite = modulated[0] + modulated[1] + modulated[2]
    composite = composite / np.max(np.abs(composite)) * 0.9
    sf.write(os.path.join(save_dir, "proj8_composite_ChatGPT_GPT5.wav"), composite, fs)
    plot_signal_and_fft(t, composite, fs, "Composite (3 stations)", "proj8_composite_fft")
    # receptor: para cada faixa, aplicar bandpass e demodular
    extracted = []
    for i, band in enumerate(band_ranges):
        sos = bandpass_sos(band[0], band[1], fs, order=8)
        filtered = sosfiltfilt(sos, composite)
        # multiplicar por carrier estimado (recriar)
        fc = centers[i]
        carrier_est = np.cos(2*np.pi*fc*t)
        dem = filtered * carrier_est
        # lowpass para recuperar (use corte ~ 2k-4k)
        sos_lp = lowpass_sos(4000, fs, order=8)
        recovered = sosfiltfilt(sos_lp, dem) * 2.0
        # normalizar e salvar
        recovered = recovered / np.max(np.abs(recovered)) * 0.9
        extracted.append(recovered)
        sf.write(os.path.join(save_dir, f"proj8_station{i+1}_demodulated_ChatGPT_GPT5.wav"), recovered, fs)
        plot_signal_and_fft(t, recovered, fs, f"Recovered station {i+1}", f"proj8_station{i+1}_recovered_fft")
    print("Projeto 8: pipeline executado. Arquivos e gráficos salvos em", save_dir)

# --- Rodar tudo ---
if __name__ == "__main__":
    ex1()
    ex2_answer()
    ex3()
    ex4_demo()
    ex5_process(audio_path=None)  # se quiser usar arquivo real, passe caminho aqui
    ex6_calc()
    ex7_calc()
    project8_pipeline(audio_paths=None)  # se tiver 3 arquivos, passe lista de paths
    print("=== Fim. Verifique a pasta:", save_dir)
