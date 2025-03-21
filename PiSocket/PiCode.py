import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from collections import deque
import csv

# Serial Configuration
SERIAL_PORT = "/dev/ttyACM1"	
BAUD_RATE = 115200
SAMPLE_RATE = 550
BUFFER_SIZE = 1024
data_buffer = deque(maxlen=BUFFER_SIZE)

# Open serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Give Arduino time to reset
    print("✅ Serial connection established")
except serial.SerialException as e:
    print(f"❌ Error opening serial port: {e}")
    exit()

# ✅ Define read_serial() function
def read_serial():
    """ Reads data from Arduino via Serial """
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                data_buffer.append(int(line))
                print(int(line))
        else:
            time.sleep(0.01)  # Avoid excessive CPU usage


def compute_fft(signal, sampling_rate):
    """ Compute FFT of the signal and return raw amplitude values scaled correctly """
    print("⚡ Running FFT...")
    n = len(signal)
    freq = np.fft.rfftfreq(n, d=1/sampling_rate)  # Frequency bins
    
    # FFT magnitude
    fft_values = np.abs(np.fft.rfft(signal)) / (n / 2)  # Normalize the magnitude to get correct amplitude
   
    # Displaying the frequency and corresponding raw amplitude
    for i, f in enumerate(freq):
        print(f"Frequency: {f:.2f} Hz, Amplitude: {fft_values[i]:.2f}")

    return freq, fft_values

def save_fft_to_csv(freq, fft_values, filename="fft_data.csv"):
    """ Save FFT frequency and amplitude data to a CSV file """
    print(f"📂 Saving FFT data to {filename}...")
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frequency (Hz)", "Amplitude"])
        for f, amp in zip(freq, fft_values):
            writer.writerow([f, amp])
    
    print(f"✅ FFT data saved to {filename}")

def calibrate_amplitude(frequency, raw_amplitude):
    """ Calibrate the raw amplitude based on frequency """
    # Here you can add custom logic to scale by a known reference point
    # If you have a known calibration factor, apply it here.
    # For example, let's assume a reference gain for 20 Hz signal:
    reference_amplitude = 2000  # 20 mVpp for 20 Hz signal as an example
    calibrated_amplitude = raw_amplitude * (reference_amplitude / raw_amplitude)
    return calibrated_amplitude


def extract_bands(freq, fft_values, calibration=False):
    """ Extract EEG Power Bands from FFT with optional calibration """
    print("📊 Extracting EEG Bands...")
    bands = {
        "Delta (0.5-4 Hz)": (0.5, 4),
        "Theta (4-8 Hz)": (4, 8),
        "Alpha (8-13 Hz)": (8, 13),
        "Beta (13-30 Hz)": (13, 30),
        "Gamma (30-55 Hz)": (30, 55),
    }
    
    # Apply calibration if required (for power calculation)
    if calibration:
        fft_values = np.array([calibrate_amplitude(f, amp) for f, amp in zip(freq, fft_values)])
    
    power = {}
    for band, (low, high) in bands.items():
        mask = (freq >= low) & (freq <= high)  # ✅ Fix: Use & instead of 'and'
        power[band] = np.sum(fft_values[mask])  # ✅ This now works
    return power


def plot_fft(freq, fft_values, power_bands):
    """ Plots FFT Spectrum and EEG Band Power """
    print("📈 Plotting FFT and EEG Bands...")
    plt.figure(figsize=(10, 5))

    # FFT Spectrum (raw data, no calibration applied here)
    plt.subplot(1, 2, 1)
    plt.plot(freq, fft_values, color='blue')
    plt.xlim(0, 60)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("FFT Spectrum")

    # EEG Band Powers (calibrated if required)
    plt.subplot(1, 2, 2)
    bands = list(power_bands.keys())
    values = list(power_bands.values())
    plt.bar(bands, values, color=['red', 'green', 'blue', 'purple', 'orange'])
    plt.xlabel("EEG Bands")
    plt.ylabel("Power")
    plt.title("EEG Power Distribution")

    plt.tight_layout()
    plt.savefig("fft_plot.png")  # Save as image
    print("✅ Plot saved as fft_plot.png")
    save_fft_to_csv(freq, fft_values)
    reconstruct_signal(freq, fft_values, SAMPLE_RATE)
    plt.show()

def reconstruct_signal(freq, fft_values, sampling_rate):
    """ Reconstruct the signal from the FFT magnitude data """
    print("🔄 Reconstructing signal from FFT data...")
    
    # Create complex FFT values (amplitude * e^(j*phase), assuming zero phase for simplicity)
    fft_complex = fft_values * np.exp(1j * np.zeros_like(fft_values))  # Assuming zero phase
    
    # Reconstruct signal using IFFT
    reconstructed_signal = np.fft.irfft(fft_complex)
    
    # Plot the reconstructed signal
    plt.figure(figsize=(10, 5))
    plt.plot(reconstructed_signal)
    plt.title("Reconstructed Signal")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.show()
    
    return reconstructed_signal

if __name__ == "__main__":
    print("🚀 Script started!")

    # ✅ Start Serial Reading Thread
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()
    print("✅ Serial reading thread started!")

    # ✅ Main loop
    while True:
        print(f"🛠 Buffer Size: {len(data_buffer)}")
        if len(data_buffer) >= BUFFER_SIZE:
            signal = np.array(data_buffer)
            freq, fft_values = compute_fft(signal, SAMPLE_RATE)
            power_bands = extract_bands(freq, fft_values)
            plot_fft(freq, fft_values, power_bands)

            data_buffer.clear()  # Reset buffer after processing
            time.sleep(1)  # Update every second
