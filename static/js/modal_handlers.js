// Обработчики для модальных окон

// Глобальный объект для хранения состояния
window.ModalState = {
    currentTab: 'warehouse',
    filters: {},
    sortOptions: {}
};

// Инициализация модального окна при загрузке
document.addEventListener('DOMContentLoaded', function() {
    // Обработка переключения вкладок через AJAX
    initTabAjaxLoading();
    
    // Инициализация всех обработчиков внутри модального окна
    initAllModalHandlers();
});

// Загрузка вкладок через AJAX
function initTabAjaxLoading() {
    document.querySelectorAll('.nav-tabs .nav-link[data-url]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(event) {
            const targetId = event.target.getAttribute('data-bs-target');
            const url = event.target.getAttribute('data-url');
            
            // Сохраняем текущую вкладку
            ModalState.currentTab = targetId.replace('#', '');
            
            // Загружаем содержимое вкладки
            loadTabContent(targetId, url);
        });
    });
}

// Загрузка содержимого вкладки
function loadTabContent(tabId, url) {
    const tabPane = document.querySelector(tabId);
    if (!tabPane) return;
    
    // Показываем индикатор загрузки
    const loadingHtml = `
        <div class="loading-overlay">
            <div class="spinner-border spinner-custom" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
        </div>
    `;
    tabPane.innerHTML = loadingHtml;
    
    // Загружаем данные
    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Network error');
            return response.text();
        })
        .then(html => {
            // Вставляем загруженный HTML
            tabPane.innerHTML = html;
            
            // Инициализируем компоненты вкладки
            initTabComponents(tabId);
            
            // Восстанавливаем состояние (фильтры, сортировку)
            restoreTabState(tabId);
        })
        .catch(error => {
            console.error('Error loading tab:', error);
            tabPane.innerHTML = `
                <div class="alert alert-danger m-3">
                    <i class="bi bi-exclamation-triangle"></i>
                    Ошибка загрузки данных. Пожалуйста, обновите страницу.
                </div>
            `;
        });
}

// Инициализация компонентов вкладки
function initTabComponents(tabId) {
    switch(tabId) {
        case '#warehouse':
            initWarehouseTab();
            break;
        case '#supplies':
            initSuppliesTab();
            break;
        case '#orders':
            initOrdersTab();
            break;
        case '#employees':
            initEmployeesTab();
            break;
    }
    
    // Общие обработчики для всех вкладок
    initCommonTabHandlers(tabId);
}

