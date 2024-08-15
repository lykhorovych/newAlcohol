from .settings import *


DATABASES = {
    # 'default': {
    #     'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
    #     'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, "/data/db.sqlite3")),
    #     'USER': os.environ.get('SQL_USER'),
    #     'PASSWORD': os.environ.get('SQL_PASSWORD', 'postgres'),
    #     'HOST': os.environ.get('SQL_HOST', 'localhost'),
    #     'PORT': os.environ.get('SQL_PORT'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'data/db.sqlite3',
    }
}

if DEBUG:
    INSTALLED_APPS.extend(['debug_toolbar', "django_browser_reload"])
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")
