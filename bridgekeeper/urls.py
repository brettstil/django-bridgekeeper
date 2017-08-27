from django.conf.urls import url

from .views import invited

urlpatterns = [
    url(r'^invited/(?P<code>[\w-]+)$', invited, name='invited'),
]
