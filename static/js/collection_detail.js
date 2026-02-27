document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('searchRecords');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchText = this.value.toLowerCase();
            const cards = document.querySelectorAll('#recordsContainer .record-card');
            
            cards.forEach(card => {
                const title = card.dataset.title;
                if (title.includes(searchText) || searchText === '') {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // Sort functionality
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const container = document.getElementById('recordsContainer');
            const cards = Array.from(document.querySelectorAll('#recordsContainer .record-card'));
            
            if (this.value === 'alpha') {
                cards.sort((a, b) => {
                    const titleA = a.dataset.title;
                    const titleB = b.dataset.title;
                    return titleA.localeCompare(titleB);
                });
            } else if (this.value === 'recent') {
                cards.sort((a, b) => b.dataset.date - a.dataset.date);
            } else if (this.value === 'oldest') {
                cards.sort((a, b) => a.dataset.date - b.dataset.date);
            }
            
            // Reorder the DOM
            cards.forEach(card => container.appendChild(card));
        });
    }
});

function removeFromCollection(recordId, collectionId) {
    if (confirm('Remove this record from the collection?')) {
        // You'll need to create this endpoint
        fetch(`/collections/${collectionId}/remove/${recordId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json',
            },
        }).then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Failed to remove record');
            }
        });
    }
}