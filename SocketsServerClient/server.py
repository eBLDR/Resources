import socket
import threading


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.recv_buffer = 4096
        self.encoding = 'utf-8'
        self.max_clients = 10

        self.connections = []
        # To avoid concurrency issues
        self.connections_lock = threading.Lock()

        self.server_socket = None

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self.server_socket = server_socket

            self.server_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )

            try:
                self.server_socket.bind((self.host, self.port))
            except socket.error as e:
                print('Bind failed. Error: {}'.format(e))
                raise e

            self.server_socket.listen(self.max_clients)

            self.connections.append(self.server_socket)

            print('Chat server started on {}.'.format(self.server_socket.getsockname()))

            while True:
                connection, address = self.server_socket.accept()
                threading.Thread(
                    target=self.client_thread, args=(connection,)
                ).start()

    def client_thread(self, conn):
        self.client_connected(conn)
        while True:
            data = conn.recv(self.recv_buffer)
            if not data:
                # Received 0 bytes, connection on the other side has closed
                self.client_disconnected(conn)
                break

            # Manage here what the server will respond to the client depending
            # on the data received

            data = '\r<{}> {}'.format(
                str(conn.getpeername()),
                data.decode(self.encoding)
            ).replace('\n', '')
            self.broadcast_data(conn, data)

    def client_connected(self, conn):
        self.connections_lock.acquire()
        self.connections.append(conn)
        self.connections_lock.release()

    def client_disconnected(self, conn):
        self.connections_lock.acquire()
        self.connections.remove(conn)
        conn.close()
        self.connections_lock.release()

    def _send_data(self, conn, data):
        try:
            conn.sendall(data)
        except Exception:
            # Socket connection broken, client has killed its process
            self.client_disconnected(conn)
            raise

    def reply_client(self, client_conn, data):
        """
        Send data to the producer socket.
        :param client_conn: producer
        :param data: data received by producer
        :return: data replied by server
        """
        # Manage reply based on data
        self._send_data(client_conn, data)  # ECHO

    def broadcast_data(self, producer_socket, msg):
        """
        Broadcasts the message to all clients except the master socket (server)
        and the producer (itself).
        :param producer_socket: client that sent the data
        :param msg:
        :return:
        """
        for conn in self.connections:
            if conn != producer_socket and conn != self.server_socket:
                self._send_data(conn, msg)


if __name__ == '__main__':
    # ENV variables
    HOST = '127.0.0.1'
    PORT = 5000

    server = Server(host=HOST, port=PORT)
    server.serve_forever()
