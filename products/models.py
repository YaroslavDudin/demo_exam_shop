from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    article = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(default=0)
    
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )
    

    def __str__(self):
        return f"{self.article} — {self.name}"
    
    def final_price(self):
        if self.discount > 0:
            return self.price - (self.price * self.discount / 100)
        return self.price

    
