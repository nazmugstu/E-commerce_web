from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Avg
from .models import Product, Cart, CartItem, Category, Order, OrderItem, Advertisement  # Added Advertisement
from .forms import CartItemUpdateForm

def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # প্রোডাক্ট ফিল্টারিং
    products = Product.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category_id:
        products = products.filter(category_id=category_id)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # পেজিনেশন
    paginator = Paginator(products, 12)  # প্রতি পেজে ১২টি প্রোডাক্ট
    page_number = request.GET.get('page')
    products_paginated = paginator.get_page(page_number)

    # ফিচার্ড প্রোডাক্ট এবং ক্যাটাগরি
    featured_products = Product.objects.filter(is_featured=True)[:6]
    categories = Category.objects.all()

    # সক্রিয় বিজ্ঞাপন লোড
    advertisements = Advertisement.objects.filter(is_active=True)[:3]  # সর্বোচ্চ ৩টি বিজ্ঞাপন
    print("Advertisements:", advertisements)  # Debugging output

    return render(request, 'core/home.html', {
        'products': products_paginated,
        'featured_products': featured_products,
        'categories': categories,
        'advertisements': advertisements
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
    reviews = product.reviews.all()[:5]  # সর্বোচ্চ ৫টি রিভিউ
    average_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'core/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'average_rating': average_rating
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                messages.error(request, "Quantity must be greater than zero.")
                return redirect('core:product_detail', product_id=product_id)
            if quantity > product.stock:
                messages.error(request, f"Only {product.stock} items available in stock.")
                return redirect('core:product_detail', product_id=product_id)
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not item_created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"{product.name} added to cart!")
            return redirect('core:cart')
        except ValueError:
            messages.error(request, "Invalid quantity provided.")
            return redirect('core:product_detail', product_id=product_id)
    return redirect('core:product_detail', product_id=product_id)

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = cart.cartitem_set.all() if cart else []
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST' and 'update_quantity' in request.POST:
        form = CartItemUpdateForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['item_id']
            quantity = form.cleaned_data['quantity']
            cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            if quantity <= 0:
                cart_item.delete()
                messages.success(request, "Item removed from cart.")
            elif quantity > cart_item.product.stock:
                messages.error(request, f"Only {cart_item.product.stock} items available in stock.")
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, "Cart updated successfully.")
            return redirect('core:cart')
    
    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.cartitem_set.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('core:cart')
    
    if request.method == 'POST':
        selected_item_ids = request.POST.getlist('selected_items')
        selected_items = CartItem.objects.filter(id__in=selected_item_ids, cart=cart)
        
        if not selected_items:
            messages.error(request, "No items selected for checkout.")
            return redirect('core:cart')
        
        total_amount = sum(item.product.price * int(request.POST.get(f'quantity_{item.id}', item.quantity)) for item in selected_items)
        
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            payment_status='Pending',
            status='Pending'
        )
        
        for item in selected_items:
            quantity = int(request.POST.get(f'quantity_{item.id}', item.quantity))
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=quantity,
                price=item.product.price
            )
        
        return render(request, 'core/checkout.html', {
            'order': order,
            'selected_items': selected_items,
            'total_amount': total_amount
        })
    
    cart_items = cart.cartitem_set.all()
    cart_total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'core/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} removed from cart.")
    return redirect('core:cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        form = CartItemUpdateForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity <= 0:
                cart_item.delete()
                messages.success(request, f"{cart_item.product.name} removed from cart.")
            elif quantity > cart_item.product.stock:
                messages.error(request, f"Only {cart_item.product.stock} items available in stock.")
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, f"{cart_item.product.name} quantity updated.")
        else:
            messages.error(request, "Invalid quantity provided.")
    return redirect('core:cart')