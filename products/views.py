from django.shortcuts import render , redirect
from .models import Product
from django.http import HttpResponseForbidden
from .forms import ProductForm
from django.shortcuts import get_object_or_404


def product_list(request):
    products = Product.objects.all()

    user = request.user
    is_admin = user.is_authenticated and user.is_superuser or user.groups.filter(name='admin').exists()
    is_manager = user.is_authenticated and user.groups.filter(name='manager').exists()
    is_client = user.is_authenticated and user.groups.filter(name='client').exists()
    is_guest = not user.is_authenticated

    can_filter = is_admin or is_manager

    query = request.GET.get('q')
    sort = request.GET.get('sort')

    if can_filter and query:
        products = products.filter(name__icontains=query)

    if can_filter and sort:
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')

    return render(
        request,
        'products/product_list.html',
        {
            'products': products,
            'is_admin': is_admin,
            'is_manager': is_manager,
            'is_client': is_client,
            'is_guest': is_guest,
            'can_filter': can_filter,
            'query': query,
            'sort': sort,
        }
    )

def product_create(request):
    user = request.user

    is_admin = user.is_authenticated and user.is_superuser or user.groups.filter(name='admin').exists()

    if not (is_admin):
        return HttpResponseForbidden("Доступ запрещён")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm()

    return render(
        request,
        'products/product_form.html',
        {'form': form}
    )

def product_update(request, pk):
    user = request.user

    is_admin = user.is_authenticated and user.is_superuser or user.groups.filter(name='admin').exists()

    if not (is_admin ):
        return HttpResponseForbidden("Доступ запрещён")

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'product': product,
        }
    )

def product_delete(request, pk):
    user = request.user

    is_admin = user.is_authenticated and user.is_superuser or user.groups.filter(name='admin').exists()

    if not (is_admin ):
        return HttpResponseForbidden("Доступ запрещён")

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('/')

    return render(
        request,
        'products/product_confirm_delete.html',
        {'product': product}
    )
