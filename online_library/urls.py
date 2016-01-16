"""online_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from library import views, admin
from django.conf.urls.static import static
import settings

urlpatterns = [
    url(r'^admin/', admin.super.urls),
    url(r'^home/', views.home),
    url(r'^book/(?P<id_book>\d+)/$', views.show_book, name='book'),
    url(r'^borrow/(?P<id_book>\d+)/$', views.borrow_book, name='borrow'),
    url(r'^login/$', views.login_user),
    url(r'^search/$', views.search),
    url(r'^filter/$', views.search),
    url(r'^register/', views.register_user),
    url(r'^reserve/(?P<id_book>\d+)/$', views.reserve_book, name='reserve'),
    url(r'^donate/$', views.donate),
    url(r'^suggest/$', views.show_suggest),
    url(r'^profile/$', views.show_profile),
    url(
        r'^logout/$',
        auth_views.logout,
        name='logout',
        kwargs={'next_page': '/home/'}
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


