/**
 * Admin Panel JavaScript
 * Specific functions for admin operations
 */

(function() {
    'use strict';

    // ============================================
    // Book Management Functions
    // ============================================
    
    window.openAddBookModal = function() {
        document.getElementById('addBookModal').classList.add('active');
    };

    window.closeAddBookModal = function() {
        document.getElementById('addBookModal').classList.remove('active');
    };

    window.editBook = function(bookId) {
        // Fetch book data and populate edit form
        fetch(`/api/books/${bookId}/`)
            .then(response => response.json())
            .then(data => {
                // Populate edit form (implement based on your needs)
                console.log('Edit book:', data);
                showToast('Edit functionality coming soon', 'info');
            })
            .catch(error => {
                showToast('Error fetching book data', 'error');
            });
    };

    window.deleteBook = function(bookId, bookTitle) {
        if (confirm(`Are you sure you want to delete "${bookTitle}"?\n\nThis action cannot be undone.`)) {
            // Show loading
            const btn = event.target.closest('button');
            setLoading(btn, true);
            
            fetch(`/api/books/${bookId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    showToast('Book deleted successfully', 'success');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    throw new Error('Failed to delete book');
                }
            })
            .catch(error => {
                showToast('Error deleting book', 'error');
                setLoading(btn, false);
            });
        }
    };

    // ============================================
    // Category Management Functions
    // ============================================
    
    window.openAddCategoryModal = function() {
        document.getElementById('addCategoryModal').classList.add('active');
    };

    window.closeAddCategoryModal = function() {
        document.getElementById('addCategoryModal').classList.remove('active');
    };

    window.editCategory = function(categoryId) {
        console.log('Edit category:', categoryId);
        showToast('Edit functionality coming soon', 'info');
    };

    window.deleteCategory = function(categoryId, categoryName) {
        if (confirm(`Are you sure you want to delete the category "${categoryName}"?\n\nThis will affect all books in this category.`)) {
            fetch(`/api/categories/${categoryId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.ok) {
                    showToast('Category deleted successfully', 'success');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    throw new Error('Failed to delete category');
                }
            })
            .catch(error => {
                showToast('Error deleting category', 'error');
            });
        }
    };

    // ============================================
    // User Management Functions
    // ============================================
    
    window.viewUser = function(userId) {
        window.location.href = `/admin/users/${userId}/`;
    };

    window.toggleUserStatus = function(userId) {
        if (confirm('Are you sure you want to change this user\'s status?')) {
            fetch(`/api/users/${userId}/toggle-status/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('User status updated', 'success');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    showToast(data.message || 'Failed to update user status', 'error');
                }
            })
            .catch(error => {
                showToast('Error updating user status', 'error');
            });
        }
    };

    // ============================================
    // Book Issue Management
    // ============================================
    
    window.viewIssue = function(issueId) {
        window.location.href = `/admin/issues/${issueId}/`;
    };

    // ============================================
    // Search & Filter Functions
    // ============================================
    
    const booksSearch = document.getElementById('booksSearch');
    if (booksSearch) {
        booksSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const rows = document.querySelectorAll('.modern-table tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    // ============================================
    // Utility Functions
    // ============================================
    
    function getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    // ============================================
    // Image Upload Preview
    // ============================================
    
    const coverImageInput = document.getElementById('coverImage');
    if (coverImageInput) {
        coverImageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('imagePreview');
                    preview.innerHTML = `
                        <div style="position: relative; display: inline-block; margin-top: 1rem;">
                            <img src="${e.target.result}" alt="Preview" style="max-width: 200px; border-radius: 0.75rem;">
                            <button type="button" onclick="clearImagePreview()" style="position: absolute; top: 0.5rem; right: 0.5rem; background: rgba(239, 68, 68, 0.9); color: white; border: none; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    `;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    window.clearImagePreview = function() {
        document.getElementById('coverImage').value = '';
        document.getElementById('imagePreview').innerHTML = '';
    };

    // ============================================
    // Drag & Drop File Upload
    // ============================================
    
    const fileUpload = document.querySelector('.file-upload');
    if (fileUpload) {
        const fileInput = fileUpload.querySelector('input[type="file"]');
        const fileLabel = fileUpload.querySelector('.file-label');
        
        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileUpload.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Highlight drop area
        ['dragenter', 'dragover'].forEach(eventName => {
            fileUpload.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            fileUpload.addEventListener(eventName, unhighlight, false);
        });

        function highlight() {
            fileUpload.style.border = '2px dashed var(--primary)';
            fileUpload.style.background = 'rgba(124, 58, 237, 0.05)';
        }

        function unhighlight() {
            fileUpload.style.border = '';
            fileUpload.style.background = '';
        }

        // Handle dropped files
        fileUpload.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                fileInput.files = files;
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        }
    }

    // ============================================
    // Form Validation
    // ============================================
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = 'var(--error)';
                    
                    // Reset border color after 2 seconds
                    setTimeout(() => {
                        field.style.borderColor = '';
                    }, 2000);
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Please fill in all required fields', 'error');
            }
        });
    });

    // ============================================
    // Export Functions
    // ============================================
    
    window.exportBooks = function() {
        showToast('Preparing export...', 'info');
        
        // Create CSV
        const table = document.querySelector('.modern-table');
        if (!table) return;
        
        let csv = [];
        const rows = table.querySelectorAll('tr');
        
        rows.forEach(row => {
            const cols = row.querySelectorAll('td, th');
            const rowData = [];
            cols.forEach((col, index) => {
                // Skip action columns
                if (index !== cols.length - 1) {
                    rowData.push(col.textContent.trim());
                }
            });
            csv.push(rowData.join(','));
        });
        
        // Download CSV
        const csvContent = csv.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `books_${Date.now()}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showToast('Export completed', 'success');
    };

    // ============================================
    // Statistics Chart (placeholder)
    // ============================================
    
    function initCharts() {
        // Placeholder for chart initialization
        // You can integrate Chart.js or any other library here
        console.log('Charts initialized');
    }

    // Initialize on load
    document.addEventListener('DOMContentLoaded', initCharts);

    console.log('%cAdmin Panel Ready', 'color: #7C3AED; font-weight: bold;');

})();
