import os
from pathlib import Path

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Включи отладку для разработки
DEBUG = True

# Разрешённые хосты (для DEBUG=True можно оставить пустым)
ALLOWED_HOSTS = []

# Подключённые приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app',  # Твоё приложение
]

# Middleware (обязательно в таком порядке)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Перед auth
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # После sessions
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной URL-конфиг
ROOT_URLCONF = 'settings.urls'  # Замени на свой проект, если другое имя
WSGI_APPLICATION = 'app.wsgi.application'
# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Папка с шаблонами, если есть
        'APP_DIRS': True,  # Автоматический поиск шаблонов в приложениях
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Важно для админки
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Подключение к базе данных PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'medicineproj',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Пароли (можно использовать стандартные валидаторы)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Локализация и часовой пояс (по желанию)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статические файлы (CSS, JS, изображения)
STATIC_URL = '/static/'

# Опционально: папка для сбора статических файлов
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Дополнительные директории со статикой (если есть)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Пользовательская модель пользователя, если есть
AUTH_USER_MODEL = 'app.User'  # Если используешь кастомную модель User

# Медиафайлы (если загружаешь pdf и т.п.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/login/'  # Путь, куда перенаправляются незалогиненные пользователи

SECRET_KEY = 'django-insecure-9x*4@#your$secret!key12345$)'

