from django import forms
from .models import Order, Product, PickUpPoint

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Укажите поля, которые хотите отображать в форме.
        # Если product_article - это артикул, а не объект Product, то придется изменить.
        # Если вы хотите, чтобы `product` и `pick_up_point` были выпадающими списками, то 'product', 'pick_up_point'.
        fields = [
            'order_number', 'product', 'order_date', 'delivery_date',
            'pick_up_point', 'customer_full_name', 'receive_code', 'status'
        ]
        # Если вы хотите более точные виджеты для дат:
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Если вы хотите, чтобы Product и PickUpPoint фильтровались или имели определенный порядок
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Опционально: отсортировать продукты и пункты выдачи в выпадающих списках
        self.fields['product'].queryset = Product.objects.all().order_by('article')
        self.fields['pick_up_point'].queryset = PickUpPoint.objects.all().order_by('id') # Или по 'address'