from xml.etree.ElementInclude import include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("base.api.urls")),
    path("educator/", include("educator.urls")),
    path("courses/", include("courses.urls")),
    path("wallet/", include("wallet.urls")),
    path("cart/", include("cart.urls")),
    path("payment/", include("payment.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
