from .settings import *
import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=500)

if 'DATABASE_URL' in os.environ and not DEBUG:
    DATABASES['default'] = db_from_env
