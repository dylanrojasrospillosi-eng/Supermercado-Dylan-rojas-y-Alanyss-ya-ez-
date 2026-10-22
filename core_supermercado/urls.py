from django.contrib import admin
from django.urls import path
from gestion_pedidos import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.catalogo, name="catalogo"),
    path("pedido/nuevo/", views.registrar_pedido, name="registrar_pedido"),
    path("resumen/", views.dashboard, name="dashboard"),
]
