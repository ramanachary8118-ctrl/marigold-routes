// ========================================
// Main JavaScript - Common Functionality
// ========================================

// ========================================
// API Helper Functions
// ========================================

class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const config = { ...defaultOptions, ...options };
        
        // Add auth token if exists
        const token = localStorage.getItem(APP_CONFIG.STORAGE_KEYS.ADMIN_TOKEN);
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
    
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }
    
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }
    
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }
    
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Initialize API client
const api = new APIClient(API_CONFIG.BASE_URL);

// ========================================
// Local Storage Helper
// ========================================

const Storage = {
    getBookings() {
        const bookings = localStorage.getItem(APP_CONFIG.STORAGE_KEYS.BOOKINGS);
        return bookings ? JSON.parse(bookings) : [];
    },
    
    saveBooking(booking) {
        const bookings = this.getBookings();
        bookings.push(booking);
        localStorage.setItem(APP_CONFIG.STORAGE_KEYS.BOOKINGS, JSON.stringify(bookings));
        this.updateBookingCount();
    },
    
    getBookingByReference(reference) {
        const bookings = this.getBookings();
        return bookings.find(b => b.reference === reference);
    },
    
    updateBooking(reference, updates) {
        const bookings = this.getBookings();
        const index = bookings.findIndex(b => b.reference === reference);
        if (index !== -1) {
            bookings[index] = { ...bookings[index], ...updates };
            localStorage.setItem(APP_CONFIG.STORAGE_KEYS.BOOKINGS, JSON.stringify(bookings));
        }
    },
    
    deleteBooking(reference) {
        const bookings = this.getBookings();
        const filtered = bookings.filter(b => b.reference !== reference);
        localStorage.setItem(APP_CONFIG.STORAGE_KEYS.BOOKINGS, JSON.stringify(filtered));
        this.updateBookingCount();
    },
    
    updateBookingCount() {
        const bookings = this.getBookings();
        const count = bookings.filter(b => b.status !== APP_CONFIG.BOOKING_STATUS.CANCELLED).length;
        const countElements = document.querySelectorAll('#bookingCount, .booking-count');
        countElements.forEach(el => {
            el.textContent = count;
        });
    },
};

// ========================================
// Mobile Navigation
// ========================================

function initMobileNav() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
            }
        });
    }
}

// ========================================
// Modal Functionality
// ========================================

class Modal {
    constructor(modalId) {
        this.modal = document.getElementById(modalId);
        if (!this.modal) return;
        
        this.closeBtn = this.modal.querySelector('.modal-close');
        
        // Close button click
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }
        
        // Click outside to close
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });
        
        // ESC key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen()) {
                this.close();
            }
        });
    }
    
    open() {
        if (this.modal) {
            this.modal.classList.remove('hidden');
            this.modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        }
    }
    
    close() {
        if (this.modal) {
            this.modal.classList.remove('show');
            this.modal.classList.add('hidden');
            document.body.style.overflow = '';
        }
    }
    
    isOpen() {
        return this.modal && this.modal.classList.contains('show');
    }
    
    setContent(html) {
        const content = this.modal.querySelector('.modal-content > div');
        if (content) {
            content.innerHTML = html;
        }
    }
}

// ========================================
// Form Validation
// ========================================

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
        
        // Email validation
        if (input.type === 'email' && input.value && !isValidEmail(input.value)) {
            isValid = false;
            input.classList.add('error');
        }
        
        // Phone validation
        if (input.type === 'tel' && input.value && !isValidPhone(input.value)) {
            isValid = false;
            input.classList.add('error');
        }
    });
    
    return isValid;
}

// ========================================
// Image Placeholder Generator
// ========================================

function generatePlaceholderImage(width, height, text) {
    // Returns a data URL for a placeholder image
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    
    // Background
    ctx.fillStyle = '#E8D5C0';
    ctx.fillRect(0, 0, width, height);
    
    // Text
    ctx.fillStyle = '#2C5F2D';
    ctx.font = 'bold 20px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, width / 2, height / 2);
    
    return canvas.toDataURL();
}

// ========================================
// Notification System
// ========================================

function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background-color: ${type === 'success' ? '#27AE60' : type === 'error' ? '#E74C3C' : '#3498DB'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// ========================================
// Date Utilities
// ========================================

function setDateLimits(dateInput) {
    if (dateInput) {
        dateInput.min = getMinStartDate();
        dateInput.max = getMaxStartDate();
    }
}

function calculateEndDate(startDate, nights) {
    const start = new Date(startDate);
    const end = new Date(start);
    end.setDate(start.getDate() + nights);
    return end;
}

// ========================================
// Price Calculator
// ========================================

class PriceCalculator {
    constructor(packagePrice, nights) {
        this.basePrice = packagePrice;
        this.nights = nights;
    }
    
    calculate(options) {
        const {
            adults = 2,
            children = 0,
            hotelCategory = 'standard',
            airportPickup = false,
            insurance = false,
            photographer = false,
        } = options;
        
        // Base package price for first 2 adults
        let total = this.basePrice;
        
        // Additional adults
        if (adults > 2) {
            total += (adults - 2) * (this.basePrice * 0.7); // 70% for additional adults
        }
        
        // Children
        total += children * (this.basePrice * (1 - APP_CONFIG.CHILD_DISCOUNT));
        
        // Hotel upgrade
        const upgradePerNight = APP_CONFIG.HOTEL_UPGRADES[hotelCategory];
        const hotelUpgradeCost = upgradePerNight * this.nights * adults;
        total += hotelUpgradeCost;
        
        // Extras
        let extrasCost = 0;
        if (airportPickup) extrasCost += APP_CONFIG.EXTRAS.airportPickup;
        if (insurance) extrasCost += APP_CONFIG.EXTRAS.insurance * (adults + children);
        if (photographer) extrasCost += APP_CONFIG.EXTRAS.photographer;
        
        total += extrasCost;
        
        // GST
        const gst = calculateGST(total);
        const finalTotal = total + gst;
        
        return {
            basePrice: this.basePrice,
            travellersPrice: total - this.basePrice - hotelUpgradeCost - extrasCost,
            hotelUpgrade: hotelUpgradeCost,
            extras: extrasCost,
            subtotal: total,
            gst: gst,
            total: Math.round(finalTotal),
        };
    }
}

// ========================================
// Initialize on Page Load
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize mobile navigation
    initMobileNav();
    
    // Update booking count
    Storage.updateBookingCount();
    
    // Set up date inputs
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => setDateLimits(input));
    
    // Add form validation on submit
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!validateForm(form)) {
                e.preventDefault();
                showNotification('Please fill in all required fields correctly', 'error');
            }
        });
    });
});

// ========================================
// Error Handling
// ========================================

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('An error occurred. Please try again.', 'error');
});

// ========================================
// Export for use in other modules
// ========================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        api,
        APIClient,
        Storage,
        Modal,
        PriceCalculator,
        validateForm,
        generatePlaceholderImage,
        showNotification,
        setDateLimits,
        calculateEndDate,
    };
}
