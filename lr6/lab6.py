import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request, render_template, send_file
import time
import functools

# === 1. Настройка проекта и логирования ===

# Убедимся, что директория для логов существует
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Настройка логгера
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)  # Общий уровень логирования

# Логирование в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Уровень логов для консоли

# Логирование в файл с ротацией
file_handler = TimedRotatingFileHandler(
    f'{log_dir}/app.log', when='midnight', interval=1, backupCount=30)
# Уровень логов для файла (установим DEBUG для теста)
file_handler.setLevel(logging.DEBUG)

# Формат логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Добавляем обработчики в логгер
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Инициализация Flask-приложения
app = Flask(__name__)

# === 2. Логирование сообщений с различными уровнями ===


@app.route('/log')
def log_example():
    # Логируем сообщения разных уровней
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARN message")
    logger.error("This is an ERROR message")
    return "Log messages sent to console and file!"

# === 3. Логирование HTTP-запросов и ответов (AOP) ===


def log_http_request(func):
    @functools.wraps(func)  # Сохраняем метаданные оригинальной функции
    def wrapper(*args, **kwargs):
        # Логируем HTTP-запрос
        logger.info(f"HTTP Request: {request.method} {request.url}")
        response = func(*args, **kwargs)
        # Логируем HTTP-ответ
        logger.info(f"HTTP Response: {response}")
        return response
    return wrapper


@app.route('/http-log')
@log_http_request
def http_log_example():
    return "HTTP request and response logged!"

# === 4. Логирование исключений и ошибок ===


@app.errorhandler(Exception)
def handle_exception(e):
    # Логируем информацию об ошибке
    logger.error("An error occurred", exc_info=True)
    return {"error": str(e)}, 500

# === 5. Логирование времени выполнения методов ===


def log_execution_time(func):
    @functools.wraps(func)  # Сохраняем метаданные оригинальной функции
    def wrapper(*args, **kwargs):
        # Засекаем время выполнения
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        # Логируем время выполнения
        logger.info(f"{func.__name__} executed in {execution_time:.2f}s")
        return result
    return wrapper


@app.route('/execution-time')
@log_execution_time
def execution_time_example():
    time.sleep(1)  # Симуляция долгой операции
    return "Execution time logged!"

# === 6. Настройка ротации логов ===
# Ротация логов настроена через TimedRotatingFileHandler выше, сохраняются 30 файлов с логами.

# Маршрут для главной страницы


@app.route('/')
def index():
    return render_template('index.html')

# Дополнительный маршрут для отображения логов


@app.route('/logs')
def get_logs():
    log_file = os.path.join(log_dir, 'app.log')  # Путь к файлу логов
    try:
        with open(log_file, 'r') as f:
            logs = f.readlines()
        # Возвращаем логи как HTML
        return ''.join(logs).replace('\n', '<br>')
    except FileNotFoundError:
        return "Log file not found.", 404

# Очистка лог файлов


@app.route('/clear-logs')
def clear_logs():
    log_file = os.path.join(log_dir, 'app.log')  # Путь к файлу логов
    try:
        # Очищаем файл логов
        open(log_file, 'w').close()
        logger.info("Log file has been cleared.")
        return "Log file cleared successfully!"
    except Exception as e:
        logger.error(f"Error clearing log file: {e}", exc_info=True)
        return f"Failed to clear log file: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
