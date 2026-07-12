// ===== DRAG AND DROP FOR KANBAN BOARD =====
document.addEventListener('DOMContentLoaded', () => {
  const taskCards = document.querySelectorAll('.task-card[draggable="true"]');
  const columns = document.querySelectorAll('.column-body');

  taskCards.forEach(card => {
    card.addEventListener('dragstart', () => {
      card.classList.add('dragging');
      setTimeout(() => card.style.opacity = '0.5', 0);
    });
    card.addEventListener('dragend', () => {
      card.classList.remove('dragging');
      card.style.opacity = '1';
      columns.forEach(col => col.classList.remove('drag-over'));
    });
  });

  columns.forEach(column => {
    column.addEventListener('dragover', e => {
      e.preventDefault();
      column.classList.add('drag-over');
    });
    column.addEventListener('dragleave', () => column.classList.remove('drag-over'));
    column.addEventListener('drop', e => {
      e.preventDefault();
      column.classList.remove('drag-over');
      const dragging = document.querySelector('.dragging');
      if (!dragging) return;
      const taskId = dragging.dataset.taskId;
      const newStatus = column.dataset.status;
      if (!taskId || !newStatus) return;
      // Submit via hidden form
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = `/tasks/${taskId}/status/`;
      form.innerHTML = `
        <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
        <input type="hidden" name="status" value="${newStatus}">
      `;
      document.body.appendChild(form);
      form.submit();
    });
  });
});

function getCookie(name) {
  let val = null;
  document.cookie.split(';').forEach(c => {
    const [k, v] = c.trim().split('=');
    if (k === name) val = decodeURIComponent(v);
  });
  return val;
}
