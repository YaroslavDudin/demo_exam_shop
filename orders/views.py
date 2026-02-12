# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden # <-- Импортируем
from .models import Order, PickUpPoint, Product
from .forms import OrderForm

# --- Функция проверки прав (лучше оставить её, она универсальная) ---
def check_admin_or_manager(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or \
           user.groups.filter(name='admin').exists() or \
           user.groups.filter(name='manager').exists()
def check_admin(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or \
               user.groups.filter(name='admin').exists()
# ------------------------------------------------------------------

def order_list(request):
    user = request.user
    
    # === ДОБАВЛЕНА ПРОВЕРКА ДОСТУПА ===
    if not check_admin_or_manager(user):
        # Если пользователь не админ/менеджер, показываем ему сообщение о запрете.
        # Или можно перенаправить на страницу логина, или на главную.
        # Я использую HttpResponseForbidden, как вы просили для других операций.
        return HttpResponseForbidden("Доступ к списку заказов запрещён.") 
    # === КОНЕЦ ДОБАВЛЕННОЙ ПРОВЕРКИ ===

    # Если доступ разрешен, продолжаем как раньше
    is_admin = user.is_authenticated and (user.is_superuser or user.groups.filter(name='admin').exists())
    is_manager = user.is_authenticated and user.groups.filter(name='manager').exists()
    
    orders = Order.objects.all().select_related('product', 'pick_up_point').order_by('-order_date', '-id')
    
    context = {
        'orders': orders,
        'is_admin': is_admin,
        'is_manager': is_manager,
    }
    return render(request, 'orders/order_list.html', context)


# ... остальные функции (order_add, order_edit, order_delete) без изменений ...
def order_add(request):
    user = request.user
    if not check_admin(user):
        return HttpResponseForbidden("Доступ запрещён")

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    
    context = {
        'form': form,
        'title': 'Добавить заказ',
    }
    return render(request, 'orders/order_form.html', context)


def order_edit(request, pk):
    user = request.user
    if not check_admin(user):
        return HttpResponseForbidden("Доступ запрещён")

    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    
    context = {
        'form': form,
        'order': order,
        'title': f'Редактировать заказ №{order.order_number}',
    }
    return render(request, 'orders/order_form.html', context)


def order_delete(request, pk):
    user = request.user
    if not check_admin(user):
        return HttpResponseForbidden("Доступ запрещён")

    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    
    context = {
        'order': order,
        'title': f'Удалить заказ №{order.order_number}',
    }
    return render(request, 'orders/order_confirm_delete.html', context)
