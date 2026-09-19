import socket
import sys
import select

# Choose the port from the command line
port = int(sys.argv[1])


# -------- Listening Socket --------
# Create the server's listening socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind(("0.0.0.0", port))

# Listen for incoming connections
server_socket.listen(5)

# Keep track of all sockets that select() should monitor
# Initially, only the server socket is present
sockets = [server_socket]


# -------- Monitor Sockets --------
while True:
    # Wait until one or more sockets are ready to be read
    readable, _, _ = select.select(sockets, [], [])

    # Process every socket that is ready
    for sock in readable:

        # -------- New Client Connection --------
        if sock is server_socket:

            # Accept the new client
            client_socket, client_address = server_socket.accept()

            # Add the new client socket to the list
            sockets.append(client_socket)

        # -------- Existing Client --------
        else:

            # Receive data from the client
            data = sock.recv(256)

            # Client disconnected
            if data == b"":
                sockets.remove(sock)
                sock.close()
                continue

            # Convert bytes to a string
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

            # Send result back to the client
            sock.sendall(str(result).encode())