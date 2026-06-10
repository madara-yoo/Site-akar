import socket

def create_server(host='localhost', port=5000):
    """Create a simple socket server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}")
            
            try:
                data = client_socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    print(f"Received: {message}")
                    response = f"Echo: {message}"
                    client_socket.sendall(response.encode('utf-8'))
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    create_server()
