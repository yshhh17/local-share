import socket
import os
import threading

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

print(f"server is running on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    t = threading.Thread(target = conn_handler, args = (conn, addr))
    t.start()
