from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('user_signin', views.Login.as_view(), name='user_signin'),
    path('register', views.register_page, name='register'),
    path('otp_page', views.otp_page, name='otp_page'),
    path('logout', views.logout_page, name='logout'),
    path('adminlogin', views.admin_login, name='adminlogin'),
    path('adminlogout', views.admin_logout, name='adminlogout'),
    path('admindashboard', views.admin_dashboard, name='admindashboard'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('admin_users', views.admin_users, name='admin_users'),
    path('userblock', views.userblock, name='userblock'),
    path('admin_orders', views.admin_orders, name='admin_orders'),
    path('admin_products', views.admin_products, name='admin_products'),
    path('admin_category', views.admin_category, name='admin_category'),
    path("send_otp", views.send_otp, name="send_otp"),
    path('add_new_product', views.add_new_product, name='add_new_product'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>', views.delete_product, name='delete_product'),
    path('add_new_category', views.add_new_category, name='add_new_category'),
    path('edit_category/<int:id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('about_product', views.about_product, name='about_product'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
]
