from django.conf.urls import *
from django.views.generic import RedirectView

# Register our save signal handlers
from pgweb.util.bases import register_basic_signal_handlers
register_basic_signal_handlers()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import feeds

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'pgweb.blog.views.all_posts'),
    url(r'^rss/', feeds.LatestPosts()),
    (r'^categories/', include('pgweb.blog.cat_urls')),
    (r'^(?P<page>[0-9].*)/$', 'pgweb.blog.views.all_posts'),
    (r'^(?P<blog>^[a-zA-Z].*)/$', 'pgweb.blog.views.by_slug'),
   )
