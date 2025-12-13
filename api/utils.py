# retail/utils.py
from django.db.models import Sum, F
from .models import Product

def calculate_warehouse_quantity(product_id, retail_outlet_id):
    """Расчет количества товара на складе для торговой точки"""
    total_supplied = Product.objects.filter(
        product_id=product_id,
        purchaseorderitem__purchase_order__retail_outlet_id=retail_outlet_id,
        purchaseorderitem__purchase_order__status='delivered'
    ).aggregate(total=Sum('purchaseorderitem__quantity'))['total'] or 0
    
    total_ordered = Product.objects.filter(
        product_id=product_id,
        salesorderitem__order__retail_outlet_id=retail_outlet_id,
        salesorderitem__order__status='completed'
    ).aggregate(total=Sum('salesorderitem__quantity'))['total'] or 0
    
    return total_supplied - total_ordered

def get_order_total_with_discount(total, discount_percent):
    """Расчет суммы заказа со скидкой"""
    if discount_percent:
        return total * (1 - discount_percent / 100)
    return total

def get_discount_amount(total, discount_percent):
    """Расчет суммы скидки"""
    if discount_percent:
        return total * discount_percent / 100
    return 0