// main.js - Упрощенная версия для статической загрузки модальных окон
document.addEventListener('DOMContentLoaded', function() {
    console.log('TradeComp system loaded (static version)');
    
    // Обработка модального окна торговой точки
    const outletModal = document.getElementById('outletModal');
    
    if (outletModal) {
        // При открытии модального окна обновляем название в заголовке
        outletModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            
            // Находим карточку торговой точки
            const outletCard = button.closest('.retail-outlet-card');
            if (outletCard) {
                // Получаем название из разных возможных мест
                const outletName = outletCard.getAttribute('data-outlet-name') || 
                                   outletCard.querySelector('.card-title')?.textContent?.trim() || 
                                   'Торговая точка';
                
                // Обновляем заголовок модального окна
                const modalTitle = document.querySelector('#outletModal .modal-title');
                if (modalTitle) {
                    const titleText = modalTitle.querySelector('#modal-outlet-name') || 
                                     modalTitle.querySelector('span:last-child');
                    
                    if (titleText) {
                        titleText.textContent = outletName;
                    } else {
                        // Создаем элемент если его нет
                        const outletNameElement = document.createElement('span');
                        outletNameElement.id = 'modal-outlet-name';
                        outletNameElement.textContent = outletName;
                        
                        // Добавляем иконку перед названием
                        const icon = document.createElement('i');
                        icon.className = 'bi bi-shop me-2';
                        modalTitle.prepend(icon);
                        modalTitle.appendChild(outletNameElement);
                    }
                }
            }
        });
        
        // Очистка при закрытии (опционально)
        outletModal.addEventListener('hidden.bs.modal', function() {
            // Можно сбросить состояние если нужно
            console.log('Modal closed');
        });
    }
    
    // Упрощенный дебаунс для поиска на главной странице
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Простая отправка формы через 500ms
                this.form.submit();
            }, 500);
        });
    }
    
    // Базовая инициализация сортировки (если используется)
    // initSimpleSorting();
});

// // Простая функция инициализации сортировки
// function initSimpleSorting() {
//     document.querySelectorAll('[data-sortable]').forEach(element => {
//         element.style.cursor = 'pointer';
//         element.addEventListener('click', function() {
//             const table = this.closest('table');
//             if (table) {
//                 sortTableByColumn(table, this.cellIndex || 0);
//             }
//         });
//     });
// }

// // Простая клиентская сортировка таблицы
// function sortTableByColumn(table, columnIndex) {
//     const tbody = table.querySelector('tbody');
//     const rows = Array.from(tbody.querySelectorAll('tr'));
    
//     rows.sort((a, b) => {
//         const aText = a.cells[columnIndex]?.textContent.trim() || '';
//         const bText = b.cells[columnIndex]?.textContent.trim() || '';
        
//         // Пытаемся сравнить как числа
//         const aNum = parseFloat(aText);
//         const bNum = parseFloat(bText);
        
//         if (!isNaN(aNum) && !isNaN(bNum)) {
//             return aNum - bNum;
//         }
        
//         // Иначе как строки
//         return aText.localeCompare(bText);
//     });
    
//     // Переставляем строки
//     tbody.innerHTML = '';
//     rows.forEach(row => tbody.appendChild(row));
// }

// Простая функция для подсветки строк при наведении
function initRowHover() {
    document.querySelectorAll('.table-hover tbody tr').forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.classList.add('table-active');
        });
        
        row.addEventListener('mouseleave', function() {
            this.classList.remove('table-active');
        });
    });
}

// Вызов при необходимости
// initRowHover();