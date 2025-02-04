# Проект: Тестирование уязвимостей веб-приложений

Данный проект предназначен для тестирования веб-приложений на наличие уязвимостей, таких как SQL-инъекции, XSS, LFI, RFI и другие. Он использует кастомные правила ModSecurity и специализированные тестовые сценарии.

## Структура проекта

```plaintext
├── html/                      # Каталог для анализа HTML-файлов
├── lfi/                       # Каталог для тестирования уязвимостей LFI
├── logs/                      # Каталог для хранения логов выполнения
├── rules/                     # Правила ModSecurity
│   ├── REQUEST_LFI_RFI.conf       # Правило для LFI и RFI
│   ├── REQUEST_RCE.conf           # Правило для Remote Code Execution
│   ├── REQUEST_RFI_CUSTOM.conf    # Правило для кастомного RFI
│   ├── REQUEST_SQL.conf           # Правило для SQL-инъекций
│   ├── REQUEST_USER_AGENT.conf    # Правило для анализа User-Agent
│   ├── REQUEST_XSS.conf           # Правило для XSS
│   ├── REQUEST_XSS_CUSTOM.conf    # Правило для кастомного XSS
├── sql/                       # Каталог с тестовыми SQL-пейлоадами
│   ├── all-payload-list.txt       # Список SQL-пейлоадов
│   ├── drop_requests_sql.txt      # Успешные запросы для SQL-инъекций
├── xss/                       # Каталог с тестовыми XSS-пейлоадами
│   ├── assets/                   # Вложенные данные для XSS
│   │   ├── all-payload-list.txt      # Список XSS-пейлоадов
│   │   ├── drop_requests_xss.txt     # Успешные запросы для XSS
├── default.conf.template      # Шаблон конфигурации Nginx
├── main.py                    # Основной скрипт для тестирования
├── Dockerfile                 # Docker-образ для запуска ModSecurity
```

## Установка и запуск

### Требования

- Python 3.8+
- Docker и Docker Compose
- Установленные зависимости для Python (`requests`)

### Шаги по установке

1. Клонируйте репозиторий:
   ```bash
   git clone <URL_репозитория>
   cd <директория_проекта>
   ```

2. Постройте Docker-образ:
   ```bash
   docker build -t modsecurity-test .
   ```

3. Запустите контейнер с ModSecurity:
   ```bash
   docker run -d -p 5010:80 modsecurity-test
   ```

4. Установите зависимости Python:
   ```bash
   pip install -r requirements.txt
   ```

5. Запустите основной скрипт:
   ```bash
   python main.py
   ```

## Основные компоненты

### Docker

Docker-файл настраивает ModSecurity с использованием правил из папки `rules`. Это позволяет фильтровать вредоносные запросы на основе преднастроенных конфигураций.

### Скрипт `main.py`

Скрипт предназначен для тестирования различных сценариев уязвимостей:
- **test_user_agent()** — проверка поведения сервера с разными значениями `User-Agent`.
- **test_xss()** — тестирование XSS-уязвимостей.
- **test_sql()** — тестирование SQL-инъекций.
- **test_lfi()** — тестирование LFI (Local File Inclusion).
- **test_base_requests()** — выполнение базовых запросов из файла `requests.txt`.

Каждая функция читает тестовые пейлоады из соответствующих файлов (например, `all-payload-list.txt`) и отправляет их на сервер.

### Правила ModSecurity

Файлы в папке `rules/` содержат кастомные правила для фильтрации вредоносных запросов. Эти правила используются для обнаружения LFI, RFI, XSS, SQL-инъекций и других угроз.

## Логи

Все результаты выполнения скрипта и запросов сохраняются в папке `logs/` для последующего анализа.

## Пример использования

1. Запустите контейнер ModSecurity.
2. Выполните нужную тестовую функцию, раскомментировав вызов в `main.py`.
3. Анализируйте результаты тестов в логах.
