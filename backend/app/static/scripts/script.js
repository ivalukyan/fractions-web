function dragstart_handler(event) {
    event.dataTransfer.setData("text/plain", event.target.id);
    event.dropEffect = "move";
}

function dragover_handler(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
}

function drop_handler(event) {
    event.preventDefault();
    const id = event.dataTransfer.getData("text/plain");
    const draggableElement = document.getElementById(id);
    const dropzone = event.target;
    dropzone.appendChild(draggableElement);
    
    // Обновляем значение скрытого поля
    updateDroppedElements();
}

function updateDroppedElements() {
    const target = document.getElementById('target');
    const elements = Array.from(target.children)
                          .map(child => child.id)
                          .join(',');
    document.getElementById('droppedElements').value = elements;
}

// Добавляем возможность возвращения элементов в начальную позицию
document.getElementById('initialContainer').addEventListener('drop', event => {
    drop_handler(event);
    updateDroppedElements();
});
document.getElementById('initialContainer').addEventListener('dragover', dragover_handler);