function copyPassage() {
    const passage = document.getElementById('passage').innerText;
    navigator.clipboard.writeText(passage).then(() => {
        // Show temporary success message
        const alert = document.createElement('div');
        alert.className = 'alert alert-success position-fixed top-0 end-0 m-3';
        alert.innerHTML = '<i class="bi bi-check-circle-fill me-2"></i>Passage copied to clipboard!';
        document.body.appendChild(alert);
        setTimeout(() => alert.remove(), 3000);
    });
}

// Show passage card when content is loaded
document.addEventListener('DOMContentLoaded', function() {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.target.innerHTML.trim() !== '') {
                document.getElementById('passage-card').style.display = 'block';
            }
        });
    });
    
    const passage = document.getElementById('passage');
    if (passage) {
        observer.observe(passage, { childList: true, subtree: true });
    }
});