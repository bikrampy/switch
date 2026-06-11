import random
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Contact, Cart, CartItem, Order, OrderItem, UserProfile
from django.contrib.auth.models import User

def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    return render(request, 'shop/index.html', {
        'categories': categories,
        'products': products,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    return render(request, 'shop/product_detail.html', {'product': product})

def products(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    if category_id:
        products_list = Product.objects.filter(category_id=category_id, is_active=True)
    else:
        products_list = Product.objects.filter(is_active=True)
    return render(request, 'shop/products.html', {
        'products': products_list,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone-number')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            message=message
        )
        send_mail(
            subject=f'New Contact Message from {name}',
            message=f'Name: {name}\nEmail: {email} Phone: {phone_number}\nMessage:\n{message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        return redirect('contact')
    return render(request, 'shop/contact.html')

def faqs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone-number')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            message=message
        )
        send_mail(
            subject=f'New FAQ Inquiry from {name}',
            message=f'Name: {name}\nEmail: {email} Phone: {phone_number}\nMessage:\n{message}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        return redirect('faqs')
    return render(request, 'shop/faqs.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_page')
    else:
        form = UserCreationForm()
    return render(request, 'shop/signup.html', {'form': form})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, "shop/cart.html", {"items": items, "total": total})

@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    except ValueError:
        quantity = 1
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.quantity = quantity
    else:
        item.quantity += quantity
    item.save()
    return redirect("home_page")

@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == "POST":
        new_qty = int(request.POST.get("quantity", 1))
        item.quantity = new_qty
        item.save()
    return redirect("cart")

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect("cart")

@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    if not items.exists():
        return redirect('home_page')
    subtotal = sum(item.product.price * item.quantity for item in items)
    total = subtotal
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        address = request.POST.get('address')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order = Order.objects.create(
            user=request.user,
            first_name=fname,
            last_name=lname,
            address=address,
            address2=address2,
            city=city,
            zip_code=zip_code,
            phone=phone,
            email=email,
            total_price=total
        )
        email_lines = []
        for item in items:
            if item.product.stock_quantity < item.quantity:
                return redirect('cart')
            item.product.stock_quantity -= item.quantity
            item.product.save()
            OrderItem.objects.create(
                order=order,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            email_lines.append(
                f"{item.product.name} x {item.quantity} @ ₹{item.product.price}"
            )
        items.delete()
        send_mail(
            subject=f"New Order #{order.id}",
            message=(
                f"Order #{order.id}\n"
                f"Customer: {fname} {lname}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"Address: {address}, {address2}, {city}, {zip_code}\n"
                "Items:\n" + "\n".join(email_lines) + f"\nTotal: ₹{total}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )
        return redirect('home_page')
    return render(request, 'shop/checkout.html', {
        'items': items,
        'subtotal': subtotal,
        'total': total
    })

@login_required
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        
        return redirect('profile')
    return render(request, 'shop/profile.html', {'user': user, 'profile': profile})

def forgot_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect('forgot_password')

        otp = str(random.randint(100000, 999999))
        from .models import PasswordResetOTP
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_mail(
            subject="Password Reset OTP",
            message=f"Your OTP is {otp}. It is valid for 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )
        request.session['reset_email'] = email
        return redirect('verify_otp')
    return render(request, 'shop/forgot_password.html')


def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        from .models import PasswordResetOTP
        email = request.session.get('reset_email')
        user = User.objects.get(email=email)
        otp_entry = PasswordResetOTP.objects.filter(user=user, otp=otp_input, is_used=False).first()
        if otp_entry and otp_entry.is_valid():
            otp_entry.is_used = True
            otp_entry.save()
            request.session['otp_verified'] = True
            return redirect('reset_password')
    return render(request, 'shop/verify_otp.html')


def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            return redirect('reset_password')
        email = request.session.get('reset_email')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        request.session.flush()
        return redirect('login')
    return render(request, 'shop/reset_password.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'shop/order_history.html', {'orders': orders})

def track_order(request, order_id=None):
    order = None
    error_message = None
    
    if order_id is not None:
        if not request.user.is_authenticated:
            return redirect('login')
        order = get_object_or_404(Order, id=order_id, user=request.user)
    elif request.method == 'POST':
        order_id_input = request.POST.get('order_id')
        email_input = request.POST.get('email')
        try:
            order = Order.objects.get(id=order_id_input, email=email_input)
        except (Order.DoesNotExist, ValueError):
            error_message = "No order found matching the provided ID and Email."
            
    return render(request, 'shop/track_order.html', {
        'order': order,
        'error_message': error_message
    })