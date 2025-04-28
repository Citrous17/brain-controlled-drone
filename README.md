# (Brain Control Interface) Real-Time EEG Data Processing & Visualization

A powerful tool for processing and visualizing real-time EEG data from Arduino or compatible microcontrollers. This project implements Fast Fourier Transform (FFT) processing, applies frequency band filters for different brainwave types (Delta, Theta, Alpha, Beta, Gamma), and provides real-time visualization. This allows user to control a game, nameley pong, using just their attention spans. This was developed for the Spring 2025 Capstone Project under Dr. Ritchey

## Features

- **Real-time data acquisition** from Arduino via serial connection
- **FFT processing** for frequency domain analysis
- **Bandpass filtering** for isolating brainwave frequency bands
- **Data persistence** to CSV and SQLite database
- **Real-time visualization** of waveforms and brainwave activity
- **Pong game** controlled by brainwave power values

## File Structure

| File | Description |
|------|-------------|
| `main.py` | Main script for data reading, FFT processing, saving results, and visualization |
| `Utilities.py` | Configuration constants and settings |
| `PiCode.py` | Oscilloscope visualization script |
| `PiGame.py` | Brainwave-controlled Pong game |
| `normalized_fft_data.csv` | Auto-generated CSV with normalized FFT amplitude data |

## Function Overview

| Function | Description |
|----------|-------------|
| `read_serial_once()` | Reads a single line from the serial port |
| `read_serial()` | Continuously reads serial data in a background thread |
| `compute_fft(signal, sampling_rate)` | Computes and analyzes FFT of the given signal |
| `save_fft_to_csv(freq, fft_values, filename)` | Saves FFT data to CSV |
| `apply_filter(data, frequency_range, sample_rate)` | Applies a Butterworth bandpass filter |
| `insert_fft_into_db(freq, fft_values, db_file)` | Stores FFT results in SQLite database |
| `read_csv_frequencies(csv_file)` | Reads frequency data from CSV |
| `normalize_fft_with_csv(freq, fft_values, csv_file)` | Normalizes FFT values using CSV reference |
| `remove_outliers(data, threshold)` | Cleans data by removing statistical outliers |
| `plot_realtime_waveform(max_loops=None)` | Plots filtered brainwave bands in real-time |
| `process_data()` | Processes buffer: cleans, performs FFT, resets |

## Getting Started

### Prerequisites

- Python 3.6+
- Arduino (or compatible microcontroller)
- USB connection cable

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Citrous17/brain-controlled-drone.git
   cd brain-controlled-drone
   ```

2. Install required packages:
   ```bash
   pip install pyserial numpy matplotlib scipy
   ```

3. Update the `SERIAL_PORT` in `Utilities.py` to match your Arduino connection
   (e.g., `COM3` on Windows, `/dev/ttyACM0` on Linux)

### Running the Application

#### Oscilloscope Visualization
```bash
python PiCode.py
```

#### Brainwave-Controlled Pong
```bash
python PiGame.py
```

## Configuration

Edit `Utilities.py` to customize the following parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `SERIAL_PORT` | Serial port name | `/dev/ttyACM0` |
| `BAUD_RATE` | Serial communication speed | `9600` |
| `SAMPLE_RATE` | Data acquisition rate (Hz) | `250` |
| `BUFFER_SIZE` | Sample buffer size | `1024` |
| `DELTA` | Delta wave frequency range (Hz) | `(0.5, 4)` |
| `THETA` | Theta wave frequency range (Hz) | `(4, 8)` |
| `ALPHA` | Alpha wave frequency range (Hz) | `(8, 13)` |
| `BETA` | Beta wave frequency range (Hz) | `(13, 30)` |
| `GAMMA` | Gamma wave frequency range (Hz) | `(30, 100)` |

## Brainwave Frequency Bands

| Band | Frequency (Hz) | Associated With |
|------|----------------|----------------|
| Delta | 0.5-4 | Deep sleep, healing |
| Theta | 4-8 | Meditation, memory, creativity |
| Alpha | 8-13 | Relaxation, calmness |
| Beta | 13-30 | Active thinking, focus |
| Gamma | 30-100 | Higher cognitive processing |


Made with ❤️ by Kyle Stallings, Pravar Chetan, Greg Miller, Sam Huang
