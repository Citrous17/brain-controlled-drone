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
from Utilities import SERIAL_PORT, BAUD_RATE, SAMPLE_RATE, BUFFER_SIZE, DELTA, THETA, ALPHA, BETA, GAMMA
eeg_buffer = [] 

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
        VALUES (?, ?, ?, ?)
    ''', (timestamp, alpha_power, beta_power, action))
    conn.commit()
    conn.close()