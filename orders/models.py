from django.db import models
from products.models import Product


from django.db import models

class PickUpPoint(models.Model):
    number = models.PositiveIntegerField(unique=True)  # порядковый номер
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.number} - {self.address}"


class Order(models.Model):

    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('completed', 'Завершён'),
    ]

    order_number = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    order_date = models.DateField()
    delivery_date = models.DateField()

    pick_up_point = models.ForeignKey(PickUpPoint, on_delete=models.PROTECT)

    customer_full_name = models.CharField(max_length=255)
    receive_code = models.CharField(max_length=20)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new'
    )

    def __str__(self):
        return f"Заказ {self.order_number}"
