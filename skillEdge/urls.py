from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('base.api.urls')),
    path('educator/', include('educator.urls')),
<<<<<<< HEAD
    path('courses/', include('courses.urls'))
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
=======
    path('courses/', include('courses.urls')),
    path('wallet/', include('wallet.urls')),
]
>>>>>>> ad1f7586af659668bbae98dc68ef98ecc21f2fad
