document.addEventListener('DOMContentLoaded', () => {
    const editTaskModalEl = document.getElementById('modal-edit-project');
    const editTaskModal = new bootstrap.Modal(editTaskModalEl);

    const editTaskForm = document.getElementById('edit-task-form');
    const editTaskId = document.getElementById('edit-task-id');
    const editTaskTitle = document.getElementById('edit-task-title');
    const editTaskContent = document.getElementById('edit-task-content');
    const editTaskPriority = document.getElementById('edit-task-priority');
    const editTaskTags = document.getElementById('edit-task-tags');
    const editTaskDueDate = document.getElementById('due_date');

    // Attach event to all edit buttons
    document.querySelectorAll('.edit-task-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Fill form fields from button data attributes
            editTaskId.value = btn.dataset.id;
            editTaskTitle.value = btn.dataset.title;
            editTaskContent.value = btn.dataset.content;
            editTaskPriority.value = btn.dataset.priority;
            editTaskDueDate.value = btn.dataset.due_date;

            // Multi-select tags
            const tags = btn.dataset.tag ? btn.dataset.tag.split(',') : [];
            Array.from(editTaskTags.options).forEach(option => {
                option.selected = tags.includes(option.value);
            });

            // Reset validation
            editTaskForm.classList.remove('was-validated');

            // Show modal
            editTaskModal.show();
        });
    });

    // Reset form when modal closes
    editTaskModalEl.addEventListener('hidden.bs.modal', () => {
        editTaskForm.reset();
        editTaskForm.classList.remove('was-validated');
    });
});
