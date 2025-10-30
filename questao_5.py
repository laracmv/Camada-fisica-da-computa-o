import numpy as np
from scipy.signal import iirpeak, freqz, TransferFunction
import matplotlib.pyplot as plt

# Parameters
fs = 44100              # Sampling rate (Hz)
f0 = 2000               # Center frequency (Hz)
Q = 3                # Quality factor

# Design band-pass filter using iirpeak (biquad)
b, a = iirpeak(w0=f0/(fs/2), Q=Q)  # Normalized frequency (f0 / Nyquist)

# Optional: Create TransferFunction object (discrete system)
# Note: 'dt=1/fs' makes it a discrete-time system
tf = TransferFunction(b, a, dt=1/fs)

print(tf)

# Frequency response plot ... Bode
w, h = freqz(b, a, fs=fs)
plt.semilogx(w, 20 * np.log10(abs(h)))
plt.title('Band-Pass Filter Frequency Response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude [dB]')
plt.grid(which='both', linestyle='--', linewidth=0.5)
plt.axvline(f0, color='red', linestyle=':', label='Center Frequency')
plt.legend()
plt.tight_layout()
plt.show()
