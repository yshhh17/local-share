import socket
import os
import threading
import mimetypes
from discovery_handler import start_listening
from discovery_handler import send_broadcast
from transfer_handler import save_uploaded_files

def conn_handler(conn, addr):
    f = open("../frontend/index.html", "r")
    html = f.read()
    f.close()

    g = open("../frontend/success.html", "r")
    msg = g.read()
    g.close()

    print(f"connection from {addr}")

    request = conn.recv(10000000)

    if not request:
        conn.close()
        return

    try:
        header_raw, body_raw = request.split(b'\r\n', 1)
    except ValueError:
        return

    header_text = header_raw.decode(errors='ignore')
    first_line = header_text.splitlines('\r\n')[0]
    method, path, _ = first_line.split(' ', 2)

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

        elif path == '/api/discovery':
            devices_list = send_broadcast()
            if devices_list and isinstance(devices_list, (list, tuple)):
                result = ', '.join(str(device) for device in devices_list)
            else:
                result = "no devices found or error finding devices..."
            body = f" here is the list of the ip's you were looking for: {result}"
            response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(body)}\r\n"
                    "\r\n"
                    + body
                    ).encode()
            conn.sendall(response)

        else:
            if path == '/api/files':
                os.makedirs('Downloads', exist_ok=True)
                files = os.listdir('Downloads')
                files = [f for f in files if os.path.isfile(os.path.join('Downloads', f))]
                html = "<html><body><h2>Files: </h2><ul>"
                for file in files:
                    html += f'<li><a href = "{file}">{file}</a></li>'
                html += "</ul></body></html>"

                response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(html)}\r\n"
                        "\r\n"
                        + html
                        ).encode()
                conn.sendall(response)

            else:
                path = path.lstrip("/api")
                paths = os.path.join('Downloads', path)
                mime_type, _ = mimetypes.guess_type(paths)
                mime_type = mime_type or "application/octed-stream"

                f = open(paths, 'r')
                data = f.read()
                f.close()

                response = (
                        "HTTP/1.1 200 OK\r\n"
                        f"Content-Type: {mime_type}\r\n"
                        f"Content-Length: {len(data)}\r\n"
                        "\r\n"
                        + data
                        ).encode()

                conn.sendall(response)
            

    elif method == 'POST':
        if path == '/api/upload':
            print("[SERVER] received a POST request to /api/upload")

            save_uploaded_files(request)

            response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(msg)}\r\n"
                    "\r\n"
                    + msg
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
