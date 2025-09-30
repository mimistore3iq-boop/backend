from django.urls import path
from . import views

urlpatterns = [
    # Products
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('featured/', views.featured_products, name='featured_products'),
    path('search/', views.search_products, name='search_products'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
]

