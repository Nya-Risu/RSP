import subprocess
import time

# Запуск сервера
server_process = subprocess.Popen(['python', 'server.py'])
print("Сервер запущен...")

# Ожидание готовности сервера
time.sleep(2)

# Запуск клиента
client_process = subprocess.Popen(['python', 'client.py'])
print("Клиент запущен...")

# Ожидание завершения процессов
server_process.wait()
client_process.wait()