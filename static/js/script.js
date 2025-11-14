/**
 * Library Management System - Main JavaScript
 * Modern, Interactive, Vanilla JS
 */

(function() {
    'use strict';

    // ============================================
    // Global Variables
    // ============================================
    let currentTheme = localStorage.getItem('theme') || 'dark';
    
    // ============================================
    // Initialize on DOM Load
    // ============================================
    document.addEventListener('DOMContentLoaded', function() {
        initTheme();
        initSidebar();
        initProfileDropdown();
        initNotificationDropdown();
        initGlobalSearch();
        initTabSystem();
        initPageAnimations();
        initTooltips();
    });

    // ============================================
    // Theme Management
    // ============================================
    function initTheme() {
        document.body.setAttribute('data-theme', currentTheme);
        
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            updateThemeIcon();
            themeToggle.addEventListener('click', toggleTheme);
        }
    }

    function toggleTheme() {
        currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.body.setAttribute('data-theme', currentTheme);
        localStorage.setItem('theme', currentTheme);
        updateThemeIcon();
        
        // Smooth transition
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    function updateThemeIcon() {
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (currentTheme === 'dark') {
                icon.className = 'fas fa-sun';
            } else {
                icon.className = 'fas fa-moon';
            }
        }
    }

    // ============================================
    // Sidebar Management
    // ============================================
    function initSidebar() {
        const sidebarToggle = document.getElementById('sidebarToggle');
        const sidebar = document.getElementById('sidebar');
        
        if (sidebarToggle && sidebar) {
            sidebarToggle.addEventListener('click', function() {
                document.body.classList.toggle('sidebar-open');
            });
            
            // Close sidebar on mobile when clicking outside
            document.addEventListener('click', function(e) {
                if (window.innerWidth <= 1024) {
                    if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                        document.body.classList.remove('sidebar-open');
                    }
                }
            });
        }
    }

    // ============================================
    // Profile Dropdown
    // ============================================
    function initProfileDropdown() {
        const profileBtn = document.getElementById('profileBtn');
        const profileMenu = document.getElementById('profileMenu');
        
        if (profileBtn && profileMenu) {
            profileBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                profileMenu.classList.toggle('active');
            });
            
            document.addEventListener('click', function(e) {
                if (!profileMenu.contains(e.target) && !profileBtn.contains(e.target)) {
                    profileMenu.classList.remove('active');
                }
            });
        }
    }

    // ============================================
    // Notification Dropdown
    // ============================================
    function initNotificationDropdown() {
        const notifBtn = document.getElementById('notificationBtn');
        const notifDropdown = document.getElementById('notificationDropdown');
        
        if (notifBtn && notifDropdown) {
            notifBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                notifDropdown.classList.toggle('active');
            });
            
            document.addEventListener('click', function(e) {
                if (!notifDropdown.contains(e.target) && !notifBtn.contains(e.target)) {
                    notifDropdown.classList.remove('active');
                }
            });
        }
    }

    // Global function for marking all notifications as read
    window.markAllRead = function(e) {
        e.preventDefault();
        fetch('/notifications/mark-all-read/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(err => console.error('Error marking notifications as read:', err));
    };

    // Helper to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ============================================
    // Global Search
    // ============================================
    function initGlobalSearch() {
        const globalSearch = document.getElementById('globalSearch');
        
        if (globalSearch) {
            let searchTimeout;
            
            globalSearch.addEventListener('input', function(e) {
                clearTimeout(searchTimeout);
                const query = e.target.value.trim();
                
                if (query.length >= 2) {
                    searchTimeout = setTimeout(() => {
                        performSearch(query);
                    }, 500);
                }
            });
            
            globalSearch.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const query = e.target.value.trim();
                    if (query.length >= 2) {
                        window.location.href = `/search?q=${encodeURIComponent(query)}`;
                    }
                }
            });
        }
    }

    function performSearch(query) {
        // AJAX search implementation
        console.log('Searching for:', query);
        // You can implement live search results here
    }

    // ============================================
    // Tab System (for Admin Panel)
    // ============================================
    function initTabSystem() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const targetTab = this.getAttribute('data-tab');
                
                // Remove active class from all buttons and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked button and corresponding content
                this.classList.add('active');
                const targetContent = document.getElementById(`${targetTab}-tab`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
            });
        });
    }

    // ============================================
    // Page Animations
    // ============================================
    function initPageAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);
        
        // Observe elements with fade-in class
        document.querySelectorAll('.hover-lift').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }

    // ============================================
    // Tooltips
    // ============================================
    function initTooltips() {
        const tooltipElements = document.querySelectorAll('[title]');
        
        tooltipElements.forEach(el => {
            el.addEventListener('mouseenter', showTooltip);
            el.addEventListener('mouseleave', hideTooltip);
        });
    }

    function showTooltip(e) {
        const title = this.getAttribute('title');
        if (!title) return;
        
        // Store original title and remove it
        this.setAttribute('data-title', title);
        this.removeAttribute('title');
        
        // Create tooltip element
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = title;
        tooltip.style.cssText = `
            position: absolute;
            background: var(--bg-dark-tertiary);
            color: var(--text-primary);
            padding: 0.5rem 0.75rem;
            border-radius: 0.5rem;
            font-size: 0.875rem;
            pointer-events: none;
            z-index: 10000;
            white-space: nowrap;
            box-shadow: var(--shadow-lg);
        `;
        
        document.body.appendChild(tooltip);
        
        // Position tooltip
        const rect = this.getBoundingClientRect();
        tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
        tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
        
        this.tooltipElement = tooltip;
    }

    function hideTooltip() {
        if (this.tooltipElement) {
            this.tooltipElement.remove();
            this.tooltipElement = null;
        }
        
        // Restore original title
        const title = this.getAttribute('data-title');
        if (title) {
            this.setAttribute('title', title);
            this.removeAttribute('data-title');
        }
    }

    // ============================================
    // Toast Notifications
    // ============================================
    window.showToast = function(message, type = 'info', duration = 3000) {
        const container = document.getElementById('toast-container') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = getToastIcon(type);
        toast.innerHTML = `
            <i class="fas ${icon}"></i>
            <span>${message}</span>
        `;
        
        container.appendChild(toast);
        
        // Auto remove
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    };

    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
        return container;
    }

    function getToastIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-times-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    // ============================================
    // Form Validation
    // ============================================
    window.validateForm = function(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;
        
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('error');
                isValid = false;
            } else {
                input.classList.remove('error');
            }
        });
        
        if (!isValid) {
            showToast('Please fill in all required fields', 'error');
        }
        
        return isValid;
    };

    // ============================================
    // Image Preview
    // ============================================
    window.previewImage = function(input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            
            reader.onload = function(e) {
                const preview = document.getElementById('imagePreview');
                if (preview) {
                    preview.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 100%; border-radius: 0.75rem; margin-top: 1rem;">`;
                }
            };
            
            reader.readAsDataURL(input.files[0]);
        }
    };

    // Add event listener for file inputs
    document.addEventListener('change', function(e) {
        if (e.target.type === 'file' && e.target.accept.includes('image')) {
            previewImage(e.target);
        }
    });

    // ============================================
    // Smooth Scroll
    // ============================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ============================================
    // Loading States
    // ============================================
    window.setLoading = function(element, isLoading) {
        if (isLoading) {
            element.disabled = true;
            element.classList.add('loading');
            element.dataset.originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        } else {
            element.disabled = false;
            element.classList.remove('loading');
            if (element.dataset.originalText) {
                element.innerHTML = element.dataset.originalText;
                delete element.dataset.originalText;
            }
        }
    };

    // ============================================
    // Confirmation Dialog
    // ============================================
    window.confirmAction = function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    };

    // ============================================
    // Debounce Utility
    // ============================================
    window.debounce = function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };

    // ============================================
    // Export Functions
    // ============================================
    window.exportBooks = function() {
        showToast('Exporting books...', 'info');
        // Implementation for export
    };

    window.printBooks = function() {
        window.print();
    };

    // ============================================
    // Auto-save Draft
    // ============================================
    window.autoSaveDraft = debounce(function(formData) {
        localStorage.setItem('draft', JSON.stringify(formData));
        console.log('Draft saved');
    }, 2000);

    // ============================================
    // Console Warning
    // ============================================
    console.log('%cLibrary Management System', 'color: #7C3AED; font-size: 24px; font-weight: bold;');
    console.log('%c⚠️ Warning: Do not paste any code here unless you know what you are doing!', 'color: #EF4444; font-size: 16px;');

    // ============================================
    // Loading Spinner Utilities
    // ============================================
    window.showLoading = function() {
        let spinner = document.getElementById('globalSpinner');
        if (!spinner) {
            spinner = document.createElement('div');
            spinner.id = 'globalSpinner';
            spinner.className = 'spinner-overlay';
            spinner.innerHTML = '<div class="spinner"></div>';
            document.body.appendChild(spinner);
        }
        setTimeout(() => spinner.classList.add('active'), 10);
    };

    window.hideLoading = function() {
        const spinner = document.getElementById('globalSpinner');
        if (spinner) {
            spinner.classList.remove('active');
        }
    };

    // Button loading state
    window.setButtonLoading = function(button, loading = true) {
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
            button.dataset.originalText = button.innerHTML;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
            if (button.dataset.originalText) {
                button.innerHTML = button.dataset.originalText;
            }
        }
    };

    // ============================================
    // Toast Notification System
    // ============================================
    let toastContainer = null;
    let toastQueue = [];
    let activeToasts = 0;
    const MAX_TOASTS = 3;

    function createToastContainer() {
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
        }
        return toastContainer;
    }

    window.showToast = function(message, type = 'info', duration = 4000, title = '') {
        const container = createToastContainer();
        
        // Queue system to prevent too many toasts
        if (activeToasts >= MAX_TOASTS) {
            toastQueue.push({ message, type, duration, title });
            return;
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-times-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        const titles = {
            success: title || 'Success',
            error: title || 'Error',
            warning: title || 'Warning',
            info: title || 'Info'
        };

        toast.innerHTML = `
            <div class="toast-icon">
                <i class="fas ${icons[type]}"></i>
            </div>
            <div class="toast-content">
                <div class="toast-title">${titles[type]}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove(); activeToasts--; processToastQueue();">
                <i class="fas fa-times"></i>
            </button>
        `;

        container.appendChild(toast);
        activeToasts++;

        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto remove
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
                activeToasts--;
                processToastQueue();
            }, 400);
        }, duration);
    };

    function processToastQueue() {
        if (toastQueue.length > 0 && activeToasts < MAX_TOASTS) {
            const next = toastQueue.shift();
            window.showToast(next.message, next.type, next.duration, next.title);
        }
    }

    // Convenience methods
    window.toastSuccess = (msg, title) => showToast(msg, 'success', 4000, title);
    window.toastError = (msg, title) => showToast(msg, 'error', 5000, title);
    window.toastWarning = (msg, title) => showToast(msg, 'warning', 4500, title);
    window.toastInfo = (msg, title) => showToast(msg, 'info', 3500, title);

    // ============================================
    // Form Submission with Loading
    // ============================================
    window.handleFormSubmit = function(form, callback) {
        const submitBtn = form.querySelector('[type="submit"]');
        
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            setButtonLoading(submitBtn, true);
            showLoading();
            
            try {
                await callback(new FormData(form));
                toastSuccess('Operation completed successfully!');
            } catch (error) {
                toastError(error.message || 'An error occurred');
            } finally {
                setButtonLoading(submitBtn, false);
                hideLoading();
            }
        });
    };

    // ============================================
    // Fade-in Animation for Page Load
    // ============================================
    function initPageAnimations() {
        const elements = document.querySelectorAll('.dashboard-card, .glass-card, .stat-card');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            setTimeout(() => {
                el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }, index * 50);
        });
    }

})();

