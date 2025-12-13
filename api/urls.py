from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Главная страница - список торговых точек
    path('', views.MainWindowView.as_view(), name='main_window'),
    
    # Модальное окно с данными торговой точки (по умолчанию склад)
    path('modal/<int:retail_outlet_id>/', 
         views.ModalWindowView.as_view(), 
         name='modal_window'),
    
    # Отдельные вкладки модального окна (для AJAX загрузки)
    path('modal/<int:retail_outlet_id>/warehouse/', 
         views.ModalWindowView.as_view(), 
         name='modal_warehouse'),
    
    path('modal/<int:retail_outlet_id>/supplies/', 
         views.ModalWindowView.as_view(), 
         name='modal_supplies'),
    
    path('modal/<int:retail_outlet_id>/orders/', 
         views.ModalWindowView.as_view(), 
         name='modal_orders'),
    
    path('modal/<int:retail_outlet_id>/employees/', 
         views.ModalWindowView.as_view(), 
         name='modal_employees'),
]