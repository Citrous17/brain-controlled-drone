import socket
import time

def send_file():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("192.168.1.2", 5000))  # Raspberry Pi's IP
    server_socket.listen(1)
    print("Waiting for a connection...")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    with open("large_file.txt", "rb") as f:
        start_time = time.time()  # Start timing
        data = f.read(4096)  # Use a larger buffer for speed
        while data:
            conn.send(data)
            data = f.read(4096)

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time

    print(f"File sent successfully in {elapsed_time:.2f} seconds.")
    conn.close()
    server_socket.close()

send_file()
