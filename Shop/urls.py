from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('order/create/<int:product_id>/', views.create_order, name='create_order'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),

    path('profile/', views.customer_profile, name='customer_profile'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]