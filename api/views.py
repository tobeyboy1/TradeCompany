# api/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from django.db.models import Q, Sum, F
from .models import *

class MainWindowView(ListView):
    """Главное окно со списком торговых точек"""
    model = RetailOutlet
    template_name = 'api/main_window.html'
    context_object_name = 'retail_outlets'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(address__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем общее количество торговых точек
        context['total_outlets'] = RetailOutlet.objects.count()
        return context

class ModalWindowView(View):
    """Модальное окно с данными торговой точки"""
    template_name = 'api/modal_base.html'
    
    def get(self, request, retail_outlet_id):
        # Получаем торговую точку
        retail_outlet = get_object_or_404(RetailOutlet, pk=retail_outlet_id)
        
        # 1. Данные для вкладки "Склад" - БЕЗ СТАТУСОВ
        products = Product.objects.all()
        warehouse_data = []
        
        for product in products:
            quantity = product.get_warehouse_quantity(retail_outlet_id)
            warehouse_data.append({
                'product': product,
                'quantity': quantity,
                'has_stock': quantity > 0,
            })
        
        # Сортируем по количеству (сначала товары в наличии)
        warehouse_data.sort(key=lambda x: (-x['quantity'], x['product'].name))
        
        # 2. Данные для вкладки "Поставки"
        supplies = PurchaseOrder.objects.filter(
            retail_outlet=retail_outlet
        ).order_by('-order_date')
        
        # 3. Данные для вкладки "Заказы"
        orders = SalesOrder.objects.filter(
            retail_outlet=retail_outlet
        ).order_by('-order_date')
        
        # 4. Данные для вкладки "Сотрудники"
        employees = Employee.objects.filter(
            retail_outlet=retail_outlet
        ).order_by('full_name')
        
        # 5. Статистика для отображения
        stats = {
            'total_products': len(warehouse_data),
            'products_in_stock': len([item for item in warehouse_data if item['quantity'] > 0]),
            'products_out_of_stock': len([item for item in warehouse_data if item['quantity'] <= 0]),
            'total_supplies': supplies.count(),
            'total_orders': orders.count(),
            'total_employees': employees.count(),
        }
        
        # Собираем контекст
        context = {
            'retail_outlet': retail_outlet,
            'active_tab': 'warehouse',
            
            # Данные для вкладок
            'warehouse_data': warehouse_data,
            'categories': Category.objects.all(),
            'supplies': supplies,
            'orders': orders,
            'employees': employees,
            
            # Статистика
            'stats': stats,
            
            # Для сортировки и фильтрации (можно упростить без статусов)
            'sort_by': request.GET.get('sort', 'quantity_desc'),
            'order': request.GET.get('order', 'desc'),
        }
        
        return render(request, self.template_name, context)