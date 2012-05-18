#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cts.views.home', name='home'),
    # url(r'^cts/', include('cts.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^', include('share.urls')),
    url(r'^tweet/', 'cts.syncr.twitter.views.tweet'),
    # Uncomment the next line to enable the admin:
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/cts/favicon.ico'}),
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^aren/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^cts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

