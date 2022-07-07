from . import views
from django.urls import path

urlpatterns = [
    path('', views.seller_index,name='seller-index'),
    path('seller-login/', views.seller_login,name='seller-login'),
    path('seller-logout/', views.seller_logout,name='seller-logout'),
    path('add-product/', views.add_product,name='add-product'),
    path('edit-product/<int:pid>', views.edit_product,name='edit-product'),
    path('delete-product/<int:pid>', views.delete_product,name='delete-product'),
    path('manage-products/', views.manage_products,name='manage-products'),
]