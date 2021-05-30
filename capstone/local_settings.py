DATABASES = {}

import dj_database_url
DATABASES['default'] = dj_database_url.config(engine='django.db.backends.postgresql', conn_max_age=600)

print(DATABASES)