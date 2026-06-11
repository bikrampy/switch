from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('signup/', views.signup, name='signup'),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", views.update_quantity, name="update_quantity"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.checkout_view, name='checkout'),
    path('profile/', views.profile_view, name='profile'),
    path('forgot-password/', views.forgot_password_request, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home_page'), name='logout'),
    path('orders/', views.order_history, name='order_history'),
    path('track/', views.track_order, name='track_order'),
    path('track/<int:order_id>/', views.track_order, name='track_order_detail'),
]
