import socket
import sys
import os

# Choose the port from the command line
port = int(sys.argv[1])


# -------- Listening Socket --------
# Create the server's listening socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind(("0.0.0.0", port))

# Listen for incoming connections
server_socket.listen(5)


while True:

    # -------- Connection Socket --------
    # Accept a new client connection
    client_socket, client_address = server_socket.accept()

    # Create a new process for this client
    pid = os.fork()

    if pid == 0:
        # -------- Child Process --------
        # The child handles communication with this client.

        # Child does not need the listening socket
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

        # Child process should terminate
        os._exit(0)

    else:
        # -------- Parent Process --------
        # Parent does not communicate with this client.
        # The child process is handling it.

        client_socket.close()

        # Parent continues the loop and accepts another client.