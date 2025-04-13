import pygame
import sys
import random
import threading
import time
import numpy as np
import serial
import scipy.signal as signal
import sqlite3
import joblib
from Utilities import SERIAL_PORT, BAUD_RATE, SAMPLE_RATE, BUFFER_SIZE, DELTA, THETA, ALPHA, BETA, GAMMA
eeg_buffer = [] 
buffer_lock = threading.Lock()
action = None  # Global action state


try:
    print("Attempting to open serial port...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow time for the device to reset
    print("EEG Serial connection established")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    ser = None

def init_db(db_file="eeg_data.db"):
    """Initialize the SQLite database and create table if it doesn't exist."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eeg_keypress_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            alpha_power REAL,
            beta_power REAL,
            gamma_power REAL,
            delta_power REAL,
            theta_power REAL,
            action TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database (creates file and table if not present)
init_db("eeg_data.db")

def log_data_to_db(alpha_power, beta_power, gamma_power, delta_power, theta_power, action, db_file="eeg_data.db"):
    timestamp = time.time()
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO eeg_keypress_log (timestamp, alpha_power, beta_power, gamma_power, delta_power, theta_power, action)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, alpha_power, beta_power, gamma_power, delta_power, theta_power, action))
    conn.commit()
    conn.close()


def read_eeg():
    """ Continuously read EEG data from the serial port and store in eeg_buffer """
    global eeg_buffer
    while True:
        if ser and ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                # Assume the device sends a single integer per line.
                sample = int(line)
                with buffer_lock:
                    eeg_buffer.append(sample)
                    if len(eeg_buffer) > BUFFER_SIZE:
                        eeg_buffer = eeg_buffer[-BUFFER_SIZE:]
            except Exception as e:
                print(f"Error reading/parsing EEG data: {e}")
        else:
            time.sleep(0.005)

def compute_fft(signal_data, sampling_rate):
    """ Compute FFT of the signal and return frequency bins and magnitudes """
    n = len(signal_data)
    if n == 0:
        return None, None
    freq = np.fft.rfftfreq(n, d=1/sampling_rate)
    fft_values = np.abs(np.fft.rfft(signal_data)) / (n / 2)
    return freq, fft_values

def process_eeg():
    global paddle_command
    global action
    while True:
        time.sleep(1)  # Process every second
        with buffer_lock:
            if len(eeg_buffer) < BUFFER_SIZE:
                continue
            data = np.array(eeg_buffer[-BUFFER_SIZE:])
        
        freq, fft_vals = compute_fft(data, SAMPLE_RATE)
        if freq is None or fft_vals is None:
            continue

        alpha_mask = (freq >= ALPHA[0]) & (freq <= ALPHA[1])
        beta_mask = (freq >= BETA[0]) & (freq <= BETA[1])
        gamma_mask = (freq >= GAMMA[0]) & (freq <= GAMMA[1])
        delta_mask = (freq >= DELTA[0]) & (freq <= DELTA[1])
        theta_mask = (freq >= THETA[0]) & (freq <= THETA[1])

        alpha_power = np.sum(fft_vals[alpha_mask])
        beta_power = np.sum(fft_vals[beta_mask])
        gamma_power = np.sum(fft_vals[gamma_mask])
        delta_power = np.sum(fft_vals[delta_mask])
        theta_power = np.sum(fft_vals[theta_mask])

        print(f"Alpha Power: {alpha_power:.2f}, Beta power: {beta_power:.2f}, Gamma power: {gamma_power:.2f}, Delta power: {delta_power:.2f}, Theta power: {theta_power:.2f}")

if ser:
    threading.Thread(target=read_eeg, daemon=True).start()
threading.Thread(target=process_eeg, daemon=True).start()

def start_key_listener():
    global action

    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("EEG Data Recorder")
    font = pygame.font.SysFont(None, 36)

    running = True
    active_action = None

    while running:
        screen.fill((255, 255, 255))
        text = font.render(f"State: {active_action or 'Idle'}", True, (0, 0, 0))
        screen.blit(text, (50, 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            active_action = "focus"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            active_action = "relax"
        else:
            active_action = None

        # Update global action state
        action = active_action

        if active_action:
            with buffer_lock:
                if len(eeg_buffer) >= BUFFER_SIZE:
                    data = np.array(eeg_buffer[-BUFFER_SIZE:])
                else:
                    continue

            freq, fft_vals = compute_fft(data, SAMPLE_RATE)
            if freq is None or fft_vals is None:
                continue

            alpha_mask = (freq >= ALPHA[0]) & (freq <= ALPHA[1])
            beta_mask = (freq >= BETA[0]) & (freq <= BETA[1])
            gamma_mask = (freq >= GAMMA[0]) & (freq <= GAMMA[1])
            delta_mask = (freq >= DELTA[0]) & (freq <= DELTA[1])
            theta_mask = (freq >= THETA[0]) & (freq <= THETA[1])

            alpha_power = np.sum(fft_vals[alpha_mask])
            beta_power = np.sum(fft_vals[beta_mask])
            gamma_power = np.sum(fft_vals[gamma_mask])
            delta_power = np.sum(fft_vals[delta_mask])
            theta_power = np.sum(fft_vals[theta_mask])

            log_data_to_db(alpha_power, beta_power, gamma_power, delta_power, theta_power, active_action)

        pygame.time.delay(200)

    pygame.quit()

    
if __name__ == "__main__":
    # Start EEG reading thread

    # Start GUI + Keypress listener
    start_key_listener()
