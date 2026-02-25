document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            this.querySelector('i').classList.toggle('bi-eye');
            this.querySelector('i').classList.toggle('bi-eye-slash');
        });
    });

    // Password strength indicator
    const newPassword = document.getElementById('new_password');
    const strengthDiv = document.getElementById('password-strength');
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');

    if (newPassword) {
        newPassword.addEventListener('input', function() {
            const password = this.value;
            
            if (password.length > 0) {
                strengthDiv.classList.remove('d-none');
                
                // Calculate strength
                let strength = 0;
                if (password.length >= 6) strength++;
                if (password.match(/[a-z]/)) strength++;
                if (password.match(/[A-Z]/)) strength++;
                if (password.match(/[0-9]/)) strength++;
                if (password.match(/[^a-zA-Z0-9]/)) strength++;
                
                // Update UI
                const percentage = (strength / 5) * 100;
                strengthBar.style.width = percentage + '%';
                
                if (strength <= 2) {
                    strengthText.textContent = 'Weak';
                    strengthBar.style.background = '#dc2626';
                } else if (strength <= 4) {
                    strengthText.textContent = 'Medium';
                    strengthBar.style.background = '#f59e0b';
                } else {
                    strengthText.textContent = 'Strong';
                    strengthBar.style.background = '#10b981';
                }
            } else {
                strengthDiv.classList.add('d-none');
            }
        });
    }

    // Delete account confirmation
    const deleteConfirm = document.getElementById('delete-confirm');
    const deleteBtn = document.getElementById('delete-account-btn');
    
    if (deleteConfirm && deleteBtn) {
        deleteConfirm.addEventListener('input', function() {
            if (this.value === 'DELETE') {
                deleteBtn.disabled = false;
            } else {
                deleteBtn.disabled = true;
            }
        });
    }

    // Form loading state
    document.getElementById('edit-account-form').addEventListener('submit', function(e) {
        const submitBtn = document.getElementById('submit-btn');
        submitBtn.classList.add('btn-loading');
        submitBtn.disabled = true;
    });
});