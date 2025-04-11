import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from collections import deque
import csv
import scipy.signal as signal
import sqlite3

# Serial Configuration
# Make sure to change the SERIAL_PORT to the correct port for your Arduino
# The SERIAL_PORT can change based on the Aduino connection
# Another common configuration is /dev/ttyACM1 
# If running on the Windows 11 machine, the SERIAL_PORT can be COM3 or COM4
# The BAUD_RATE is the same as the one used in the Arduino sketch
# The SAMPLE_RATE can be adjusted, a higher rate will give more data but will also
# increase the amount of data to process
# The BUFFER_SIZE is the size of the data buffer, it can be adjusted based on the amount of data
# you want to process at once. A larger buffer will give more data but will also increase the
# amount of data to process

SERIAL_PORT = "COM3"	
SERIAL_SLEEP_TIME = 0.01
REALTIME_WAVEFORM_SLEEP_TIME = 0.01
REALTIME_WAVEFORM_RANGE = 128
BAUD_RATE = 115200
SAMPLE_RATE = 800
BUFFER_SIZE = 1024
data_buffer = deque(maxlen=BUFFER_SIZE)

# Open serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print("Serial connection established")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

def read_serial():
    """ Reads data from Arduino via Serial connection and appends to data_buffer """
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                data_buffer.append(int(line))
        else:
            # Sleep for a short time to avoid busy waiting
            time.sleep(SERIAL_SLEEP_TIME) 

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

def save_fft_to_csv(freq, fft_values, filename="normalized_fft_data.csv"):
    """ Save FFT frequency and normalized amplitude data to a CSV file """
    print(f"Saving normalized FFT data to {filename}...")
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frequency (Hz)", "Normalized Amplitude"])
        for f, amp in zip(freq, fft_values):
            writer.writerow([f, amp])
    
    print(f"Normalized FFT data saved to {filename}")

def apply_filter(data, frequency_range, sample_rate=SAMPLE_RATE):
    """ Apply a band-pass filter to extract the specific frequency range """
    low, high = frequency_range

    # Normalize the frequencies with respect to Nyquist frequency
    nyquist = 0.5 * sample_rate
    low = low / nyquist
    high = high / nyquist

    # Create a Butterworth band-pass filter
    b, a = signal.butter(4, [low, high], btype='band')

    # Apply the filter to the signal
    filtered_data = signal.filtfilt(b, a, data)
    
    return filtered_data

