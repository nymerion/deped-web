from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.listing, name='vacancy_listing'),
]
