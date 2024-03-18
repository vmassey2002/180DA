import numpy as np
import matplotlib.pyplot as plt

# Define the range of frequencies (omega)
omega = np.logspace(-2, 2, 400)  # Frequency range from 0.01 to 100

# Define the function
def transfer_function(w):
    numerator = 0.5j * w
    denominator = -w**2 + 1j * w + 1
    return numerator / denominator

# Calculate magnitude (in dB) and phase (in degrees)
magnitude = 20 * np.log10(np.abs(transfer_function(omega)))
phase = np.angle(transfer_function(omega), deg=True)

# Plot the Bode plot
plt.figure(figsize=(10, 6))

# Magnitude plot
plt.subplot(2, 1, 1)
plt.semilogx(omega, magnitude)
plt.title('Bode Plot')
plt.ylabel('Magnitude (dB)')
plt.grid(True)

# Phase plot
plt.subplot(2, 1, 2)
plt.semilogx(omega, phase)
plt.xlabel('Frequency (log scale)')
plt.ylabel('Phase (degrees)')
plt.grid(True)

plt.show()
