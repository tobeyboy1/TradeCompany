import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter
from .models import *

class PurchaseOrderFilter(django_filters.FilterSet):
    """Фильтры для поставок"""
    order_id = CharFilter(field_name='order_id', lookup_expr='exact', label='Номер поставки')
    status = ChoiceFilter(choices=PurchaseOrder.ORDER_STATUSES, label='Статус поставки')
    order_date_from = DateFilter(field_name='order_date', lookup_expr='gte', label='Дата заказа от')
    order_date_to = DateFilter(field_name='order_date', lookup_expr='lte', label='Дата заказа до')
    delivery_date_from = DateFilter(field_name='expected_delivery_date', lookup_expr='gte', label='Дата поставки от')
    delivery_date_to = DateFilter(field_name='expected_delivery_date', lookup_expr='lte', label='Дата поставки до')
    
    class Meta:
        model = PurchaseOrder
        fields = []

class SalesOrderFilter(django_filters.FilterSet):
    """Фильтры для заказов"""
    order_id = CharFilter(field_name='order_id', lookup_expr='exact', label='Номер заказа')
    status = ChoiceFilter(choices=SalesOrder.ORDER_STATUSES, label='Статус заказа')
    order_date_from = DateFilter(field_name='order_date', lookup_expr='gte', label='Дата заказа от')
    order_date_to = DateFilter(field_name='order_date', lookup_expr='lte', label='Дата заказа до')
    
    class Meta:
        model = SalesOrder
        fields = []

class EmployeeFilter(django_filters.FilterSet):
    """Фильтры для сотрудников"""
    position = CharFilter(field_name='position', lookup_expr='icontains', label='Должность')
    
    class Meta:
        model = Employee
        fields = []