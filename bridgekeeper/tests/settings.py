DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'bridgekeeper',
]
SECRET_KEY = 'correct horse battery staple'
ROOT_URLCONF = 'bridgekeeper.urls'
