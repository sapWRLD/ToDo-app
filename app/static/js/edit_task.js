document.addEventListener('DOMContentLoaded', () => {

    // Open modal
    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.style.display = 'flex';
    }

    // Close modal
    function closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.style.display = 'none';
    }

    // Close buttons
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('.modal').style.display = 'none';
        });
    });

    // Close when clicking outside modal
    window.addEventListener('click', (event) => {
        document.querySelectorAll('.modal').forEach(modal => {
            if (event.target === modal) modal.style.display = 'none';
        });
    });

    // Fill modal fields when clicking Edit
    document.querySelectorAll('.edit-task-btn').forEach(btn => {
        btn.addEventListener('click', () => {

            // Fill hidden ID
            document.getElementById('edit-task-id').value = btn.dataset.id;

            // Fill title and content
            document.getElementById('edit-task-title').value = btn.dataset.title;
            document.getElementById('edit-task-content').value = btn.dataset.content;

            // Fill priority
            document.getElementById('edit-task-priority').value = btn.dataset.priority;

            // Fill due date (optional)
            if (btn.dataset.due_date) {
                document.getElementById('due_date').value = btn.dataset.due_date;
            } else {
                document.getElementById('due_date').value = '';
            }

            // Fill multi-select tags
            const selectedTags = btn.dataset.tag.split(',');
            const tagSelect = document.getElementById('edit-task-tags');
            Array.from(tagSelect.options).forEach(option => {
                option.selected = selectedTags.includes(option.value);
            });

            // Open modal
            openModal('modal-edit-project');
        });
    });

});
