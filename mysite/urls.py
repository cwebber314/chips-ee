from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

#import hello.views
import power.views

# Examples:
# url(r'^$', 'mysite.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
#    url(r'^$', hello.views.index, name='index'),
    url(r'^$', power.views.index, name='index'),
#    url(r'^db', hello.views.db, name='db'),
    path('power/', include('power.urls')),
    path('admin/', admin.site.urls),
]
