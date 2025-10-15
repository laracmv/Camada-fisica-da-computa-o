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
maior_menor = sorted(pares, key=lambda p: p[1], reverse=True)[:20]
# Formata os valores para 3 casas decimais antes de criar o dicionário
dicionario = {round(x, 3): round(y, 3) for x, y in maior_menor}
print(dicionario)

# Gráfico
plt.plot(frequencias, np.abs(transformada))
plt.xlim(0, 2000)
plt.title("Gráfico transformada de Fourier")
plt.show()
