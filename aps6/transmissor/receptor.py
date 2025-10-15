import sounddevice as sd  
import numpy as np 
import matplotlib.pyplot as plt  
import time

fs = 44100  # frequência de amostragem

# Espera o usuário iniciar
input("Pressione ENTER para iniciar a gravação...")
inicio = time.time()
print("Gravando...")

# Inicia o stream de gravação (sem número fixo de amostras)
stream = sd.InputStream(samplerate=fs, channels=1)
stream.start()

# Espera o usuário parar
input("Pressione ENTER para parar a gravação...")
fim = time.time()
print("Gravação finalizada.")

# Calcula a duração e lê o áudio correspondente
duracao = fim - inicio
amostras = int(duracao * fs)
audio, _ = stream.read(amostras)
stream.stop()

print(f"Duração gravada: {duracao:.2f} segundos ({amostras} amostras)")

# Transformada de Fourier
transformada = np.fft.fft(audio.squeeze())
frequencias = np.fft.fftfreq(len(transformada), 1/fs)

pares = list(zip(frequencias, np.abs(transformada)))
dic = {}
for tupla in pares:
    if tupla[0] > 0 and tupla[0] < 1500:  # Considera apenas frequências positivas
        dic[tupla[0]] = tupla[1]
if dic:
    # Ordena pelas chaves (frequências) em ordem decrescente e pega as 5 maiores
    top5_by_freq = sorted(dic.items(), key=lambda item: item[1], reverse=True)[:20]
    top5_by_freq_dict = dict(top5_by_freq)
    print("\nTop 5 maiores frequências e suas magnitudes (ordenadas por frequência decrescente):")
    for freq, mag in top5_by_freq:
        print(f"{freq:.2f} Hz: {mag:.6f}")
    print('\nDicionário top5 por frequência:', top5_by_freq_dict)
else:
    print("Dicionário vazio: sem frequências positivas.")

# Formata os valores para 3 casas decimais antes de criar o dicionário


# Gráfico
plt.plot(frequencias, np.abs(transformada))
plt.xlim(0, 2000)
plt.title("Gráfico transformada de Fourier")
plt.show()
