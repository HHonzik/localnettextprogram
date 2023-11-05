import tkinter as tk
from tkinter import filedialog
import socket
import threading
import os


class TextAppGUI:
    def __init__(self, root):

        self.username = ""
        self.root = root
        self.root.title("Text App GUI")

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect_to_server)
        self.connect_button.pack()

        self.text_area = tk.Text(self.root, state="disabled")
        self.text_area.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.root, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)

        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack()

        self.send_message_button = tk.Button(self.root, text="Send Message", command=self.send_message)
        self.send_message_button.pack()

    
        self.message_entry.config(state=tk.DISABLED)
        self.send_message_button.config(state=tk.DISABLED)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_socket.connect(("192.168.50.36", 12695))

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def connect_to_server(self):
        self.username = self.username_entry.get()
        self.tmpvar1 = "SERVER"
        self.tmp1var = "User " + self.username + " has connected!!"
        self.message_socket.send(f"MESSAGE\n{self.tmpvar1}\n{self.tmp1var}".encode("utf-8"))
        del(self.tmpvar1)
        del(self.tmp1var)
        self.message_entry.delete(0, tk.END)
        self.connect_button.config(state=tk.DISABLED)
        self.username_entry.config(state=tk.DISABLED)
        self.message_entry.config(state=tk.NORMAL)
        self.send_message_button.config(state=tk.NORMAL)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.message_socket.send(f"MESSAGE\n{self.username}\n{message}".encode("utf-8"))
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.message_socket.recv(1024).decode("utf-8")
                self.text_area.config(state=tk.NORMAL)  # Enable editing temporarily
                self.text_area.delete(1.0, tk.END)  # Clear existing content
                self.text_area.insert(tk.END, data)
                self.text_area.config(state=tk.DISABLED)  # Disable editing again
            except:
                break

    def on_closing(self):
        self.tmpvar1 = "SERVER"
        self.tmp1var = "User " + self.username + " has disconnected!!"
        self.message_socket.send(f"MESSAGE\n{self.tmpvar1}\n{self.tmp1var}".encode("utf-8"))
        self.message_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextAppGUI(root)
    root.mainloop()
