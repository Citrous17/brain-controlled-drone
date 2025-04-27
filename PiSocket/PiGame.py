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
from tensorflow.keras.models import load_model
from Utilities import SERIAL_PORT, BAUD_RATE, SAMPLE_RATE, BUFFER_SIZE, DELTA, THETA, ALPHA, BETA, GAMMA, USE_MODEL, INSERT_INTO_DB, USE_ALGORIHITHM, BETA_THRESHOLD
# =============================
# EEG / PiCode Configuration
# =============================
# This should be dependent on the device used to analyze the EEG DATA
# The SERIAL_PORT can change based on the Aduino connection
# If running on the Raspberry Pi, the SERIAL_PORT can be /dev/ttyACM0 or /dev/ttyACM1
# If it is running on the Windows 11 machine, the SERIAL_PORT can be COM3 or COM4
eeg_buffer = [] 

# Global variable for paddle movement:
#   -1 for move up, 1 for move down, 0 for still.
paddle_command = 0
action = "none"

buffer_lock = threading.Lock()  # To protect shared data

if USE_MODEL:
    model = load_model("eeg_action_model_tf.keras")

    # Load the scaler and action mapping
    scaler = joblib.load("scaler.pkl")
    action_to_index = joblib.load("action_to_index.pkl")
    index_to_action = {v: k for k, v in action_to_index.items()}

# Setup serial connection for EEG (if available)
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
    """
    Insert a new log record into the database.
    
    Args:
        timestamp: Timestamp of the log entry.
        alpha_power: Computed alpha band power.
        beta_power: Computed beta band power.
        gamma_power: Computed gamma band power.
        delta_power: Computed delta band power.
        theta_power: Computed theta band power.
        action: A string representing the user action (e.g., "up", "down", "none").
        db_file: SQLite database file name.
    """
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
    """
    Process the EEG buffer periodically. Determine which band is dominant:
      - Alpha (8-13 Hz): If alpha power is strong, move paddle up, if it is small, move paddle down.
      - Otherwise: no movement
    Updates global variable `paddle_command`.
    """
    global paddle_command
    global action
    while True:
        time.sleep(1)  # Process every second (adjust as needed)
        with buffer_lock:
            if len(eeg_buffer) < BUFFER_SIZE:
                continue  # Not enough data yet
            data = np.array(eeg_buffer[-BUFFER_SIZE:])
        
        freq, fft_vals = compute_fft(data, SAMPLE_RATE)
        if freq is None or fft_vals is None:
            continue
        
        # Define frequency band:
        # Alpha band (8-13 Hz)
        # Beta band (13-30 Hz)
        
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
        
        # Debug output
        print(f"Alpha Power: {alpha_power:.6f}, Beta power: {beta_power:.6f}, Gamma power: {gamma_power:.2f}, Delta power: {delta_power:.2f}, Theta power: {theta_power:.2f}")

        # Use ML model to predict action
        if USE_ALGORIHITHM:
            try:
                if(beta_power > BETA_THRESHOLD):
                    action = "up"
                    paddle_command = -1
                elif(beta_power < BETA_THRESHOLD):
                    action = "down"
                    paddle_command = 1
                else:
                    action = "none"
                    paddle_command = 0
            except Exception as e:
                print("Prediction error:", e)
        
        # Determine dominant band
        # The threshold value should be adjusted based on the EEG device and environment

        # Log the EEG features and action to the database.
        if INSERT_INTO_DB:
            # Log the data to the database
            log_data_to_db(alpha_power, beta_power, gamma_power, delta_power, theta_power, action, db_file="eeg_data.db")
# Start EEG data reading and processing threads (if serial is available)
if ser:
    threading.Thread(target=read_eeg, daemon=True).start()
threading.Thread(target=process_eeg, daemon=True).start()

# =============================
# Pong Game Setup (Pong.py)
# =============================
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with EEG Control")
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15

# Paddle positions (player is left, opponent is right)
player_x = 20
player_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
opponent_x = WIDTH - 20 - PADDLE_WIDTH
opponent_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Ball starting position and velocity
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = random.choice([-4, 4])
ball_speed_y = random.choice([-4, 4])

# Scores
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 74)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # EEG-controlled paddle movement logic:
    # If EEG suggests upward movement, move up; if downward, move down.
    if paddle_command == -1 and player_y > 0:
        player_y -= 5
    elif paddle_command == 1 and player_y < HEIGHT - PADDLE_HEIGHT:
        player_y += 5

    # Still allow keyboard control for testing:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_y > 0:
        player_y -= 5
        action = "up"
    if keys[pygame.K_s] and player_y < HEIGHT - PADDLE_HEIGHT:
        player_y += 5
        action = "down"

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce off top and bottom
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_speed_y *= -1

    # Bounce off paddles
    if (ball_x <= player_x + PADDLE_WIDTH and
        player_y < ball_y + BALL_SIZE and
        player_y + PADDLE_HEIGHT > ball_y):
        ball_speed_x *= -1
    if (ball_x + BALL_SIZE >= opponent_x and
        opponent_y < ball_y + BALL_SIZE and
        opponent_y + PADDLE_HEIGHT > ball_y):
        ball_speed_x *= -1

    # Basic opponent AI: follow the ball
    if opponent_y + PADDLE_HEIGHT / 2 < ball_y:
        opponent_y += 3
    elif opponent_y + PADDLE_HEIGHT / 2 > ball_y:
        opponent_y -= 3

    # Reset ball if it goes off screen
    if ball_x < 0:
        opponent_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x = random.choice([-4, 4])
        ball_speed_y = random.choice([-4, 4])
    elif ball_x > WIDTH:
        player_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x = random.choice([-4, 4])
        ball_speed_y = random.choice([-4, 4])

    # Drawing
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (opponent_x, opponent_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, (255, 255, 255), (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw scores
    score_text = font.render(f"{player_score}    {opponent_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
