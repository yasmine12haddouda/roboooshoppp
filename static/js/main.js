// Robo Shop - simple frontend JS
document.addEventListener('DOMContentLoaded', function() {
  // Auto-hide alerts after 3 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      alert.style.opacity = '0';
      setTimeout(function() { alert.remove(); }, 300);
    }, 3000);
  });
});
