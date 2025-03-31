import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from collections import deque
import csv

# Serial Configuration
SERIAL_PORT = "/dev/ttyACM0"	
BAUD_RATE = 115200
SAMPLE_RATE = 550
BUFFER_SIZE = 1024
data_buffer = deque(maxlen=BUFFER_SIZE)

# Open serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Give Arduino time to reset
    print("Serial connection established")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def read_serial():
    """ Reads data from Arduino via Serial """
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                if int(line) < 2 or int(line) > 1020:
                    continue
                data_buffer.append(int(line))
                print(int(line))
        else:
            time.sleep(0.01)  # Avoid excessive CPU usage


def compute_fft(signal, sampling_rate):
    """ Compute FFT of the signal and return raw amplitude values scaled correctly """
    print("Running FFT...")
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
    print(f"Saving FFT data to {filename}...")
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frequency (Hz)", "Amplitude"])
        for f, amp in zip(freq, fft_values):
            writer.writerow([f, amp])
    
    print(f"FFT data saved to {filename}")

def calibrate_amplitude(frequency, raw_amplitude):
    """ Calibrate the raw amplitude based on frequency """
    # Here you can add custom logic to scale by a known reference point
    # If you have a known calibration factor, apply it here.
    # For example, let's assume a reference gain for 20 Hz signal:
    reference_amplitude = 2000  # 20 mVpp for 20 Hz signal as an example
    calibrated_amplitude = raw_amplitude * (reference_amplitude / raw_amplitude)
    return calibrated_amplitude

def plot_realtime_waveform():
    """ Plots the real-time waveform """
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'b')
    ax.set_xlim(0, BUFFER_SIZE)
    ax.set_ylim(0, 1024)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.set_title("Real-Time Waveform")
    
    while True:
        if len(data_buffer) >= BUFFER_SIZE:
            line.set_ydata(list(data_buffer))
            line.set_xdata(np.arange(len(data_buffer)))
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.01)  # Adjust for refresh rate


def extract_bands(freq, fft_values, calibration=False):
    """ Extract EEG Power Bands from FFT with optional calibration """
    print("Extracting EEG Bands...")
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
        mask = (freq >= low) & (freq <= high)
        power[band] = np.sum(fft_values[mask])
    return power


def plot_fft(freq, fft_values, power_bands):
    """ Plots FFT Spectrum and EEG Band Power """
    print("Plotting FFT and EEG Bands...")
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
    print("Plot saved as fft_plot.png")
    save_fft_to_csv(freq, fft_values)
    reconstruct_signal(freq, fft_values, SAMPLE_RATE)
    plt.show()

def reconstruct_signal(freq, fft_values, sampling_rate):
    """ Reconstruct the signal from the FFT magnitude data while ignoring frequencies below 2 Hz and handling phase correctly """
    print("Reconstructing signal from FFT data (with frequency filter)...")
    
    # Mask out frequencies below 2 Hz
    freq_mask = freq >= 8.0
    filtered_freq = freq[freq_mask]
    filtered_fft_values = fft_values[freq_mask]
    
    # Create complex FFT values (magnitude * e^(j*phase)), assume phase is 0 for now (or estimate it)
    # We could also try to create a phase estimate if needed, but for now let's assume zero phase
    phase = np.zeros_like(filtered_fft_values)  # Assumption: Zero phase
    fft_complex = filtered_fft_values * np.exp(1j * phase)  # Using zero phase assumption
    
    # Reconstruct signal using IFFT
    reconstructed_signal = np.fft.irfft(fft_complex)
    
    # Apply a windowing function to the reconstructed signal to reduce edge artifacts (if needed)
    # You can experiment with different windowing functions (like Hamming, Hann, etc.)
    # Here we apply a simple Hamming window to the reconstructed signal:
    window = np.hamming(len(reconstructed_signal))
    reconstructed_signal *= window  # Apply window to reduce edge effects
    
    # Plot the reconstructed signal
    plt.figure(figsize=(10, 5))
    plt.plot(reconstructed_signal)
    plt.title("Reconstructed Signal (with low-frequency filter and windowing)")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.show()
    
    return reconstructed_signal

if __name__ == "__main__":
    print("Script started!")

    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()
    print("Serial reading thread started!")
    
    waveform_thread = threading.Thread(target=plot_realtime_waveform, daemon=True)
    waveform_thread.start()
    print("Waveform plotting thread started!")

    while True:
        print(f"Buffer Size: {len(data_buffer)}")
        if len(data_buffer) >= BUFFER_SIZE:
            if sum(data_buffer) <= 10 or sum(data_buffer) >= 1000000:
                print("Error: Poor Connection detected!")
                data_buffer.clear()
                continue
            signal = np.array(data_buffer)
            freq, fft_values = compute_fft(signal, SAMPLE_RATE)
            power_bands = extract_bands(freq, fft_values)
            #plot_fft(freq, fft_values, power_bands)

            data_buffer.clear()  # Reset buffer after processing
            time.sleep(1)  # Update every second
