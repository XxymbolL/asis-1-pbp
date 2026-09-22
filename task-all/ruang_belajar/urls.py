from django.contrib import admin
from django.urls import path

from ruang_belajar.views import landing_page


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing_page, name="landing_page"),
    # TODO: Hubungkan URL utama project dengan URL configuration milik aplikasi main
]
