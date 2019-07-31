import socket
import sys
import select


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.recv_buffer = 4096
        self.encoding = 'utf-8'
        self.timeout = 2

        self.client_socket = None
        self.listening = False

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(self.timeout)

        try:
            self.client_socket.connect((self.host, self.port))
            print('Connected to remote host.')
        except socket.error:
            print('Unable to connect to {}:{}.'.format(self.host, self.port))
            raise

    def listen_for_incoming(self):
        self.listening = True
        while self.listening:
            socket_list = [self.client_socket]
            ready_to_read, ready_to_write, in_error = select.select(
                socket_list, [], []
            )

            for sock in ready_to_read:
                if sock == self.client_socket:
                    # Incoming message from remote server
                    self.incoming_message()

                    # Stop listening upon message is received
                    self.listening = False

    def listen_forever(self):
        while True:
            self.listening = True
            self.listen_for_incoming()

    def incoming_message(self):
        # Incoming messages from remote host
        data = self.client_socket.recv(self.recv_buffer)
        if data:
            print(data.decode(self.encoding))

    def send_data(self, data):
        # Sending messages to remote host
        self.client_socket.sendall(data)
        if b'/exit' in data:
            # Exiting keyword
            self.client_socket.close()
            sys.exit()


if __name__ == '__main__':
    # ENV variables
    HOST = '127.0.0.1'
    PORT = 5000

    client = Client(host=HOST, port=PORT)
    client.connect_to_server()
    client.listen_for_incoming()
