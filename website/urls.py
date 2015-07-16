from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'website.views.index'),
    url(r'^uploader/$', 'website.views.uploader'),
    url(r'^register/$', 'website.views.register'),
    url(r'^account/$', 'website.views.account'),
    url(r'^checkout/$', 'website.views.checkout'),
    url(r'^download/$', 'website.views.download_codes'),
    url(r'^order_products/$', 'website.views.get_order_products'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'website/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'upload/', 'website.views.upload', name = 'jfu_upload' ),
# You may optionally define a delete url as well
	url( r'^delete/(?P<pk>\d+)$', 'website.views.upload_delete', name = 'jfu_delete' ),
	url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
