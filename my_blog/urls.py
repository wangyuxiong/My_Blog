from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns(
    '',

    # css3two_blog
    url(r'^(?P<page>\d*)/$', 'css3two_blog.views.home'),
    url(r'^$', 'css3two_blog.views.home'),
    url(r'^blog/', include('css3two_blog.urls')),
    url('^sitemap/$', 'css3two_blog.views.sitemap'),

    # admin 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^referral/', 'my_blog.views.referral')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'my_blog.views.handler404'
