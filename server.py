import os
import socket
import threading
import datetime

class TextAppServer:
    def __init__(self):
        self.message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_socket.bind(("0.0.0.0", 12695))
        self.message_socket.listen()

        self.clients = []

        self.text_content = ""

        self.message_thread = threading.Thread(target=self.accept_message_connections)

        self.message_thread.start()

    def accept_message_connections(self):
        while True:
            client_socket, _ = self.message_socket.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_message_client, args=(client_socket,)).start()

    def handle_message_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if message.startswith("MESSAGE"):
                    username, content = message[8:].split("\n", 1)
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.text_content += f"{username} ({timestamp}): {content}\n"
                    self.send_updated_text()
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break

    def send_updated_text(self):
        for client_socket in self.clients:
            try:
                client_socket.send(self.text_content.encode("utf-8"))
            except:
                pass


if __name__ == "__main__":
    server = TextAppServer()
    print("Message server listening on 0.0.0.0:12695")