# retail/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField
from .models import *
class MainWindowView(ListView):
    """Главное окно со списком торговых точек"""
    model = RetailOutlet
    template_name = 'api/main_window.html'
    context_object_name = 'retail_outlets'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(address__icontains=search_query)
            )
        return queryset

class BaseModalView(View):
    """Базовый класс для модальных окон"""
    template_name = 'api/modal_base.html'
    active_tab = None  # Определяется в дочерних классах
    
    def get(self, request, retail_outlet_id):
        retail_outlet = get_object_or_404(RetailOutlet, pk=retail_outlet_id)
        context = {
            'retail_outlet': retail_outlet,
            'active_tab': self.active_tab,
        }
        
        # Загружаем контекст для активной вкладки
        if self.active_tab == 'warehouse':
            context.update(self._get_warehouse_context(retail_outlet))
        elif self.active_tab == 'supplies':
            context.update(self._get_supplies_context(retail_outlet, request))
        elif self.active_tab == 'orders':
            context.update(self._get_orders_context(retail_outlet, request))
        elif self.active_tab == 'employees':
            context.update(self._get_employees_context(retail_outlet, request))
        
        return render(request, self.template_name, context)
    
    # Общие методы для всех вкладок
    def _get_warehouse_context(self, retail_outlet):
        products = Product.objects.all()
        warehouse_data = []
        
        for product in products:
            quantity = product.get_warehouse_quantity(retail_outlet.retail_outlet_id)
            warehouse_data.append({
                'product': product,
                'quantity': quantity,
                'has_stock': quantity > 0,
            })
        
        warehouse_data.sort(key=lambda x: x['product'].name)
        
        return {
            'warehouse_data': warehouse_data,
            'categories': Category.objects.all(),
        }
    
    def _get_supplies_context(self, retail_outlet, request):
        from .filters import PurchaseOrderFilter
        
        supplies = PurchaseOrder.objects.filter(retail_outlet=retail_outlet)
        supply_filter = PurchaseOrderFilter(request.GET, queryset=supplies)
        supplies = supply_filter.qs
        
        sort_by = request.GET.get('sort', 'order_id')
        order = request.GET.get('order', 'asc')
        
        if sort_by == 'order_date':
            supplies = supplies.order_by(f'{"-" if order == "desc" else ""}order_date')
        elif sort_by == 'expected_delivery_date':
            supplies = supplies.order_by(f'{"-" if order == "desc" else ""}expected_delivery_date')
        elif sort_by == 'status':
            supplies = supplies.order_by(f'{"-" if order == "desc" else ""}status')
        elif sort_by == 'total_price':
            supplies = supplies.annotate(
                total_price=Sum(F('purchaseorderitem__purchase_price') * F('purchaseorderitem__quantity'))
            ).order_by(f'{"-" if order == "desc" else ""}total_price')
        else:
            supplies = supplies.order_by(f'{"-" if order == "desc" else ""}order_id')
        
        return {
            'supplies': supplies,
            'filter': supply_filter,
            'sort_by': sort_by,
            'order': order,
        }
    
    def _get_orders_context(self, retail_outlet, request):
        from .filters import SalesOrderFilter
        
        orders = SalesOrder.objects.filter(retail_outlet=retail_outlet)
        order_filter = SalesOrderFilter(request.GET, queryset=orders)
        orders = order_filter.qs
        
        sort_by = request.GET.get('sort', 'order_id')
        order = request.GET.get('order', 'asc')
        
        if sort_by == 'order_date':
            orders = orders.order_by(f'{"-" if order == "desc" else ""}order_date')
        elif sort_by == 'status':
            orders = orders.order_by(f'{"-" if order == "desc" else ""}status')
        elif sort_by == 'total_price':
            orders = orders.annotate(
                calculated_total=ExpressionWrapper(
                    Sum(F('salesorderitem__selling_price') * F('salesorderitem__quantity')) * 
                    (100 - F('discount')) / 100,
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            ).order_by(f'{"-" if order == "desc" else ""}calculated_total')
        else:
            orders = orders.order_by(f'{"-" if order == "desc" else ""}order_id')
        
        return {
            'orders': orders,
            'filter': order_filter,
            'sort_by': sort_by,
            'order': order,
        }
    
    def _get_employees_context(self, retail_outlet, request):
        from .filters import EmployeeFilter
        
        employees = Employee.objects.filter(retail_outlet=retail_outlet)
        employee_filter = EmployeeFilter(request.GET, queryset=employees)
        employees = employee_filter.qs
        
        sort_by = request.GET.get('sort', 'full_name')
        order = request.GET.get('order', 'asc')
        
        if sort_by == 'position':
            employees = employees.order_by(f'{"-" if order == "desc" else ""}position')
        else:
            employees = employees.order_by(f'{"-" if order == "desc" else ""}full_name')
        
        return {
            'employees': employees,
            'filter': employee_filter,
            'sort_by': sort_by,
            'order': order,
        }

# Создаем конкретные View для каждой вкладки
class ModalWarehouseView(BaseModalView):
    active_tab = 'warehouse'

class ModalSuppliesView(BaseModalView):
    active_tab = 'supplies'

class ModalOrdersView(BaseModalView):
    active_tab = 'orders'

class ModalEmployeesView(BaseModalView):
    active_tab = 'employees'

# View по умолчанию (склад)
class ModalWindowView(ModalWarehouseView):
    """Модальное окно по умолчанию (склад)"""
    pass