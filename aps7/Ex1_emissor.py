frequencia = range(100,1000,10)
fc =500

import numpy as np
import sounddevice as sd  
import matplotlib.pyplot as plt  
from scipy.signal import butter, lfilter

sample_rate = 44100
ordem = 5 #determina o decaimento do filtro, quanto menor, menos acentuado é o decaimento
t = np.arange(stop=2,step=1/sample_rate)

tom = 0

for f in frequencia:
    tom += np.sin(2*np.pi*f*t)

sd.play(tom,sample_rate)
sd.wait()

transformada = np.fft.fft(tom)

frequencias = np.fft.fftfreq(len(transformada),1/sample_rate)

#Filtro passa-baixas 
b_lp, a_lp = butter(N=ordem, Wn= fc/(sample_rate/2), btype='low')
sinal_filtrado = lfilter(b_lp, a_lp, tom)

plt.plot(frequencias, np.abs(transformada), label='Sinal original')
plt.plot(frequencias, np.abs(np.fft.fft(sinal_filtrado)), label='Sinal filtrado passa-baixas', linestyle='--')
plt.xlim(0,2000)
plt.title("Gráfico transformada de fourier")
plt.show()


print("Reproduzindo sinal original...")
sd.play(tom, sample_rate)
sd.wait()

print("Reproduzindo sinal filtrado...")
sd.play(sinal_filtrado, sample_rate)
sd.wait()
