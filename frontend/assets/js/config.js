// ========================================
// API Configuration
// ========================================

const API_CONFIG = {
    // Backend API URL - Update this for production
    BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000/api'
        : 'https://your-backend-url.com/api', // Update with actual backend URL
    
    // API Endpoints
    ENDPOINTS: {
        // Destinations
        DESTINATIONS: '/destinations',
        DESTINATION_DETAIL: '/destinations/:id',
        
        // Packages
        PACKAGES: '/packages',
        PACKAGE_DETAIL: '/packages/:id',
        
        // Bookings
        BOOKINGS: '/bookings',
        BOOKING_DETAIL: '/bookings/:id',
        BOOKING_LOOKUP: '/bookings/lookup',
        BOOKING_CANCEL: '/bookings/:id/cancel',
        PRICE_QUOTE: '/bookings/quote',
        
        // Payments
        PAYMENT_ORDER: '/payments/create-order',
        PAYMENT_VERIFY: '/payments/verify',
        
        // Contact
        CONTACT: '/contact',
        
        // Admin
        ADMIN_LOGIN: '/admin/login',
        ADMIN_LOGOUT: '/admin/logout',
        ADMIN_DASHBOARD: '/admin/dashboard',
        ADMIN_BOOKINGS: '/admin/bookings',
        ADMIN_DESTINATIONS: '/admin/destinations',
        ADMIN_PACKAGES: '/admin/packages',
        ADMIN_ENQUIRIES: '/admin/enquiries',
    },
    
    // Request timeout in milliseconds
    TIMEOUT: 30000,
    
    // Retry configuration
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000,
};

// ========================================
// Application Constants
// ========================================

const APP_CONFIG = {
    // Pricing
    GST_RATE: 0.05, // 5% GST
    CHILD_DISCOUNT: 0.30, // Children pay 70% (30% discount)
    
    // Hotel Upgrades (per night)
    HOTEL_UPGRADES: {
        standard: 0,
        superior: 900,
        luxury: 2400,
    },
    
    // Additional Services
    EXTRAS: {
        airportPickup: 1800,
        insurance: 650, // per person
        photographer: 3500,
    },
    
    // Booking Status
    BOOKING_STATUS: {
        PENDING: 'pending',
        CONFIRMED: 'confirmed',
        CANCELLED: 'cancelled',
        COMPLETED: 'completed',
    },
    
    // Payment Status
    PAYMENT_STATUS: {
        PENDING: 'pending',
        SUCCESS: 'success',
        FAILED: 'failed',
        REFUNDED: 'refunded',
    },
    
    // Local Storage Keys
    STORAGE_KEYS: {
        BOOKINGS: 'marigold_bookings',
        ADMIN_TOKEN: 'marigold_admin_token',
        ADMIN_USER: 'marigold_admin_user',
    },
    
    // Date Configuration
    MIN_START_DATE_OFFSET: 1, // Start date must be at least 1 day from today
    MAX_ADVANCE_BOOKING_DAYS: 365, // Can book up to 1 year in advance
    
    // Validation
    MIN_ADULTS: 1,
    MAX_ADULTS: 10,
    MIN_CHILDREN: 0,
    MAX_CHILDREN: 5,
};

// ========================================
// Razorpay Configuration
// ========================================

const RAZORPAY_CONFIG = {
    // Key ID (public key) - Safe to expose in frontend
    KEY_ID: 'rzp_test_XXXXXXXXXX', // Replace with actual test key
    
    // Theme
    THEME: {
        color: '#D4A574', // Marigold primary color
    },
    
    // Currency
    CURRENCY: 'INR',
    
    // Company Info
    COMPANY: {
        name: 'Marigold Routes',
        description: 'Guided trips across India',
        logo: '', // Optional logo URL
    },
};

// ========================================
// Utility Functions
// ========================================

// Format currency
function formatCurrency(amount, includeCurrency = true) {
    const formatted = new Intl.NumberFormat('en-IN', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(amount);
    
    return includeCurrency ? `₹${formatted}` : formatted;
}

// Format date
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    return new Intl.DateFormat('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    }).format(date);
}

// Get minimum start date
function getMinStartDate() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + APP_CONFIG.MIN_START_DATE_OFFSET);
    return tomorrow.toISOString().split('T')[0];
}

// Get maximum start date
function getMaxStartDate() {
    const maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + APP_CONFIG.MAX_ADVANCE_BOOKING_DAYS);
    return maxDate.toISOString().split('T')[0];
}

// Calculate GST
function calculateGST(amount) {
    return Math.round(amount * APP_CONFIG.GST_RATE);
}

// Generate booking reference
function generateBookingReference() {
    const prefix = 'MR';
    const timestamp = Date.now().toString(36).toUpperCase();
    const random = Math.random().toString(36).substring(2, 6).toUpperCase();
    return `${prefix}${timestamp}${random}`;
}

// Validate email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validate phone number (Indian format)
function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[0-9]{10,15}$/;
    return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
}

// Show loading indicator
function showLoading(element) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    if (element) {
        element.innerHTML = `
            <div class="loading-indicator">
                <div class="spinner"></div>
                <p>Loading...</p>
            </div>
        `;
    }
}

// Show error message
function showError(element, message) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    if (element) {
        element.innerHTML = `
            <div class="error-message">
                <p>${message}</p>
            </div>
        `;
    }
}

// Show success message
function showSuccess(element, message) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    if (element) {
        element.innerHTML = `
            <div class="success-message">
                <p>${message}</p>
            </div>
        `;
    }
}

// Debounce function
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

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        API_CONFIG,
        APP_CONFIG,
        RAZORPAY_CONFIG,
        formatCurrency,
        formatDate,
        getMinStartDate,
        getMaxStartDate,
        calculateGST,
        generateBookingReference,
        isValidEmail,
        isValidPhone,
        showLoading,
        showError,
        showSuccess,
        debounce,
    };
}
