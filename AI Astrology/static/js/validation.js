/**
 * Client-side validation for the AI Astrology app
 */

// Date validation function
function validateDate(dateString) {
    if (!dateString || dateString.trim() === '') {
        return { isValid: false, message: 'Please enter a date of birth' };
    }
    
    // Remove extra spaces and normalize separators
    const cleanDate = dateString.trim().replace(/\s+/g, '');
    
    // Try to parse the date using multiple formats
    const dateFormats = [
        /^\d{4}-\d{1,2}-\d{1,2}$/,  // YYYY-MM-DD or YYYY-M-D
        /^\d{1,2}-\d{1,2}-\d{4}$/,  // DD-MM-YYYY or D-M-YYYY
        /^\d{1,2}\/\d{1,2}\/\d{4}$/, // DD/MM/YYYY or D/M/YYYY
        /^\d{4}\/\d{1,2}\/\d{1,2}$/, // YYYY/MM/DD or YYYY/M/D
        /^\d{1,2}-\d{1,2}-\d{2}$/,   // DD-MM-YY or D-M-YY
        /^\d{1,2}\/\d{1,2}\/\d{2}$/, // DD/MM/YY or D/M/YY
    ];
    
    // Check if the date string matches any of our formats
    const isValidFormat = dateFormats.some(format => format.test(cleanDate));
    
    if (!isValidFormat) {
        return { 
            isValid: false, 
            message: 'Please enter a valid date format (e.g., 15-05-1990, 1990-05-15, 15/05/1990)' 
        };
    }
    
    // Try to create a Date object to validate the actual date
    let dateObj;
    try {
        // Replace separators with standard format for Date constructor
        const normalizedDate = cleanDate.replace(/[-\/]/g, '-');
        dateObj = new Date(normalizedDate);
        
        // Check if the date is valid
        if (isNaN(dateObj.getTime())) {
            return { 
                isValid: false, 
                message: 'Please enter a valid date (e.g., 15-05-1990)' 
            };
        }
        
        // Check if date is not in the future
        const today = new Date();
        if (dateObj > today) {
            return { 
                isValid: false, 
                message: 'Date of birth cannot be in the future' 
            };
        }
        
        // Check if date is not too far in the past (reasonable age range)
        const minDate = new Date();
        minDate.setFullYear(today.getFullYear() - 120); // 120 years ago
        if (dateObj < minDate) {
            return { 
                isValid: false, 
                message: 'Please enter a reasonable date of birth' 
            };
        }
        
        return { isValid: true, message: '' };
        
    } catch (error) {
        return { 
            isValid: false, 
            message: 'Please enter a valid date format' 
        };
    }
}

// Name validation function
function validateName(name) {
    if (!name || name.trim() === '') {
        return { isValid: false, message: 'Please enter your name' };
    }
    
    const cleanName = name.trim();
    
    // Check if name has at least 2 characters
    if (cleanName.length < 2) {
        return { isValid: false, message: 'Name must be at least 2 characters long' };
    }
    
    // Check if name contains only letters, spaces, and common punctuation
    const nameRegex = /^[a-zA-Z\s\-'\.]+$/;
    if (!nameRegex.test(cleanName)) {
        return { isValid: false, message: 'Name can only contain letters, spaces, hyphens, apostrophes, and periods' };
    }
    
    return { isValid: true, message: '' };
}

// Form validation function
function validateForm() {
    const nameInput = document.getElementById('name');
    const dobInput = document.getElementById('dob');
    const submitBtn = document.querySelector('.submit-btn');
    
    // Clear previous error messages
    clearErrors();
    
    // Validate name
    const nameValidation = validateName(nameInput.value);
    if (!nameValidation.isValid) {
        showError(nameInput, nameValidation.message);
        return false;
    }
    
    // Validate date of birth
    const dobValidation = validateDate(dobInput.value);
    if (!dobValidation.isValid) {
        showError(dobInput, dobValidation.message);
        return false;
    }
    
    return true;
}

// Show error message
function showError(inputElement, message) {
    // Create error message element
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        color: #ff6b6b;
        font-size: 0.85rem;
        margin-top: 5px;
        padding: 5px 10px;
        background: rgba(255, 107, 107, 0.1);
        border-radius: 5px;
        border-left: 3px solid #ff6b6b;
    `;
    errorDiv.textContent = message;
    
    // Insert error message after the input
    inputElement.parentNode.appendChild(errorDiv);
    
    // Add error styling to input
    inputElement.style.borderColor = '#ff6b6b';
    inputElement.style.boxShadow = '0 0 0 2px rgba(255, 107, 107, 0.2)';
}

// Clear all error messages
function clearErrors() {
    // Remove all error messages
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(error => error.remove());
    
    // Reset input styling
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.style.borderColor = '';
        input.style.boxShadow = '';
    });
}

// Real-time validation
function setupRealTimeValidation() {
    const nameInput = document.getElementById('name');
    const dobInput = document.getElementById('dob');
    
    // Debounce function to limit validation frequency
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Real-time name validation
    nameInput.addEventListener('input', debounce(function() {
        clearErrors();
        const validation = validateName(this.value);
        if (!validation.isValid && this.value.trim() !== '') {
            showError(this, validation.message);
        }
    }, 500));
    
    // Real-time date validation
    dobInput.addEventListener('input', debounce(function() {
        clearErrors();
        const validation = validateDate(this.value);
        if (!validation.isValid && this.value.trim() !== '') {
            showError(this, validation.message);
        }
    }, 500));
}

// Initialize validation when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    setupRealTimeValidation();
    
    // Add form submission validation
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return false;
            }
        });
    }
});
