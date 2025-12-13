// Функции для фильтрации и сортировки

// Дебаунс функция для оптимизации
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Фильтрация таблицы
function filterTable(tableId, filters) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tbody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        let showRow = true;
        
        // Применяем все фильтры
        for (const [field, value] of Object.entries(filters)) {
            if (value) {
                const cell = row.querySelector(`[data-field="${field}"]`);
                if (cell) {
                    const cellValue = cell.textContent || cell.getAttribute('data-value') || '';
                    if (!cellValue.toLowerCase().includes(value.toLowerCase())) {
                        showRow = false;
                        break;
                    }
                }
            }
        }
        
        // Показываем/скрываем строку
        row.style.display = showRow ? '' : 'none';
        if (showRow) visibleCount++;
    });
    
    // Обновляем счетчик
    updateRowCount(tableId, visibleCount);
}

// Сортировка таблицы
function sortTable(tableId, columnIndex, order = 'asc') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr:not([style*="display: none"])'));
    
    rows.sort((a, b) => {
        const aCell = a.cells[columnIndex];
        const bCell = b.cells[columnIndex];
        
        let aValue = aCell.textContent || aCell.getAttribute('data-sort-value') || '';
        let bValue = bCell.textContent || bCell.getAttribute('data-sort-value') || '';
        
        // Парсинг чисел
        if (!isNaN(aValue) && !isNaN(bValue)) {
            aValue = parseFloat(aValue);
            bValue = parseFloat(bValue);
        }
        
        // Парсинг дат
        const aDate = Date.parse(aValue);
        const bDate = Date.parse(bValue);
        if (!isNaN(aDate) && !isNaN(bDate)) {
            aValue = aDate;
            bValue = bDate;
        }
        
        // Сравнение
        if (aValue < bValue) return order === 'asc' ? -1 : 1;
        if (aValue > bValue) return order === 'asc' ? 1 : -1;
        return 0;
    });
    
    // Обновляем таблицу
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
    
    // Обновляем иконки сортировки
    updateSortIndicators(tableId, columnIndex, order);
}

// Обновление индикаторов сортировки
function updateSortIndicators(tableId, columnIndex, order) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    // Сбрасываем все индикаторы
    table.querySelectorAll('th .sort-indicator').forEach(indicator => {
        indicator.className = 'sort-indicator bi bi-arrow-down-up text-muted';
    });
    
    // Устанавливаем индикатор для текущей колонки
    const header = table.rows[0].cells[columnIndex];
    const indicator = header.querySelector('.sort-indicator');
    if (indicator) {
        indicator.className = `sort-indicator bi ${order === 'asc' ? 'bi-sort-down' : 'bi-sort-up'}`;
    }
}

// Обновление счетчика строк
function updateRowCount(tableId, count) {
    const counter = document.querySelector(`#${tableId}-count`);
    if (counter) {
        counter.textContent = count;
    }
}

// Инициализация фильтров для всех таблиц
function initTableFilters() {
    document.querySelectorAll('[data-filter-table]').forEach(input => {
        const tableId = input.getAttribute('data-filter-table');
        const field = input.getAttribute('data-filter-field');
        
        input.addEventListener('input', debounce(function() {
            const filters = {};
            filters[field] = this.value;
            filterTable(tableId, filters);
        }, 300));
    });
}

// Инициализация сортировки для всех таблиц
function initTableSorting() {
    document.querySelectorAll('th[data-sortable]').forEach(header => {
        header.style.cursor = 'pointer';
        header.title = 'Нажмите для сортировки';
        
        // Добавляем индикатор сортировки
        if (!header.querySelector('.sort-indicator')) {
            const indicator = document.createElement('i');
            indicator.className = 'sort-indicator bi bi-arrow-down-up text-muted ms-1';
            header.appendChild(indicator);
        }
        
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const tableId = table.id;
            const columnIndex = Array.from(this.parentNode.children).indexOf(this);
            
            // Определяем порядок сортировки
            const currentOrder = this.getAttribute('data-sort-order') || 'asc';
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            
            // Сохраняем порядок сортировки
            this.setAttribute('data-sort-order', newOrder);
            
            // Сортируем таблицу
            sortTable(tableId, columnIndex, newOrder);
        });
    });
}

// Экспорт таблицы в CSV
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const rows = table.querySelectorAll('tr');
    const csv = [];
    
    rows.forEach(row => {
        const rowData = [];
        const cells = row.querySelectorAll('th, td');
        
        cells.forEach(cell => {
            // Исключаем кнопки действий
            if (!cell.closest('.actions-column')) {
                let text = cell.textContent.trim();
                // Экранируем кавычки
                text = text.replace(/"/g, '""');
                // Добавляем кавычки если есть запятые или переносы строк
                if (text.includes(',') || text.includes('\n') || text.includes('"')) {
                    text = `"${text}"`;
                }
                rowData.push(text);
            }
        });
        
        csv.push(rowData.join(','));
    });
    
    const csvString = csv.join('\n');
    const blob = new Blob(['\ufeff' + csvString], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (navigator.msSaveBlob) {
        // Для IE
        navigator.msSaveBlob(blob, filename);
    } else {
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initTableFilters();
    initTableSorting();
    
    // Обработчики для кнопок экспорта
    document.querySelectorAll('[data-export-table]').forEach(button => {
        button.addEventListener('click', function() {
            const tableId = this.getAttribute('data-export-table');
            const filename = this.getAttribute('data-filename') || 'export.csv';
            exportTableToCSV(tableId, filename);
        });
    });
});

// Экспорт функций
window.TableUtils = {
    filterTable,
    sortTable,
    exportTableToCSV,
    initTableFilters,
    initTableSorting
};