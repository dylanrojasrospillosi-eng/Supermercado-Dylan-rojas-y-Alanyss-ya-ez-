from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True, verbose_name="Código de barras (SKU)")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    precio = models.PositiveIntegerField(verbose_name="Precio unitario (CLP)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible")
    requiere_refrigeracion = models.BooleanField(default=False, verbose_name="Requiere refrigeración")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} (${self.precio:,})"


class Pedido(models.Model):
    class Modalidad(models.TextChoices):
        PICKUP = "PICKUP", "Retiro en tienda"
        EXPRESS = "EXPRESS", "Despacho Express"

    cliente_nombre = models.CharField(max_length=120, verbose_name="Nombre del cliente")
    cliente_email = models.EmailField(verbose_name="Correo electrónico")
    modalidad = models.CharField(max_length=10, choices=Modalidad.choices)
    fecha_entrega = models.DateField(verbose_name="Fecha comprometida de entrega")
    direccion = models.CharField(max_length=250, blank=True, verbose_name="Dirección")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name="pedidos")
    cantidad = models.PositiveIntegerField(default=1)
    total_estimado = models.PositiveIntegerField(verbose_name="Total estimado (CLP)")
    observaciones = models.TextField(blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente_nombre}"
