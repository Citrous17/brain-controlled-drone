import socket
import time

def receive_file():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("169.254.194.84", 5000))  # Connect to Raspberry Pi

    with open("received_large_file.txt", "wb") as f:
        start_time = time.time()  # Start timing
        total_bytes = 0

        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            f.write(data)
            total_bytes += len(data)

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time

    print(f"File received successfully in {elapsed_time:.2f} seconds.")
    print(f"Total data received: {total_bytes / (1024 * 1024):.2f} MB")
    print(f"Transfer speed: {total_bytes / (1024 * 1024) / elapsed_time:.2f} MB/s")

    client_socket.close()

receive_file()
