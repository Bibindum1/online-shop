from django.urls import path, include
from . import views
from .views import ProductDetailAdminView

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('', views.product_list, name='index'),

    path('public/', views.public_page, name='public_page'),
    path('client/', views.client_page, name='client_page'),
    path('manager/', views.manager_page, name='manager_page'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('products/<int:pk>/admin-detail/',
         ProductDetailAdminView.as_view(),
         name='product_detail_admin'),

    path('products/reorder/', views.reorder_products, name='reorder_products'),
    path('categories/reorder/', views.reorder_categories, name='reorder_categories'),
]
