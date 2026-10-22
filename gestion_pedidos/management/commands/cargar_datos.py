from django.core.management.base import BaseCommand
from gestion_pedidos.models import Categoria, Producto

class Command(BaseCommand):
    help = "Crea 3 categorías y 6 productos de ejemplo."

    def handle(self, *args, **options):
        datos = [
            ("Lácteos", "Productos que requieren cadena de frío."),
            ("Abarrotes", "Alimentos y productos de despensa."),
            ("Congelados", "Productos que deben mantenerse congelados."),
        ]
        categorias = {}
        for nombre, descripcion in datos:
            categoria, _ = Categoria.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": descripcion}
            )
            categorias[nombre] = categoria

        productos = [
            ("Leche entera 1L", "780100100001", "Lácteos", 1200, 30, True),
            ("Queso laminado 250g", "780100100002", "Lácteos", 2800, 15, True),
            ("Arroz 1kg", "780100100003", "Abarrotes", 1600, 40, False),
            ("Fideos 400g", "780100100004", "Abarrotes", 900, 50, False),
            ("Helado 1L", "780100100005", "Congelados", 4500, 12, True),
            ("Verduras congeladas 500g", "780100100006", "Congelados", 2200, 18, True),
        ]
        for nombre, sku, categoria, precio, stock, frio in productos:
            Producto.objects.get_or_create(
                sku=sku,
                defaults={"nombre": nombre, "categoria": categorias[categoria],
                          "precio": precio, "stock": stock,
                          "requiere_refrigeracion": frio}
            )
        self.stdout.write(self.style.SUCCESS("Datos de prueba cargados correctamente."))
