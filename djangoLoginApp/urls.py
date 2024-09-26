import djangoLoginApp.views as views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.sign_in, name="sign_in"),
    path("sign-out", views.sign_out, name="sign_out"),
    path("auth-receiver", views.auth_receiver, name="auth_receiver"),
    path("portfolio", views.portfolio, name="portfolio"),
    path("sign", views.sign, name="sign"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
