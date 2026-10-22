from django import forms
from django.utils import timezone
from .models import Pedido, Producto

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            "cliente_nombre", "cliente_email", "modalidad", "fecha_entrega",
            "direccion", "producto", "cantidad", "total_estimado", "observaciones",
        ]
        widgets = {
            "cliente_nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre y apellido"}),
            "cliente_email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@ejemplo.cl"}),
            "modalidad": forms.Select(attrs={"class": "form-select"}),
            "fecha_entrega": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "direccion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dirección para despacho Express"}),
            "producto": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "total_estimado": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Indicaciones del pedido"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["producto"].queryset = Producto.objects.filter(stock__gt=0).select_related("categoria")
        self.fields["fecha_entrega"].help_text = "La fecha no puede ser anterior a hoy."
        self.fields["direccion"].required = False
        self.fields["observaciones"].required = False

    def clean(self):
        cleaned = super().clean()
        fecha = cleaned.get("fecha_entrega")
        modalidad = cleaned.get("modalidad")
        total = cleaned.get("total_estimado")
        observaciones = (cleaned.get("observaciones") or "").lower()
        producto = cleaned.get("producto")
        cantidad = cleaned.get("cantidad")

        if fecha and fecha < timezone.localdate():
            self.add_error("fecha_entrega", "La fecha de entrega no puede ser anterior a hoy.")

        if modalidad == Pedido.Modalidad.EXPRESS:
            if total is not None and total < 15000:
                self.add_error("total_estimado", "El despacho Express requiere un pedido mínimo de $15.000 CLP.")
            if not cleaned.get("direccion"):
                self.add_error("direccion", "Ingresa una dirección para el despacho Express.")

        if modalidad == Pedido.Modalidad.PICKUP and producto and producto.requiere_refrigeracion:
            if "bolsa térmica" not in observaciones and "bolsa termica" not in observaciones:
                self.add_error("observaciones", "Para retirar productos refrigerados, indica que llevarás una bolsa térmica.")

        if producto and cantidad:
            if cantidad < 1:
                self.add_error("cantidad", "La cantidad debe ser al menos 1.")
            elif cantidad > producto.stock:
                self.add_error("cantidad", f"Stock insuficiente. Hay {producto.stock} unidad(es) disponible(s).")
        return cleaned
