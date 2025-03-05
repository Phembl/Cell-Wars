import socket, threading, json, time

class NetworkManager:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.connection = None
        self.address = None
        self.receive_thread = None
        self.running = False
        self.message_queue = []
        self.default_port = 5555

    def send_message(self, message):
        """
        Send a message to the connected peer.
        """

        if not self.connected:
            print("Can't send message - Not connected to a peer.")
            return False

        try:
            # Convert message to JSON and encode to bytes
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')

            # Add message length as heads (4 bytes)
            # The header contains the length of the message and is necessary so that receiver can allocate the space
            message_length = len(message_bytes)
            header = message_length.to_bytes(4, byteorder='big')

            # Send header followed by message
            if isinstance(self.connection, socket.socket):
                self.connection.sendall(header + message_bytes)
            else:
                self.socket.sendall(header + message_bytes)
            return True

        except Exception as e:
            print(f"Error sending message {e}")
            self.disconnet()
            return False

    def receive_message(self):
        """
        Background thread to receive a message from the connected peer.
        """

        connection = self.connection if isinstance(self.connection, socket.socket) else self.socket

        while self.running:
            try:
                # Read message length from header (4 bytes)
                header = connection.recv(4)
                if not header:
                    break

                message_length = int.from_bytes(header, byteorder='big')

                # Read the actual message
                message_bytes = connection.recv(message_length)
                if not message_bytes:
                    break

                # Decode and parse the message
                message_json = message_bytes.decode('utf-8')
                message = json.loads(message_json)

                # Add to queue for processing
                self.message_queue.append(message)

            except Exception as e:
                print(f"Error receiving message {e}")
                break

        self.disconnect()

    def get_next_message(self):
        """
        Get the next message from the message queue.
        """

        if self.message_queue:
            return self.message_queue.pop(0)
        return None

    def disconnect(self):
        """
        Disconnect from the network.
        """

        self.running = False
        self.connected = False

        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        if self.connection and isinstance(self.connection, socket.socket):
            try:
                self.connection.close()
            except:
                pass
            self.connection = None

        print("Disconnected from network")

class NetworkHost (NetworkManager):
    """
    Network manager for the game host.
    """

    def host_game(self, port = None):
        """
        Host a game on the specified port.
        """

        if not port:
            port = self.default_port

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('', port)) # Empty string = all available interfaces
            self.socket.listen(1) # Only accept one connection

            print(f"Hosting game on port {port}")
            print(f"Your IP adress: {socket.gethostbyname(socket.gethostname())}")

            # Accept client connection (this blocks until a client connects)
            self.connection, self.address = self.socket.accept()
            self.connected = True
            self.running = True

            print(f"Client connected fromt {self.address}")

            # Start background thread to receive messages
            self.receive_thread = threading.Thread(target=self.receive_message)
            self.receive_thread.daemon = True
            self.receive_thread.start()

            return True

        except Exception as e:
            print(f"Error hosting game {e}")
            self.disconnect()
            return False

class NetworkClient(NetworkManager):
    """
    Network manager for the game client.
    """

    def join_game(self, host_ip, port = None):
        """
        Join a game at the specified host IP and port.
        """

        if not port:
            port = self.default_port

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host_ip, port))
            self.connected = True
            self.running = True

            print(f"Conneted to host at {host_ip}:{port}")

            # Start background Thread to receive messages
            self.receive_thread = threading.Thread(target=self.receive_message)
            self.receive_thread.daemon
            self.receive_thread.start()

            return True

        except Exception as e:
            print(f"Error joining game {e}")
            self.disconnect()
            return False


# ==== NEED TO FIND OUT WHAT THIS MEANS ==== #
# Example usage:
if __name__ == "__main__":
    # This code only runs if you execute network.py directly
    # It's a simple test of the networking functionality

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "host":
        # Run as host
        host = NetworkHost()
        if host.host_game():
            print("Hosting game. Press Enter to send a test message.")
            input()
            host.send_message({"type": "test", "content": "Hello from host!"})

            # Wait for a response
            while host.connected:
                message = host.get_next_message()
                if message:
                    print(f"Received: {message}")
                time.sleep(0.1)
    else:
        # Run as client
        client = NetworkClient()
        host_ip = input("Enter host IP: ")
        if client.join_game(host_ip):
            print("Connected to host. Waiting for messages...")

            # Wait for messages
            while client.connected:
                message = client.get_next_message()
                if message:
                    print(f"Received: {message}")
                    # Respond
                    client.send_message({"type": "response", "content": "Hello from client!"})
                time.sleep(0.1)