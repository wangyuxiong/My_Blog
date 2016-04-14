from django.conf.urls import patterns, url, include
from . import views
from .feeds import BlogPostFeed

urlpatterns = patterns(
    '',
    url('^$', views.home),
    url(r'^(?P<slug>[-\w\d]+),(?P<post_id>\d+)/$', views.blogpost),
    url('^archive/$', views.archive),
    url('^about/$', views.about),
    url('^projects/$', views.projects),
    url('^talks/$', views.talks),
    url('^contact/', include('contact_form.urls')),
    url('^article/(?P<freshness>.*)/$', views.article),
    url('^rss/$', BlogPostFeed()),
)
