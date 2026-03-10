document.addEventListener('DOMContentLoaded', function() {
    // Небольшая задержка для полной загрузки DOM и Bootstrap
    setTimeout(() => {
        initDragAndDrop();
    }, 100);
});

function initDragAndDrop() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfToken) {
        console.warn('❌ CSRF токен не найден');
        return;
    }

    const tableBody = document.querySelector('.table-responsive tbody');
    if (!tableBody) {
        console.warn('❌ Не найдена таблица');
        return;
    }

    // Проверяем наличие draggable элементов
    const draggableElements = tableBody.querySelectorAll('.draggable');
    if (draggableElements.length === 0) {
        console.log('ℹ️ Draggable элементы не найдены');
        return;
    }

    // ОДИН Sortable для всей таблицы
    new Sortable(tableBody, {
        animation: 250,
        handle: '.bi-grip-vertical',  // ТОЛЬКО за grip иконку
        draggable: '.draggable',      // все строки с классом draggable

        // Визуальные классы
        ghostClass: 'dragging',
        chosenClass: 'sortable-chosen',
        dragClass: 'sortable-drag',

        // Предотвращаем начало перетаскивания не за handle
        preventOnTarget: true,

        // Фильтруем нежелательные элементы
        filter: 'thead tr, .table-dark, .no-drag',

        onEnd: function(evt) {
            handleReorder(evt.item.dataset.type, csrfToken.value);
        },

        onStart: function(evt) {
            console.log('🚀 Начато перетаскивание:', evt.item.dataset.type);
        },

        onAdd: function(evt) {
            console.log('✅ Элемент добавлен:', evt.item.dataset.type);
        }
    });

    console.log('✅ Drag & Drop успешно инициализирован');
}

function handleReorder(type, csrfToken) {
    let selector, endpoint, label;

    if (type === 'category') {
        selector = '.category-row[data-id]';
        endpoint = '/catalog/categories/reorder/';
        label = 'Категории';
    } else if (type === 'product') {
        selector = '.product-row[data-id]';
        endpoint = '/catalog/products/reorder/';
        label = 'Товары';
    } else {
        console.warn('❌ Неизвестный тип:', type);
        return;
    }

    const items = Array.from(document.querySelectorAll(selector))
        .map(row => parseInt(row.dataset.id))
        .filter(id => !isNaN(id) && id > 0);

    if (items.length === 0) {
        console.warn('❌ Элементы не найдены');
        return;
    }

    sendReorderRequest(endpoint, items, label, csrfToken);
}

function sendReorderRequest(url, order, type, csrfToken) {
    console.log(`📤 Отправка ${type}...`, order);

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ order: order })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            console.log(`✅ ${type} (${order.length} шт.) успешно переупорядочены`);
            showToast(`Порядок ${type.toLowerCase()} обновлен`, 'success');
        } else {
            throw new Error(data.error || 'Серверная ошибка');
        }
    })
    .catch(error => {
        console.error(`❌ Ошибка ${type}:`, error);
        showToast(`Ошибка сохранения ${type.toLowerCase()}`, 'danger');
        //setTimeout(() => location.reload(), 1500);
    });
}

function showToast(message, type = 'info') {
    // Bootstrap Toast уведомления
    const toastId = `toast-${Date.now()}`;
    const bgClass = type === 'success' ? 'bg-success' :
                   type === 'danger' ? 'bg-danger' : 'bg-info';

    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }

    toastContainer.insertAdjacentHTML('beforeend', toastHtml);

    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}
