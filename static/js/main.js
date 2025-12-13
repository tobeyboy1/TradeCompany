// Улучшенный main.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('TradeComp system loaded');
    
    // Обработка модального окна
    const outletModal = document.getElementById('outletModal');
    
    if (outletModal) {
        outletModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            
            // Получаем название торговой точки
            const outletCard = button.closest('.retail-outlet-card');
            const outletName = outletCard ? 
                outletCard.getAttribute('data-outlet-name') || 
                outletCard.querySelector('.card-title')?.textContent || 
                'Торговая точка' : 
                'Торговая точка';
            
            // Обновляем название в заголовке (если элемент существует)
            const modalOutletName = document.getElementById('modal-outlet-name');
            if (modalOutletName) {
                modalOutletName.textContent = outletName;
            } else {
                console.warn('Element #modal-outlet-name not found');
                // Создаем элемент если его нет
                const modalTitle = document.querySelector('#outletModal .modal-title');
                if (modalTitle) {
                    const newElement = document.createElement('span');
                    newElement.id = 'modal-outlet-name';
                    newElement.textContent = outletName;
                    modalTitle.appendChild(newElement);
                }
            }
            
            // Получаем URL для загрузки
            const url = button.getAttribute('data-url') || button.getAttribute('href');
            
            if (url) {
                console.log('Loading modal from:', url);
                
                // Показываем индикатор загрузки
                const modalContent = document.getElementById('modal-content');
                if (modalContent) {
                    modalContent.innerHTML = `
                        <div class="text-center py-5">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Загрузка...</span>
                            </div>
                            <p class="mt-3">Загрузка данных...</p>
                        </div>
                    `;
                    
                    // Загружаем данные
                    fetch(url)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`HTTP error! status: ${response.status}`);
                            }
                            return response.text();
                        })
                        .then(html => {
                            modalContent.innerHTML = html;
                        })
                        .catch(error => {
                            console.error('Error loading modal:', error);
                            modalContent.innerHTML = `
                                <div class="alert alert-danger m-3">
                                    <i class="bi bi-exclamation-triangle"></i>
                                    Ошибка загрузки данных: ${error.message}
                                </div>
                            `;
                        });
                }
            }
        });
        
        // Очистка при закрытии
        outletModal.addEventListener('hidden.bs.modal', function() {
            const modalContent = document.getElementById('modal-content');
            if (modalContent) {
                modalContent.innerHTML = `
                    <div class="text-center py-5">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Загрузка...</span>
                        </div>
                        <p class="mt-3">Загрузка данных...</p>
                    </div>
                `;
            }
        });
    }
    
    // Дебаунс для поиска
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.form.submit();
            }, 500);
        });
    }
    
    // Проверка всех необходимых элементов
    console.log('Checking required elements:');
    console.log('#outletModal:', document.getElementById('outletModal'));
    console.log('#modal-outlet-name:', document.getElementById('modal-outlet-name'));
    console.log('#modal-content:', document.getElementById('modal-content'));
});