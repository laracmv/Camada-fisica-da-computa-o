frequencias_acordes = {
    'do_maior': [523.25, 659.25, 783.99],
    're_menor': [587.33, 698.46, 880.00],
    'mi_menor': [659.25, 783.99, 987.77],
    'fa_maior': [698.46, 880.00, 1046.50],
    'sol_maior': [783.99, 987.77, 1174.66],
    'la_menor': [880.00, 1046.50, 1318.51],
    'si_menor_5b': [493.88, 587.33, 698.46]
}

import numpy as np
import sounddevice as sd  
import matplotlib.pyplot as plt  

sample_rate = 44100
t = np.arange(stop=2,step=1/sample_rate)
i = True
while i:
    print("Escolha um acorde e tecle enter: ")
    print("1 - do maior")
    print("2 - re menor")
    print("3 - mi menor")
    print("4 - fa maior")
    print("5 - sol maior")
    print("6 - la menor")
    print("7 - si menor 5b")
    acorde = input("Dgite o número do acorde: ")

    if acorde == '1':
        acorde = 'do_maior'
        i = False
    elif acorde == '2':
        acorde = 're_menor'
        i = False
    elif acorde == '3':
        acorde = 'mi_menor'
        i = False
    elif acorde == '4':
        acorde = 'fa_maior'
        i = False
    elif acorde == '5':
        acorde = 'sol_maior'
        i = False
    elif acorde == '6':
        acorde = 'la_menor'
        i = False
    elif acorde == '7':
        acorde = 'si_menor_5b' 
        i = False

# sen = sen(2*pi*f*t)
tom= np.sin(2*np.pi*frequencias_acordes[acorde][0]*t) + np.sin(2*np.pi*frequencias_acordes[acorde][1]*t) + np.sin(2*np.pi*frequencias_acordes[acorde][2]*t)

sd.play(tom,sample_rate)
sd.wait()

transformada = np.fft.fft(tom)
print(len(transformada))
frequencias = np.fft.fftfreq(len(transformada),1/sample_rate)

plt.plot(t,tom)
plt.title("Gráfico frequencias somada x tempo")
plt.show()

plt.plot(frequencias, np.abs(transformada))
plt.xlim(0,2000)
plt.title("Gráfico transformada de fourier")
plt.show()