// Инициализация вкладки "Склад"
function initWarehouseTab() {
    // Фильтрация по категории
    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            filterWarehouseByCategory(this.value);
            saveTabState('#warehouse', { category: this.value });
        });
        
        // Восстанавливаем фильтр из состояния
        if (ModalState.filters.warehouse?.category) {
            categoryFilter.value = ModalState.filters.warehouse.category;
            filterWarehouseByCategory(ModalState.filters.warehouse.category);
        }
    }
    
    // Сортировка
    document.querySelectorAll('#warehouse .sort-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const sortBy = this.getAttribute('data-sort-by');
            const order = this.getAttribute('data-order');
            
            sortWarehouseTable(sortBy, order);
            saveTabState('#warehouse', { sortBy, order });
            
            // Обновляем активную кнопку
            document.querySelectorAll('#warehouse .sort-btn').forEach(b => {
                b.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
    
    // Восстанавливаем сортировку из состояния
    if (ModalState.sortOptions.warehouse) {
        const { sortBy, order } = ModalState.sortOptions.warehouse;
        const sortBtn = document.querySelector(`#warehouse .sort-btn[data-sort-by="${sortBy}"]`);
        if (sortBtn) {
            sortBtn.setAttribute('data-order', order);
            sortBtn.click();
        }
    }
}

// Фильтрация склада по категории
function filterWarehouseByCategory(categoryId) {
    const items = document.querySelectorAll('#warehouse-items .warehouse-item');
    let visibleCount = 0;
    
    items.forEach(item => {
        const itemCategory = item.getAttribute('data-category-id');
        
        if (!categoryId || itemCategory === categoryId) {
            item.style.display = '';
            visibleCount++;
        } else {
            item.style.display = 'none';
        }
    });
    
    // Обновляем счетчики
    updateWarehouseCounters();
}

// Сортировка таблицы склада
function sortWarehouseTable(sortBy, order) {
    const items = Array.from(document.querySelectorAll('#warehouse-items .warehouse-item:not([style*="display: none"])'));
    
    items.sort((a, b) => {
        let aValue, bValue;
        
        if (sortBy === 'name') {
            aValue = a.querySelector('td:first-child strong').textContent.toLowerCase();
            bValue = b.querySelector('td:first-child strong').textContent.toLowerCase();
        } else if (sortBy === 'quantity') {
            aValue = parseInt(a.getAttribute('data-quantity'));
            bValue = parseInt(b.getAttribute('data-quantity'));
        }
        
        const multiplier = order === 'asc' ? 1 : -1;
        if (aValue < bValue) return -1 * multiplier;
        if (aValue > bValue) return 1 * multiplier;
        return 0;
    });
    
    // Для сортировки по названию: товары без остатка в конце
    if (sortBy === 'name') {
        const inStock = items.filter(item => parseInt(item.getAttribute('data-quantity')) > 0);
        const outOfStock = items.filter(item => parseInt(item.getAttribute('data-quantity')) <= 0);
        items = [...inStock, ...outOfStock];
    }
    
    // Обновляем таблицу
    const tbody = document.getElementById('warehouse-items');
    tbody.innerHTML = '';
    items.forEach(item => tbody.appendChild(item));
    
    // Обновляем иконки сортировки
    updateSortIcons('#warehouse', sortBy, order);
}

// Обновление счетчиков склада
function updateWarehouseCounters() {
    const items = document.querySelectorAll('#warehouse-items .warehouse-item:not([style*="display: none"])');
    const inStockCount = Array.from(items).filter(item => 
        parseInt(item.getAttribute('data-quantity')) > 0
    ).length;
    const outOfStockCount = items.length - inStockCount;
    
    // Обновляем бейджи
    const totalBadge = document.querySelector('#warehouse .badge.bg-primary');
    const inStockBadge = document.querySelector('#warehouse .badge.bg-success');
    const outOfStockBadge = document.querySelector('#warehouse .badge.bg-secondary');
    
    if (totalBadge) totalBadge.textContent = items.length;
    if (inStockBadge) inStockBadge.textContent = inStockCount;
    if (outOfStockBadge) outOfStockBadge.textContent = outOfStockCount;
}

// Обновление иконок сортировки
function updateSortIcons(container, sortBy, order) {
    document.querySelectorAll(`${container} .sort-icon`).forEach(icon => {
        icon.className = 'bi sort-icon';
    });
    
    const activeHeader = document.querySelector(`${container} .sortable[data-sort-by="${sortBy}"]`);
    if (activeHeader) {
        const icon = activeHeader.querySelector('.sort-icon');
        if (icon) {
            const iconClass = order === 'asc' ? 'bi-sort-alpha-down' : 'bi-sort-alpha-up';
            icon.className = `bi sort-icon ${iconClass}`;
        }
    }
}

// Сохранение состояния вкладки
function saveTabState(tabId, state) {
    const tabName = tabId.replace('#', '');
    ModalState.filters[tabName] = ModalState.filters[tabName] || {};
    ModalState.sortOptions[tabName] = ModalState.sortOptions[tabName] || {};
    
    if (state.category !== undefined) {
        ModalState.filters[tabName].category = state.category;
    }
    
    if (state.sortBy !== undefined && state.order !== undefined) {
        ModalState.sortOptions[tabName] = { sortBy: state.sortBy, order: state.order };
    }
}

// Восстановление состояния вкладки
function restoreTabState(tabId) {
    const tabName = tabId.replace('#', '');
    // Реализация восстановления состояния
}

// Общие обработчики для всех вкладок
function initCommonTabHandlers(tabId) {
    // Обработка форм фильтрации
    const forms = document.querySelectorAll(`${tabId} form`);
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // AJAX отправка формы
            submitFilterForm(this, tabId);
        });
    });
    
    // Обработка кликов по строкам таблицы
    document.querySelectorAll(`${tabId} tbody tr`).forEach(row => {
        row.addEventListener('click', function(e) {
            if (!e.target.closest('button') && !e.target.closest('a')) {
                this.classList.toggle('highlight-row');
            }
        });
    });
}

// AJAX отправка формы фильтрации
function submitFilterForm(form, tabId) {
    const formData = new FormData(form);
    const url = new URL(form.action || window.location.href);
    
    // Добавляем параметры формы в URL
    for (const [key, value] of formData.entries()) {
        url.searchParams.set(key, value);
    }
    
    // Загружаем обновленные данные
    loadTabContent(tabId, url.toString());
}

// Инициализация всех обработчиков модального окна
function initAllModalHandlers() {
    // Закрытие модального окна по клику вне его
    document.addEventListener('click', function(event) {
        const modal = document.getElementById('outletModal');
        if (modal && event.target === modal) {
            // Очищаем состояние при закрытии
            ModalState = {
                currentTab: 'warehouse',
                filters: {},
                sortOptions: {}
            };
        }
    });
}