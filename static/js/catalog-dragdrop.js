document.addEventListener('DOMContentLoaded', function() {
    const categoryRows = document.querySelectorAll('.category-row.draggable');
    if (categoryRows.length === 0) return;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const tableContainer = document.querySelector('.table-responsive');

    new Sortable(tableContainer, {
        group: 'categories',
        animation: 200,
        handle: '.bi-grip-vertical, .cursor-move',
        draggable: '.category-row.draggable',
        ghostClass: 'dragging',
        filter: '.product-row',
        onEnd: function(evt) {
            const categoryIds = Array.from(document.querySelectorAll('.category-row[data-id]'))
                .map(row => row.dataset.id);

            fetch('/catalog/categories/reorder/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ order: categoryIds })
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert('Ошибка: ' + data.error);
                    location.reload();
                }
            })
            .catch(() => {
                alert('Ошибка сети');
                location.reload();
            });
        }
    });
});
