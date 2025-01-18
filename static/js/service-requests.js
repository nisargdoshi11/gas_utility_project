// static/js/service-requests.js
// Service request form handling
class ServiceRequestForm {
    constructor(formId) {
        this.form = document.getElementById(formId);
        if (this.form) {
            this.initializeForm();
        }
    }

    initializeForm() {
        this.form.addEventListener('submit', this.handleSubmit.bind(this));
        
        // Dynamic priority setting based on request type
        const requestTypeSelect = this.form.querySelector('[name="request_type"]');
        if (requestTypeSelect) {
            requestTypeSelect.addEventListener('change', (e) => {
                const prioritySelect = this.form.querySelector('[name="priority"]');
                if (e.target.value === 'gas_leak') {
                    prioritySelect.value = 'urgent';
                }
            });
        }
    }

    handleSubmit(e) {
        e.preventDefault();
        
        // Form validation
        if (!this.validateForm()) {
            return;
        }

        // Submit form
        this.submitForm();
    }

    validateForm() {
        let isValid = true;
        const requiredFields = this.form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                this.showError(field, 'This field is required');
            } else {
                this.clearError(field);
            }
        });

        return isValid;
    }

    showError(field, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        field.classList.add('is-invalid');
        field.parentNode.appendChild(errorDiv);
    }

    clearError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    submitForm() {
        const formData = new FormData(this.form);
        fetch(this.form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                this.showFormErrors(data.errors);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

// Initialize forms when document is ready
document.addEventListener('DOMContentLoaded', function() {
    new ServiceRequestForm('serviceRequestForm');
    if (document.getElementById('dashboardCharts')) {
        initializeDashboardCharts();
    }
});