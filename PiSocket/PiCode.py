import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from collections import deque
import csv

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

SERIAL_PORT = "COM7"	
SERIAL_SLEEP_TIME = 0.01
REALTIME_WAVEFORM_SLEEP_TIME = 0.01
REALTIME_WAVEFORM_RANGE = 128
BAUD_RATE = 115200
SAMPLE_RATE = 700
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

def notch_filter(data, notch_freq=60.0, quality_factor=30.0, sample_rate=SAMPLE_RATE):
    """ Apply a notch filter to remove powerline noise (e.g., 60Hz) """
    nyquist = 0.5 * sample_rate
    norm_freq = notch_freq / nyquist
    b, a = signal.iirnotch(norm_freq, quality_factor)
    return signal.filtfilt(b, a, data)


def moving_average(data, window_size=5):
    return np.convolve(data, np.ones(window_size)/window_size, mode='same')


def reject_artifacts(signal, threshold_factor=3):
    mean = np.mean(signal)
    std = np.std(signal)
    mask = np.abs(signal - mean) < threshold_factor * std
    return signal[mask]

def highpass_filter(data, cutoff=1.0, sample_rate=SAMPLE_RATE):
    nyquist = 0.5 * sample_rate
    norm_cutoff = cutoff / nyquist
    b, a = signal.butter(4, norm_cutoff, btype='high')
    return signal.filtfilt(b, a, data)

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
    DELTA = (0.5, 4)
    THETA = (4, 8)
    ALPHA = (8, 13)
    BETA = (13, 30)
    GAMMA = (30, 55)
    
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
                "delta": apply_filter(data_buffer, DELTA) /5,
                "theta": apply_filter(data_buffer, THETA) / 5,
                "alpha": apply_filter(data_buffer, ALPHA)/5,
                "beta": apply_filter(data_buffer, BETA)/5,
                "gamma": apply_filter(data_buffer, GAMMA)/5,
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
    print("🚀 Script started!")

    # ✅ Start Serial Reading Thread
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()
    print("Serial reading thread started!")
    
    plot_realtime_waveform()
    print("Waveform plotting thread started!")
    bands = {
        "delta": (0.5, 4),
        "theta": (4, 8),
        "alpha": (8, 13),
        "beta": (13, 30),
        "gamma": (30, 55)
    }

    while True:
        print(f"🛠 Buffer Size: {len(data_buffer)}")
        if len(data_buffer) >= BUFFER_SIZE:
            # Convert buffer to NumPy array
            raw_signal = np.array(data_buffer)

            # Compute mean and standard deviation
            mean = np.mean(raw_signal)
            std = np.std(raw_signal)

            raw_signal = highpass_filter(raw_signal, cutoff=1.0)

            # Apply 3σ clipping
            filtered_signal = reject_artifacts(raw_signal)
            filtered_signal = notch_filter(filtered_signal)

            # Analyze filtered signal by frequency bands
            filtered_data = {}

            for band, (low, high) in bands.items():
                filtered_data[band] = apply_filter(filtered_signal, (low, high), SAMPLE_RATE)
                filtered_data[band] = moving_average(filtered_data[band], window_size=5)


            print(f"Original size: {len(raw_signal)}, After 3σ filtering: {len(filtered_signal)}")

            # Ensure we have enough samples left after outlier removal
            if len(filtered_signal) > 10:
                # Compute FFT on the cleaned signal
                freq, fft_values = compute_fft(filtered_signal, SAMPLE_RATE)

                # Normalize FFT data (optional, depending on use-case)
                freq, normalized_fft = normalize_fft_with_csv(freq, fft_values)

                # Save FFT data to CSV
                save_fft_to_csv(freq, normalized_fft)

                # Insert FFT data into SQLite DB
                insert_fft_into_db(freq, normalized_fft)

            # Clear the buffer after processing
            data_buffer.clear()
            time.sleep(1)  # Wait before next read
