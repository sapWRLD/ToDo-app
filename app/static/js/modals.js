function openModal(modalId) {
  document.getElementById(modalId).style.display = 'flex';
}

function closeModal(modalId) {
  document.getElementById(modalId).style.display = 'none';
}

// Close buttons
document.querySelectorAll('.close-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.closest('.modal').style.display = 'none';
  });
});

// Close when clicking outside
window.onclick = function(event) {
  document.querySelectorAll('.modal').forEach(modal => {
    if(event.target === modal) modal.style.display = 'none';
  });
}
