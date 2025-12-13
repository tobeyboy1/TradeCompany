from django import template

register = template.Library()

@register.filter
def get_status_class(status):
    """Возвращает CSS класс для статуса"""
    status_classes = {
        'delivered': 'status-delivered',
        'in_transit': 'status-in_transit',
        'ordered': 'status-ordered',
        'cancelled': 'status-cancelled',
        'pending': 'status-ordered',
        'confirmed': 'status-in_transit',
        'in_delivery': 'status-in_transit',
        'completed': 'status-delivered',
    }
    return status_classes.get(status, '')

@register.filter
def get_status_icon(status):
    """Возвращает иконку для статуса"""
    status_icons = {
        'delivered': 'bi-check-circle-fill',
        'in_transit': 'bi-truck',
        'ordered': 'bi-clock',
        'cancelled': 'bi-x-circle-fill',
        'pending': 'bi-clock',
        'confirmed': 'bi-check-circle',
        'in_delivery': 'bi-truck',
        'completed': 'bi-check-circle-fill',
    }
    return status_icons.get(status, 'bi-question-circle')

@register.filter
def multiply(value, arg):
    """Умножает значение на аргумент"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract(value, arg):
    """Вычитает аргумент из значения"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return value

@register.simple_tag
def get_sort_url(request, field, current_sort, current_order):
    """Генерирует URL для сортировки"""
    params = request.GET.copy()
    
    if current_sort == field:
        new_order = 'desc' if current_order == 'asc' else 'asc'
    else:
        new_order = 'asc'
    
    params['sort'] = field
    params['order'] = new_order
    
    return f"?{params.urlencode()}"