import os
import re

def save_uploaded_files(request_data: bytes) -> str:

    try:
        header_raw, body = request_data.split(b"\r\n\r\n", 1)
    except:
        raise ValueError("Invalid HTTP request: Headers and Body not seperated")

    headers_text = header_raw.decode(errors='ignore')
    match = re.search(r'Content-Type:\s*multipart/form-data;\s*boundary=(.+)', headers_text)
    if not match:
        raise ValueError("Boundary not found in headers")

    boundary = match.group(1)
    boundary_bytes = b'--' + boundary.encode()
