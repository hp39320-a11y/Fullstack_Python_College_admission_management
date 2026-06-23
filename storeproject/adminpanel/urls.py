from django.urls import path
from . import views

urlpatterns = [

    # LOGIN
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    # DASHBOARD
    path('', views.dashboard, name='admin_dashboard'),

    # CATEGORY
    path('categories/', views.categories, name='admin_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:id>/', views.delete_category, name='delete_category'),

    # SUBCATEGORY
    path('subcategories/', views.subcategories, name='admin_subcategories'),
    path('add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('edit-subcategory/<int:id>/', views.edit_subcategory, name='edit_subcategory'),
    path('delete-subcategory/<int:id>/', views.delete_subcategory, name='delete_subcategory'),

    # PRODUCTS
    path('products/', views.products, name='admin_products'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),

    # ORDERS
    # ORDERS
    path('orders/', views.orders, name='admin_orders'),
    path('orders/<int:id>/', views.view_order, name='view_order'),  # FIXED
    path('update-order/<int:id>/', views.update_order, name='update_order'),
    path('contacts/', views.contacts, name='admin_contacts'),
    path('coupons/', views.coupons, name='admin_coupons'),
    path('add-coupon/', views.add_coupon, name='add_coupon'),
    path('delete-coupon/<int:id>/', views.delete_coupon, name='delete_coupon'),

]