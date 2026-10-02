import socket
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8080
PAGES = Path(__file__).resolve().parent/"./"

ROUTES = {
    "/": "index.html",
    "/index.html": "index.html",
    "/about": "about.html",
    "/about.html": "about.html"
}

def http_response(status: str, body: bytes, content_type: str) -> bytes:
    header = (
        f"HTTP/1.1{status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    return header.encode("utf-8") + body

def handle_request(raw: bytes) -> bytes:
    try:
        request_line = raw.split(b"\r\n", 1)[0].decode("utf-8", errors="replace")
        method, path, *_ = request_line.split(" ")
        path = path.split("?", 1)[0]

        if method != "GET":
            return http_response(
                "405 Method Not Allowed",
                b"<h1>405 Method Not Allowed</h1>",
                "text/html; charset=utf-8"
            )

        filename = ROUTES.get(path)

        if filename is None:
            return http_response(
                "404 Not Found",
                b"<h1>404 Not Found</h1>",
                "text/html; charset=utf-8"
            )

        page = PAGES / filename

        if not page.is_file():
            return http_response(
                "404 Not Found",
                b"<h1>404 Not Found</h1>",
                "text/html; charset=utf-8"
            )

        return http_response(
            "200 OK",
            page.read_bytes(),
            "text/html; charset=utf-8"
        )
        
    except ValueError:
        return http_response(
            "400 Bad Request",
            b"<h1>400 Bad Request</h1>",
            "text/html; charset=utf-8"
        )

def serve() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"Server is listening on http://{HOST}:{PORT}")
        print("Pages: / and /about")
        print("Click CTRL + C to stop")

        while True:
            conn, _addr = server.accept()
            with conn:
                raw = b""

                while b"\r\n\r\n" not in raw:
                    chunk = conn.recv(4096)

                    if not chunk:
                        break

                    raw += chunk

                if not raw:
                    continue

                request_line = raw.split(b"\r\n", 1)[0].decode(errors="replace")
                print(f"{HOST}:{PORT} {request_line}")
                conn.sendall(handle_request(raw))


if __name__ == "__main__":
    try:
        serve()
    except KeyboardInterrupt:
        print("\nStopped.")   