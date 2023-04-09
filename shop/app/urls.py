from django.urls import path
from .views import ListProducts, DetailProduct, ListCart, DetailCart

urlpatterns = [
    path('products', ListProducts),
    path('products/<int:pk>', DetailProduct),

    path("cart", ListCart),
    path("cart/<int:pk>", DetailCart),

]