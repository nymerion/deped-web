from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.latest, {"template": "listing.html"}, name='vacancies'),
    url('^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})/$', views.listing, {"template": "listing.html"}, name='vacancy_listing'),
]
