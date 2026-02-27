// collections.js

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== CREATE MODAL ====================
    
    // Create modal search
    const createDropdownSearch = document.getElementById('dropdownSearch');
    if (createDropdownSearch) {
        createDropdownSearch.addEventListener('keyup', function() {
            const searchText = this.value.toLowerCase();
            const items = document.querySelectorAll('#createCollectionModal .dropdown-item.record-item');
            
            items.forEach(item => {
                const title = item.querySelector('.fw-semibold').textContent.toLowerCase();
                if (title.includes(searchText) || searchText === '') {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Update create modal count
    window.updateCreateCount = function() {
        const checked = document.querySelectorAll('#createCollectionModal .record-checkbox:checked').length;
        const countEl = document.getElementById('selectedCount');
        const dropdownBtnEl = document.getElementById('selectedCountDropdown');
        
        if (countEl) countEl.innerText = checked;
        if (dropdownBtnEl) dropdownBtnEl.innerText = checked;
    };
    
    // Initialize create modal count
    updateCreateCount();
    
    // Add change event to create modal checkboxes
    document.querySelectorAll('#createCollectionModal .record-checkbox').forEach(cb => {
        cb.addEventListener('change', updateCreateCount);
    });
    
    // ==================== EDIT MODAL ====================
    
    // Edit modal search
    const editDropdownSearch = document.getElementById('editDropdownSearch');
    if (editDropdownSearch) {
        editDropdownSearch.addEventListener('keyup', function() {
            const searchText = this.value.toLowerCase();
            const items = document.querySelectorAll('#editCollectionModal .dropdown-item.record-item');
            
            items.forEach(item => {
                const title = item.querySelector('.fw-semibold').textContent.toLowerCase();
                if (title.includes(searchText) || searchText === '') {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Update edit modal count
    window.updateEditCount = function() {
        const checked = document.querySelectorAll('#editCollectionModal .record-checkbox:checked').length;
        const countEl = document.getElementById('editSelectedCount');
        const dropdownBtnEl = document.getElementById('editSelectedCountDropdown');
        
        if (countEl) countEl.innerText = checked;
        if (dropdownBtnEl) dropdownBtnEl.innerText = checked;
    };
    
    // Select all in edit modal
    const editSelectAllBtn = document.getElementById('editSelectAllRecords');
    if (editSelectAllBtn) {
        editSelectAllBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('#editCollectionModal .record-checkbox').forEach(cb => {
                cb.checked = true;
            });
            updateEditCount();
        });
    }
    
    // Deselect all in edit modal
    const editDeselectAllBtn = document.getElementById('editDeselectAllRecords');
    if (editDeselectAllBtn) {
        editDeselectAllBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('#editCollectionModal .record-checkbox').forEach(cb => {
                cb.checked = false;
            });
            updateEditCount();
        });
    }
    
    // Add change event to edit modal checkboxes
    document.querySelectorAll('#editCollectionModal .record-checkbox').forEach(cb => {
        cb.addEventListener('change', updateEditCount);
    });
    
    // Initialize edit modal count when modal opens
    document.getElementById('editCollectionModal')?.addEventListener('shown.bs.modal', function() {
        updateEditCount();
    });
    
});

// ==================== GLOBAL FUNCTIONS ====================

function editCollection(collectionId, collectionTitle, selectedRecordIds = []) {
    document.getElementById('edit_collection_id').value = collectionId;
    document.getElementById('edit_collection_title').value = collectionTitle;
    
    const subtitle = document.getElementById('editCollectionSubtitle');
    if (subtitle) {
        subtitle.innerText = `Editing "${collectionTitle}"`;
    }
    
    // Reset all checkboxes in edit modal only
    document.querySelectorAll('#editCollectionModal .record-checkbox').forEach(cb => {
        cb.checked = false;
    });
    
    // Check the selected records
    selectedRecordIds.forEach(id => {
        const cb = document.getElementById(`edit_record_${id}`);
        if (cb) cb.checked = true;
    });
    
    // Update count
    const count = selectedRecordIds.length;
    const countEl = document.getElementById('editSelectedCount');
    const dropdownBtnEl = document.getElementById('editSelectedCountDropdown');
    
    if (countEl) countEl.innerText = count;
    if (dropdownBtnEl) dropdownBtnEl.innerText = count;
    
    // Show the modal
    new bootstrap.Modal(document.getElementById('editCollectionModal')).show();
}

function deleteCollection(collectionId, collectionTitle) {
    // Set the collection ID in the hidden input
    document.getElementById('delete_collection_id').value = collectionId;
    
    // Update the modal title to show which collection is being deleted
    const titleEl = document.getElementById('deleteCollectionTitle');
    if (titleEl) {
        titleEl.innerText = `Delete "${collectionTitle}"?`;
    }
    
    // Show the modal
    new bootstrap.Modal(document.getElementById('deleteCollectionModal')).show();
}

const colors = [
    'linear-gradient(90deg, #667eea, #764ba2)',
    'linear-gradient(90deg, #10b981, #059669)',
    'linear-gradient(90deg, #f59e0b, #d97706)',
    'linear-gradient(90deg, #ec4899, #db2777)',
    'linear-gradient(90deg, #8b5cf6, #7c3aed)',
    'linear-gradient(90deg, #ef4444, #dc2626)'
];

const iconColors = ['#667eea', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6', '#ef4444'];

document.querySelectorAll('.collection-color-bar').forEach((bar, index) => {
    bar.style.background = colors[index % colors.length];
});

document.querySelectorAll('.collection-icon i').forEach((icon, index) => {
    icon.style.color = iconColors[index % iconColors.length];
});