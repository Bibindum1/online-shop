document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.product-row.draggable');
    if (items.length === 0) return;

    let draggedItem = null;

    items.forEach(item => {
        item.draggable = true;

        item.addEventListener('dragstart', function(e) {
            draggedItem = this;
            this.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        });

        item.addEventListener('dragend', function(e) {
            this.classList.remove('dragging');
            draggedItem = null;
        });

        item.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });

        item.addEventListener('dragenter', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });

        item.addEventListener('dragleave', function(e) {
            this.classList.remove('drag-over');
        });

        item.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');

            if (this !== draggedItem) {
                const allItems = document.querySelectorAll('.product-row.draggable');
                const fromIndex = Array.from(allItems).indexOf(draggedItem);
                const toIndex = Array.from(allItems).indexOf(this);

                if (fromIndex < toIndex) {
                    this.parentNode.insertBefore(draggedItem, this.nextSibling);
                } else {
                    this.parentNode.insertBefore(draggedItem, this);
                }

                saveOrder();
            }
        });
    });

    function saveOrder() {
        const items = document.querySelectorAll('.product-row.draggable');
        const order = Array.from(items).map(item => parseInt(item.dataset.productId));

        fetch("{% url 'catalog:reorder_products' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({order: order})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ Порядок товаров сохранен');
            } else {
                console.error('❌ Ошибка:', data.error);
                location.reload(); // Откат при ошибке
            }
        })
        .catch(error => {
            console.error('Ошибка AJAX:', error);
            location.reload();
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.category-row.draggable');
    if (items.length === 0) return;

    let draggedItem = null;

    items.forEach(item => {
        item.draggable = true;

        item.addEventListener('dragstart', function(e) {
            draggedItem = this;
            this.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        });

        item.addEventListener('dragend', function(e) {
            this.classList.remove('dragging');
            draggedItem = null;
        });

        item.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });

        item.addEventListener('dragenter', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });

        item.addEventListener('dragleave', function(e) {
            this.classList.remove('drag-over');
        });

        item.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');

            if (this !== draggedItem) {
                const allItems = document.querySelectorAll('.category-row.draggable');
                const fromIndex = Array.from(allItems).indexOf(draggedItem);
                const toIndex = Array.from(allItems).indexOf(this);

                if (fromIndex < toIndex) {
                    this.parentNode.insertBefore(draggedItem, this.nextSibling);
                } else {
                    this.parentNode.insertBefore(draggedItem, this);
                }

                saveOrder();
            }
        });
    });

    function saveOrder() {
        const items = document.querySelectorAll('.category-row.draggable');
        const order = Array.from(items).map(item => parseInt(item.dataset.categoryId));

        fetch("{% url 'catalog:reorder_categories' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({order: order})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('✅ Порядок категорий сохранен');
            } else {
                console.error('❌ Ошибка:', data.error);
                location.reload();
            }
        })
        .catch(error => {
            console.error('Ошибка AJAX:', error);
            location.reload();
        });
    }
});
