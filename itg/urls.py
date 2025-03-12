from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from itg import settings
from news import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='index'),
    path('about/', views.about, name='about'),
    path('news/', include('news.urls', namespace='news')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
