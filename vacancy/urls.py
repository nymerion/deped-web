from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.listing, {"template": "listing.html"}, name='home'),
]
