import os
import re

def save_uploaded_files(request_data: bytes) -> str:

    try:
        header_raw, body = request_data.split(b"\r\n\r\n", 1)
    except:
        raise ValueError("Invalid HTTP request: Headers and Body not seperated")

    print("\n-- Body data right here ---\n")
    print(body[:500])
    print("\n----------------------\n")

    headers_text = header_raw.decode(errors='ignore')
    match = re.search(r'boundary="?([^";\r\n]+)"?', headers_text)
    if not match:
        raise ValueError("Boundary not found in headers")

    boundary = match.group(1)
    boundary_bytes = b'--' + boundary.encode()

    parts = body.split(boundary_bytes)

    for part in parts:
        if b"Content-Disposition" in part and b'filename="' in part:
            try:
                headers, rest = part.split(b"\r\n\r\n", 1)
                if rest.endswith(b"\r\n"):
                    rest = rest[:-2]

                file_content = rest

                filename_match = re.search(rb'filename="([^"]+)"', headers)
                if not filename_match:
                    continue
                filename = filename_match.group(1).decode()

                safe_filename = os.path.basename(filename)

                os.makedirs("uploads", exist_ok=True)
                filepath = os.path.join("uploads",safe_filename)
                f = open(filepath, 'wb')
                f.write(file_content)
                f.close()

                print(f"saved to: {filepath}")
                return filepath
            except Exception as e:
                raise ValueError(f"failed to process file part: {e}")

    raise ValueError("No file found in request")
