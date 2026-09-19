
#!/usr/bin/env python3
import socket
import sys

MAX_INPUT_SIZE = 256


def main():
    if len(sys.argv) < 3:
        print(f"usage {sys.argv[0]} <server-ip-addr> <server-port>", file=sys.stderr)
        sys.exit(0)

    server_ip = sys.argv[1]
    portnum = int(sys.argv[2])

    # Create client socket
    try:
        sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except OSError:
        print("ERROR opening socket", file=sys.stderr)
        sys.exit(1)

    # Connect to server (validates IP and connects)
    try:
        sockfd.connect((server_ip, portnum))
    except OSError:
        print("ERROR connecting", file=sys.stderr)
        sys.exit(1)

    print("Connected to server")

    try:
        while True:
            # Ask user for message to send to server
            inputbuf = input("Please enter the message to the server: ")
            # fgets includes the newline; replicate that behavior
            inputbuf += "\n"

            # Write to server
            try:
                sockfd.sendall(inputbuf.encode())
            except OSError:
                print("ERROR writing to socket", file=sys.stderr)
                sys.exit(1)

            # Read reply
            try:
                data = sockfd.recv(MAX_INPUT_SIZE - 1)
            except OSError:
                print("ERROR reading from socket", file=sys.stderr)
                sys.exit(1)

            print(f"Server replied: {data.decode(errors='replace')}\n")
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        sockfd.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())