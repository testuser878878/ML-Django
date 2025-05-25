#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings') # указывает настройки проекта
    try:
        from django.core.management import execute_from_command_line  # импортирует механизм команд
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)  # запускает команду из аргументов командной строки

if __name__ == '__main__':
    main()