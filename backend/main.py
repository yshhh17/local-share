import socket
import os
import threading
from discovery_handler import start_listening
from discovery_handler import send_broadcast

def conn_handler(conn, addr):
    f = open("../frontend/index.html", "r")
    html = f.read()
    f.close()

    print(f"connection from {addr}")

    request = conn.recv(1024).decode('utf-8')
    print(f"request: {request}")

    if not request:
        conn.close()
        return

    request_line = request.splitlines()[0]
    parts = request_line.split()

    if len(parts) < 2:
        conn.close()
        return

    method, path = parts[0], parts[1]

    if method == 'GET':
        if path == '/':
            response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(html)}\r\n"
                    "\r\n"
                    + html
                    ).encode()
            conn.sendall(response)

        elif path == '/style.css':
            f = open("../frontend/style.css", "r")
            css = f.read()
            f.close()
            response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/css\r\n"
                    f"Content-Length: {len(css)}\r\n"
                    "\r\n"
                    + css
                    ).encode()
            conn.sendall(response)

        elif path == '/script.js':
            f = open("../frontend/script.js", "r")
            js = f.read()
            f.close

            response = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Type: application/javascript\r\n"
                    "Content-Length: {len(js)}\r\n"
                    "\r\n"
                    + js
                    ).encode()
            conn.sendall(response)

        elif path == '/api/discovery':
            devices_list = send_broadcast()
            if devices_list and isinstance(devices_list, (list, tuple)):
                result = ', '.join(str(device) for device in devices_list)
            else:
                result = "no devices found or error finding devices..."
            body = f"<html><body><h1> here is the list of the ip's you were looking for: {result}</h1></body></html>"
            response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "\r\n"
                    + body
                    ).encode()
            conn.sendall(response)

    else:
        body = b"ERROR 404 Not Found"
        response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(html)}\r\n"
                "\r\n").encode() + body
        conn.sendall(response)

    conn.close()

HOST = '0.0.0.0'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

th = threading.Thread(target = start_listening, daemon = True)
th.start()

print(f"server is running on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    t = threading.Thread(target = conn_handler, args = (conn, addr))
    t.start()
