from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Главное окно
    path('', views.MainWindowView.as_view(), name='main_window'),
    
    # Модальное окно с разными вкладками
    path('modal/<int:retail_outlet_id>/', 
         views.ModalWindowView.as_view(), 
         name='modal_window'),
    
    # Вкладка "Склад"
    path('modal/<int:retail_outlet_id>/warehouse/', 
         views.ModalWarehouseView.as_view(), 
         name='modal_warehouse'),
    
    # Вкладка "Поставки"
    path('modal/<int:retail_outlet_id>/supplies/', 
         views.ModalSuppliesView.as_view(), 
         name='modal_supplies'),
    
    # Вкладка "Заказы"
    path('modal/<int:retail_outlet_id>/orders/', 
         views.ModalOrdersView.as_view(), 
         name='modal_orders'),
    
    # Вкладка "Сотрудники"
    path('modal/<int:retail_outlet_id>/employees/', 
         views.ModalEmployeesView.as_view(), 
         name='modal_employees'),
]