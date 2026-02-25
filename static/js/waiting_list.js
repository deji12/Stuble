// Auto-hide alerts after 5 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    });
}, 5000);

// Loading state
document.querySelector('form').addEventListener('submit', function(e) {
    const btn = document.getElementById('submit-btn');
    btn.classList.add('btn-loading');
    btn.disabled = true;
});