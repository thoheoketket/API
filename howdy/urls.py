from django.conf.urls import url
from howdy import views


urlpatterns = [
    url(r'^all/$', views.detect_api),
    url(r'^oneperson/$', views.one_detect_api),
]