def insert_fft_into_db(freq, fft_values, db_file="fft_data.db"):
    """ Inserts FFT frequency and amplitude data into a SQLite database. """
    print("Inserting FFT data into database...")
    
    # Connect to (or create) the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fft_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            frequency REAL,
            amplitude REAL,
            timestamp REAL
        )
    ''')
    
    timestamp = time.time() 
    # Insert each (frequency, amplitude) pair into the table
    for f, amp in zip(freq, fft_values):
        cursor.execute(
            "INSERT INTO fft_data (frequency, amplitude, timestamp) VALUES (?, ?, ?)",
            (f, amp, timestamp)
        )
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
    print(f"FFT data inserted into database '{db_file}'.")


def read_csv_frequencies(csv_file="scope_0.csv"):
    """ Reads frequencies from the CSV file and returns as a list/array """
    frequencies = []
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            # Assuming that the frequency is in the first column
            try:
                frequencies.append(float(row[0]))
            except ValueError:
                continue  # Skip rows with invalid data
    return np.array(frequencies)
    
def normalize_fft_with_csv(freq, fft_values, csv_file="scope_0.csv"):
    """ Normalize FFT by dividing by corresponding frequency from CSV """
    print("Normalizing FFT using frequencies from CSV...")
    
    csv_frequencies = read_csv_frequencies(csv_file)
    
    # Make sure CSV frequencies and FFT frequencies are the same length
    min_length = min(len(freq), len(csv_frequencies))
    freq = freq[:min_length]
    fft_values = fft_values[:min_length]
    csv_frequencies = csv_frequencies[:min_length]

    # Normalize FFT values by dividing with corresponding frequencies from CSV
    normalized_fft_values = fft_values / csv_frequencies

    return freq, normalized_fft_values / 105.7

    
def plot_realtime_waveform():
    """ Plots the real-time waveform 
        The waveforms are separated by frequency channels:
        Delta (0.5-4 Hz), Theta (4-8 Hz), Alpha (8-13 Hz),
        Beta (13-30 Hz), Gamma (30-55 Hz)
    """
    # Constants for frequency ranges (in Hz)
    DELTA = (2, 3)
    THETA = (3, 5)
    ALPHA = (5.5, 9)
    BETA = (9, 22)
    GAMMA = (22, 35)
    
    # Create a figure with 5 subplots, one for each frequency band
    plt.ion()
    fig, axes = plt.subplots(5, 1, figsize=(10, 10), sharex=True)  # 5 subplots stacked vertically
    axes[0].set_title("Delta (0.5-4 Hz)")
    axes[1].set_title("Theta (4-8 Hz)")
    axes[2].set_title("Alpha (8-13 Hz)")
    axes[3].set_title("Beta (13-30 Hz)")
    axes[4].set_title("Gamma (30-55 Hz)")
    
    # Set common properties for all axes
    for ax in axes:
        ax.set_xlim(0, BUFFER_SIZE)
        ax.set_ylim(-1 * REALTIME_WAVEFORM_RANGE, REALTIME_WAVEFORM_RANGE)
        ax.set_ylabel("Amplitude")
    
    axes[4].set_xlabel("Time")
    
    # Create an initial empty plot for each frequency band with color differentiation
    lines = [ax.plot([], [], color)[0] for ax, color in zip(axes, ['red', 'green', 'blue', 'purple', 'orange'])]
    plot_counter = 0
    while True:
        if len(data_buffer) >= BUFFER_SIZE:
            print("Updating Realtime Waveform")
            # Compute and plot the waveform for each frequency band
            filtered_data = {
                "delta": apply_filter(data_buffer, DELTA),
                "theta": apply_filter(data_buffer, THETA),
                "alpha": apply_filter(data_buffer, ALPHA),
                "beta": apply_filter(data_buffer, BETA),
                "gamma": apply_filter(data_buffer, GAMMA),
            }

            # Ensure there is data to plot
            for band, filtered in filtered_data.items():
                if len(filtered) == 0:
                    continue

                # Update the plot for each channel (frequency band)
                index = {"delta": 0, "theta": 1, "alpha": 2, "beta": 3, "gamma": 4}[band]
                lines[index].set_ydata(filtered)

            for i, ax in enumerate(axes):
                lines[i].set_xdata(np.arange(len(data_buffer)))
                ax.relim()
                ax.autoscale_view()

            fig.canvas.draw()
            
            plot_counter += 1
            fig.canvas.flush_events()
            
            time.sleep(REALTIME_WAVEFORM_SLEEP_TIME)


def save_realtime_waveform(fig, filtered_data, filename="realtime_waveform.png"):
    """ Saves the current plot figure to a file. """
    print(f"Saving real-time waveform picture to {filename}...")
    fig.savefig(filename + ".png")   # Save the figure as a PNG file
    print(f"Saved to {filename}")
    
    print(f"Saving filtered data to {filename}.png ...")
    
    filename = "realtime_waveform_data.csv"
        
    # Open the CSV file in append mode ('a')
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if the file is empty (check if file is new)
        file_empty = file.tell() == 0
        if file_empty:
            writer.writerow(["Timestamp", "Frequency (Hz)", "Amplitude"])
        
        # Append filtered data (with timestamp)
        timestamp = time.time()  # You can adjust the timestamp format as needed
        for band, data in filtered_data.items():
            for i, amplitude in enumerate(data):
                # Write the timestamp, frequency, and amplitude for each filtered data point
                writer.writerow([timestamp, band, amplitude])
    
    print(f"Filtered data saved to {filename}")

if __name__ == "__main__":
    print("Script started!")

    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()
    print("Serial reading thread started!")
    
    plot_realtime_waveform()
    print("Waveform plotting thread started!")

    while True:
        print(f"Buffer Size: {len(data_buffer)}")
        if len(data_buffer) >= BUFFER_SIZE:
            signal = np.array(data_buffer)
            freq, fft_values = compute_fft(signal, SAMPLE_RATE)

            data_buffer.clear()  # Reset buffer after processing
            time.sleep(1)  # Update every second
