from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from decimal import Decimal

class Supplier(models.Model):
    """Поставщики"""
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес")
    inn = models.CharField(max_length=12, verbose_name="ИНН")
    
    def __str__(self):
        return self.name

class Category(models.Model):
    """Категория товаров"""
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название категории")
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Продукт"""
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    description = models.TextField(verbose_name="Описание", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    unit = models.CharField(max_length=20, verbose_name="Единица измерения")
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    def get_warehouse_quantity(self, retail_outlet_id):
        """Расчет количества на складе для конкретной торговой точки"""
        from django.db.models import Sum  # Или импорт здесь
        
        # Исправлено: Sum('quantity'), а не sum('quantity')
        total_supplied = PurchaseOrderItem.objects.filter(
            product=self,
            order__retail_outlet_id=retail_outlet_id,
            order__status='delivered'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        total_sold = SalesOrderItem.objects.filter(
            product=self,
            order__retail_outlet_id=retail_outlet_id,
            order__status='completed'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        return total_supplied - total_sold

class RetailOutlet(models.Model):
    """Торговая точка"""
    retail_outlet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название")
    address = models.TextField(verbose_name="Адрес")
    
    def __str__(self):
        return self.name

class Customer(models.Model):
    """Покупатель"""
    CUSTOMER_TYPES = [
        ('individual', 'Физическое лицо'),
        ('legal', 'Юридическое лицо'),
    ]
    
    customer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, verbose_name="ФИО/Название")
    type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, verbose_name="Тип")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email", blank=True)
    address = models.TextField(verbose_name="Адрес", blank=True)
    
    def __str__(self):
        return self.full_name

class Employee(models.Model):
    """Сотрудник"""
    employee_id = models.AutoField(primary_key=True)
    retail_outlet = models.ForeignKey(RetailOutlet, on_delete=models.CASCADE, verbose_name="Торговая точка")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=100, verbose_name="Должность")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    
    def __str__(self):
        return self.full_name

class PurchaseOrder(models.Model):
    """Заказ на поставку"""
    ORDER_STATUSES = [
        ('ordered', 'Заказан'),
        ('in_transit', 'В пути'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    order_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Поставщик")
    retail_outlet = models.ForeignKey(RetailOutlet, on_delete=models.CASCADE, verbose_name="Торговая точка")
    order_date = models.DateField(verbose_name="Дата заказа")
    expected_delivery_date = models.DateField(verbose_name="Ожидаемая дата поставки")
    actual_delivery_date = models.DateField(verbose_name="Фактическая дата поставки", null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUSES, verbose_name="Статус поставки")
    
    def __str__(self):
        return f"Поставка #{self.order_id}"
    
    def get_total_price(self):
        """Общая стоимость поставки"""
        total = self.purchaseorderitem_set.aggregate(
            total=models.sum(models.F('purchase_price') * models.F('quantity'))
        )['total'] or Decimal('0')
        return total

class PurchaseOrderItem(models.Model):
    """Товары в заказе на поставку"""
    purchase_order_items_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Количество")
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total(self):
        return self.purchase_price * self.quantity

class SalesOrder(models.Model):
    """Заказ на продажу"""
    ORDER_STATUSES = [
        ('pending', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('in_delivery', 'В доставке'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Покупатель")
    retail_outlet = models.ForeignKey(RetailOutlet, on_delete=models.CASCADE, verbose_name="Торговая точка")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сотрудник")
    order_date = models.DateField(verbose_name="Дата заказа")
    delivery_date = models.DateField(verbose_name="Дата доставки", null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUSES, verbose_name="Статус заказа")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Персональная скидка (%)")
    
    def __str__(self):
        return f"Заказ #{self.order_id}"
    
    def get_total_price(self):
        """Общая стоимость заказа со скидкой"""
        total = sum(item.get_total() for item in self.salesorderitem_set.all())
        if self.discount:
            total = total * (1 - self.discount / 100)
        return total
    
    def get_total_without_discount(self):
        """Общая стоимость заказа без скидки"""
        return sum(item.get_total() for item in self.salesorderitem_set.all())

class SalesOrderItem(models.Model):
    """Товары в заказе на продажу"""
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за единицу")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Количество")
    
    class Meta:
        unique_together = ['order', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def get_total(self):
        return self.selling_price * self.quantity