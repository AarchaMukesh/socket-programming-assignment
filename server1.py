import socket
import sys

# Choose the port from the command line
port = int(sys.argv[1])

while True:
    # -------- Listening Socket --------
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind(("0.0.0.0", port))

    # Listen for incoming connections
    server_socket.listen(0)

    # -------- Connection Socket --------
    client_socket, client_address = server_socket.accept()

    # No longer accept new clients while this client is being handled
    server_socket.close()

    # -------- Communicate with this client --------
    while True:
        data = client_socket.recv(256)

        # Client disconnected
        if data == b"":
            break

        message = data.decode().strip()

        # Split expression into its components
        parts = message.split(" ")

        num1 = int(parts[0])
        operator = parts[1]
        num2 = int(parts[2])

        # Perform calculation
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            result = num1 // num2

        # Send result to client
        client_socket.sendall(str(result).encode())

    # Client has disconnected
    client_socket.close()

    # Outer loop creates a new listening socket
    # and waits for the next client

# Client 1 connects --> accept --> close listening socket --> communicate with C1 --> C1 disconnects --> close client socket --> outer loop --> create new listening socket --> accept C2   

# When the first client disconnects, server 1 closes its connection socket. 
