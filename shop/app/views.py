from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from user.authentication import BearerAuthentication
from .permissins import IsAdminOrReadOnly
from .models import Product, Cart, Order
from .serializers import ProductsSerializer, CartSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly, ])
@authentication_classes([BearerAuthentication, ])
def ListProducts(request):
    if not request.method == "GET" and not request.user.is_staff:
        return Response({
                           "error": {
                             "code": 403,
                             "message": "Forbidden for you"
                           }
                        }
                        )
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminOrReadOnly, ])
@authentication_classes([BearerAuthentication, ])
def DetailProduct(request, **kwargs):
    try:
        product = Product.objects.get(pk=kwargs.get("pk", None))
    except:
        return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
    if not request.method == "GET" and not request.user.is_staff:
        return Response({
                           "error": {
                             "code": 403,
                             "message": "Forbidden for you"
                           }
                        }
                        )
    if request.method == "GET":
        serializer = ProductsSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == "PUT":
        serializer = ProductsSerializer(data=request.data, instance=product)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        product.delete()
        return Response({
                        "data": {
                            "message": "Product removed"
                        }
                    }, status=status.HTTP_200_OK)


    # CRUD Cart


@api_view(["GET"])
@permission_classes([IsAuthenticated, ])
@authentication_classes([BearerAuthentication, ])
def ListCart(request):
    if request.method == "GET":
        cart = Cart.objects.all()
        serializer = CartSerializer(cart, many=True)
        return Response({"data": serializer.data[0]["products"]}, status=status.HTTP_200_OK)


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated, ])
@authentication_classes([BearerAuthentication, ])
def DetailCart(request, **kwargs):
    try:
        pk = kwargs.get("pk", None)
        product = Product.objects.get(pk=pk)
        if not pk:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        cart, created = Cart.objects.get_or_create(user=request.user)
    except:
        return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        if product not in cart.products.all():
            cart.products.add(pk)
            cart.save()
            return Response({
                            "data": {
                                    "message": "Product add to card"
                            }
                       }, status=status.HTTP_201_CREATED
                )
        return Response({"error": "Product not append"})
    if request.method == "DELETE":
        try:
            cart.products.remove(pk)
        except:
            return Response({"error": "Product not in cart"}, status=status.HTTP_404_NOT_FOUND)
        return Response({
                        "data": {
                            "message": "Product removed"
                        }
                    }, status=status.HTTP_200_OK)