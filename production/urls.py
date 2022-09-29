from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings

from blog.views import (
    blog_post_create_view,
    )

from searches.views import search_view
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('blog-new/', blog_post_create_view, name='blog-new'),
    path('blog/', include('blog.urls')),
    path('search/', search_view, name='search_view'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:

    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)