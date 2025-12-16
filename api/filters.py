# # api/filters.py
# import django_filters
# from django_filters import DateFilter, CharFilter
# from .models import *

# class PurchaseOrderFilter(django_filters.FilterSet):
#     """Фильтры для поставок (БЕЗ СТАТУСОВ)"""
#     order_id = CharFilter(field_name='order_id', lookup_expr='exact', label='Номер поставки')
#     supplier = django_filters.ModelChoiceFilter(
#         queryset=Supplier.objects.all(),
#         label='Поставщик'
#     )
    
#     # Диапазоны дат
#     order_date_from = DateFilter(field_name='order_date', lookup_expr='gte', label='Дата заказа от')
#     order_date_to = DateFilter(field_name='order_date', lookup_expr='lte', label='Дата заказа до')
    
#     delivery_date_from = DateFilter(field_name='expected_delivery_date', lookup_expr='gte', label='Дата поставки от')
#     delivery_date_to = DateFilter(field_name='expected_delivery_date', lookup_expr='lte', label='Дата поставки до')
    
#     # Поиск по товару
#     product_name = CharFilter(
#         field_name='purchaseorderitem__product__name', 
#         lookup_expr='icontains',
#         label='Название товара'
#     )
    
#     class Meta:
#         model = PurchaseOrder
#         fields = []

# class SalesOrderFilter(django_filters.FilterSet):
#     """Фильтры для заказов (БЕЗ СТАТУСОВ)"""
#     order_id = CharFilter(field_name='order_id', lookup_expr='exact', label='Номер заказа')
#     customer = django_filters.ModelChoiceFilter(
#         queryset=Customer.objects.all(),
#         label='Покупатель'
#     )
    
#     # Диапазоны дат
#     order_date_from = DateFilter(field_name='order_date', lookup_expr='gte', label='Дата заказа от')
#     order_date_to = DateFilter(field_name='order_date', lookup_expr='lte', label='Дата заказа до')
    
#     # Фильтр по скидке
#     min_discount = django_filters.NumberFilter(
#         field_name='discount', 
#         lookup_expr='gte',
#         label='Скидка от (%)'
#     )
#     max_discount = django_filters.NumberFilter(
#         field_name='discount', 
#         lookup_expr='lte',
#         label='Скидка до (%)'
#     )
    
#     # Поиск по товару
#     product_name = CharFilter(
#         field_name='salesorderitem__product__name', 
#         lookup_expr='icontains',
#         label='Название товара'
#     )
    
#     class Meta:
#         model = SalesOrder
#         fields = []

# class EmployeeFilter(django_filters.FilterSet):
#     """Фильтры для сотрудников"""
#     position = CharFilter(field_name='position', lookup_expr='icontains', label='Должность')
#     full_name = CharFilter(field_name='full_name', lookup_expr='icontains', label='ФИО')
    
#     class Meta:
#         model = Employee
#         fields = []