from django.conf.urls import url, include
from django.contrib import admin

from api import urls as api_urls

urlpatterns = [
    url(r'^api/', include(api_urls, namespace='api')),
    url(r'^admin/', admin.site.urls),
]
