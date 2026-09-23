import socket

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 9000))
srv.listen(5)

while True:
    conn, addr = srv.accept()
    data = conn.recv(1024)
    print(data)
    conn.sendall(data.upper())
    conn.close()