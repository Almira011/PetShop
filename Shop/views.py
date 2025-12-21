from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Product, Customer, Order, OrderProduct

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import login


class UserLoginView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
from .forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # Create User
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )

        # Create Customer
        customer = form.save(commit=False)
        customer.user = user
        customer.save()

        # Auto login
        login(self.request, user)

        return redirect(self.success_url)

class UserLogoutView(LogoutView):
    next_page = 'login'



def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {
        'product': product
    })

@login_required
def customer_profile(request):
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,
            'email': request.user.email or '',
            'phone_number': '',
            'address': '',
        }
    )

    orders = customer.orders.all()

    return render(request, 'customers/profile.html', {
        'customer': customer,
        'orders': orders
    })


@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = get_object_or_404(Customer, user=request.user)

    # Create order
    order = Order.objects.create(
        customer=customer,
        total_amount=product.price
    )

    # Link product to order
    OrderProduct.objects.create(
        order=order,
        product=product
    )

    return redirect('order_detail', order.id)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer__user=request.user)
    order_products = order.order_products.select_related('product')

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'order_products': order_products
    })

@login_required
def my_orders(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = customer.orders.all()

    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })