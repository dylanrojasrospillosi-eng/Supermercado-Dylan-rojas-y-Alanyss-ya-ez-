from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Sum
from django.shortcuts import render, redirect
from .forms import PedidoForm
from .models import Categoria, Producto, Pedido

def catalogo(request):
    # Partimos mostrando todos los productos y aplicamos los filtros que eligió el usuario.
    productos = Producto.objects.select_related("categoria").all()
    categoria_id = request.GET.get("categoria")
    stock = request.GET.get("stock")
    refrigerados = request.GET.get("refrigerados")

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    if stock == "disponible":
        productos = productos.filter(stock__gt=0)
    elif stock == "agotado":
        productos = productos.filter(stock=0)
    if refrigerados == "si":
        productos = productos.filter(requiere_refrigeracion=True)
    elif refrigerados == "no":
        productos = productos.filter(requiere_refrigeracion=False)

    return render(request, "gestion_pedidos/catalogo.html", {
        "productos": productos,
        "categorias": Categoria.objects.all(),
        "categoria_seleccionada": categoria_id or "",
        "stock_seleccionado": stock or "",
        "refrigerados_seleccionado": refrigerados or "",
    })


def registrar_pedido(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Revisamos el stock otra vez antes de guardar el pedido.
                producto = Producto.objects.get(pk=form.cleaned_data["producto"].pk)
                cantidad = form.cleaned_data["cantidad"]

                if cantidad > producto.stock:
                    form.add_error("cantidad", f"Stock insuficiente. Disponible: {producto.stock}.")
                else:
                    pedido = form.save(commit=False)
                    pedido.producto = producto
                    pedido.save()

                    # Al registrar el pedido, descontamos las unidades del inventario.
                    producto.stock -= cantidad
                    producto.save(update_fields=["stock"])

                    messages.success(request, f"Pedido #{pedido.pk} registrado correctamente.")
                    return redirect("catalogo")
    else:
        form = PedidoForm()
    return render(request, "gestion_pedidos/registrar_pedido.html", {"form": form})


def dashboard(request):
    pedidos = Pedido.objects.all()
    resumen = pedidos.aggregate(ingresos=Sum("total_estimado"), total=Count("id"))
    return render(request, "gestion_pedidos/dashboard.html", {
        "total_pedidos": resumen["total"] or 0,
        "ingresos": resumen["ingresos"] or 0,
        "express": pedidos.filter(modalidad=Pedido.Modalidad.EXPRESS).count(),
        "pickup": pedidos.filter(modalidad=Pedido.Modalidad.PICKUP).count(),
    })
