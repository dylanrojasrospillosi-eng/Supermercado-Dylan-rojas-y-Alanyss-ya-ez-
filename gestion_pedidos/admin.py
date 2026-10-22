from django.contrib import admin
from .models import Categoria, Producto, Pedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sku", "categoria", "precio", "stock", "requiere_refrigeracion")
    list_filter = ("categoria", "requiere_refrigeracion")
    search_fields = ("nombre", "sku")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente_nombre", "modalidad", "producto", "cantidad", "total_estimado", "fecha_entrega")
    list_filter = ("modalidad", "fecha_entrega")
    search_fields = ("cliente_nombre", "cliente_email")
