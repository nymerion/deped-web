from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vacancy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'vacancy.views.listing', name='vacancy_listing'),
) 
