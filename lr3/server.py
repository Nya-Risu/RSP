import socket
import threading
import time
import struct

# Настройки
TCP_IP = '127.0.0.1'
TCP_PORT = 1501
UDP_GROUP = '233.0.0.1'
UDP_PORT = 1502
BUFFER_SIZE = 1024
MESSAGE_INTERVAL = 10  # Интервал в секундах для отправки сообщений

# Список для хранения сообщений
messages = []

# Функция для обработки соединений с клиентами (TCP)
def handle_client(conn, addr):
    print(f'Клиент подключен: {addr}')
    while True:
        try:
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break
            print(f'Получено сообщение от {addr}: {data}')
            messages.append(data)
        except ConnectionResetError:
            break
    conn.close()

# Функция для рассылки сообщений через UDP
def broadcast_messages():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    
    while True:
        time.sleep(MESSAGE_INTERVAL)
        if messages:
            message_batch = '\n'.join(messages)
            sock.sendto(message_batch.encode('utf-8'), (UDP_GROUP, UDP_PORT))
            print(f'Рассылка сообщений: {message_batch}')
            messages.clear()

# Запуск сервера
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(5)
    print(f'Сервер запущен на {TCP_IP}:{TCP_PORT}')

    # Поток для рассылки сообщений через UDP
    broadcast_thread = threading.Thread(target=broadcast_messages)
    broadcast_thread.daemon = True
    broadcast_thread.start()

    # Основной цикл для обработки новых подключений
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()