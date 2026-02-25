document.addEventListener('DOMContentLoaded', function() {
    const deleteForm = document.querySelector('#deleteRecordModal form');
    const deleteBtn = document.getElementById('delete-record-btn');
    
    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            // Add loading state to button
            deleteBtn.classList.add('btn-loading');
            deleteBtn.disabled = true;
            
            // Optional: Prevent double submission
            setTimeout(() => {
                deleteBtn.classList.remove('btn-loading');
                deleteBtn.disabled = false;
            }, 5000); // Reset after 5 seconds if something goes wrong
        });
    }
});