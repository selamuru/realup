from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic.base import RedirectView

from remanage import views as remanage_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'realup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # Root
    url(r'^$', remanage_views.index),

    # Portfolio route
    url(r'^portfolio/$', remanage_views.portfolio),

    url(r'^login/$', remanage_views.login_user),

    url(r'^main/$', remanage_views.main),

    # Redirect unknown paths back to root URL
    #url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index'),
]
