# Frontend JavaScript Implementation Guide

This document outlines the JavaScript files that need to be created to connect the frontend to the backend APIs.

## Files to Create

1. `frontend/assets/js/destinations.js` - Destinations page
2. `frontend/assets/js/packages.js` - Packages listing page
3. `frontend/assets/js/package-details.js` - Individual package details
4. `frontend/assets/js/booking.js` - Booking form and flow
5. `frontend/assets/js/my-bookings.js` - Booking lookup and management
6. `frontend/assets/js/contact.js` - Contact form
7. `frontend/assets/js/admin.js` - Admin dashboard

---

## 1. destinations.js

**Purpose:** Load and display destinations from API

**Key Functions Needed:**
```javascript
// Load all destinations
async function loadDestinations() {
    // GET /api/destinations
    // Render destination cards
}

// Filter destinations by category
function filterDestinations(category) {
    // Apply category filter
}

// Search destinations
function searchDestinations(query) {
    // Filter by search term
}

// Show destination modal
function showDestinationDetail(destinationId) {
    // GET /api/destinations/:id
    // Display in modal
}
```

**Integration Points:**
- Filters: `#categoryFilter`
- Search: `#searchInput`
- Grid: `#destinationsGrid`
- Modal: `#destinationModal`

---

## 2. packages.js

**Purpose:** Load and display packages with sorting and filtering

**Key Functions Needed:**
```javascript
// Load all packages
async function loadPackages() {
    // GET /api/packages
    // Render package cards
}

// Sort packages
function sortPackages(sortBy) {
    // Apply sorting
}

// Filter by destination
function filterByDestination(destinationId) {
    // Filter packages
}

// Navigate to package details
function viewPackage(packageId) {
    // Redirect to package-details.html?id=packageId
}
```

**Integration Points:**
- Sort dropdown: `#sortBy`
- Destination filter: `#destinationFilter`
- Search: `#searchInput`
- Grid: `#packagesGrid`

---

## 3. package-details.js

**Purpose:** Display complete package information and itinerary

**Key Functions Needed:**
```javascript
// Load package details
async function loadPackageDetails() {
    const packageId = new URLSearchParams(window.location.search).get('id');
    // GET /api/packages/:id?include_itinerary=true
    // Populate all fields
}

// Render itinerary
function renderItinerary(itinerary) {
    // Display day-by-day plan
}

// Book now button
function bookPackage(packageId) {
    // Redirect to booking.html?package=packageId
}

// Load related packages
async function loadRelatedPackages(packageId) {
    // GET /api/packages/:id/related
}
```

**Integration Points:**
- Package name: `#packageName`
- Description: `#packageDescription`
- Itinerary: `#itineraryContainer`
- Price: `#packagePrice`
- Book button: `#bookNowBtn`

---

## 4. booking.js (Most Complex)

**Purpose:** Complete booking flow with real-time pricing

**Key Functions Needed:**
```javascript
// Load packages for dropdown
async function loadPackageOptions() {
    // GET /api/packages
    // Populate #packageSelect
}

// Calculate price quote
async function calculatePrice() {
    const data = {
        package_id: packageId,
        adults: adults,
        children: children,
        hotel_category: category,
        airport_pickup: pickup,
        insurance: insurance,
        photographer: photographer
    };
    // POST /api/bookings/quote
    // Update price display
}

// Submit booking
async function submitBooking(e) {
    e.preventDefault();
    
    // Validate form
    if (!validateForm(form)) return;
    
    const bookingData = {
        package_id: packageId,
        start_date: startDate,
        adults: adults,
        children: children,
        hotel_category: category,
        airport_pickup: pickup,
        insurance: insurance,
        photographer: photographer,
        special_requests: requests,
        customer: {
            full_name: name,
            email: email,
            phone: phone
        }
    };
    
    // POST /api/bookings
    // On success: Save to localStorage and show confirmation
    // Then create payment order
}

// Create payment order
async function createPaymentOrder(bookingId) {
    // POST /api/payments/create-order
    // Open Razorpay checkout
}

// Handle Razorpay payment
function initiatePayment(orderData) {
    const options = {
        key: RAZORPAY_CONFIG.KEY_ID,
        amount: orderData.amount * 100,
        currency: orderData.currency,
        name: 'Marigold Routes',
        order_id: orderData.order_id,
        handler: function(response) {
            verifyPayment(response);
        }
    };
    
    const rzp = new Razorpay(options);
    rzp.open();
}

// Verify payment
async function verifyPayment(paymentData) {
    // POST /api/payments/verify
    // Show success message
}
```

**Integration Points:**
- Form: `#bookingForm`
- Package select: `#packageSelect`
- All form inputs
- Price summary: `#priceDetails`
- Confirmation modal: `#confirmationModal`

**Important:**
- Recalculate price on any change
- Validate all inputs before submission
- Never trust frontend pricing - verify with backend
- Handle all error states
- Show loading indicators

---

## 5. my-bookings.js

**Purpose:** Look up and display bookings

**Key Functions Needed:**
```javascript
// Load bookings from localStorage
function loadLocalBookings() {
    const bookings = Storage.getBookings();
    // Display booking cards
}

// Look up booking by reference
async function lookupBooking(e) {
    e.preventDefault();
    
    const reference = document.getElementById('lookupReference').value;
    const email = document.getElementById('lookupEmail').value;
    
    // POST /api/bookings/lookup
    const response = await api.post('/bookings/lookup', { reference, email });
    
    // Display booking details in modal
    showBookingDetail(response.booking);
}

// Show booking detail modal
function showBookingDetail(booking) {
    // Display complete booking information
    // Show cancellation option if eligible
}

// Cancel booking
async function cancelBooking(bookingId, email) {
    if (!confirm('Are you sure you want to cancel this booking?')) return;
    
    const reason = prompt('Please provide a cancellation reason (optional):');
    
    // POST /api/bookings/:id/cancel
    const response = await api.post(`/bookings/${bookingId}/cancel`, {
        email: email,
        reason: reason
    });
    
    // Show cancellation confirmation with refund info
    showCancellationConfirmation(response.booking);
}
```

**Integration Points:**
- Local bookings list: `#bookingsList`
- Lookup form: `#lookupForm`
- Booking detail modal: `#bookingModal`
- Empty state: `#emptyState`

---

## 6. contact.js

**Purpose:** Handle contact form submission

**Key Functions Needed:**
```javascript
// Submit contact form
async function submitContactForm(e) {
    e.preventDefault();
    
    // Validate
    if (!validateForm(contactForm)) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    const data = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        subject: document.getElementById('subject').value,
        message: document.getElementById('message').value
    };
    
    try {
        showLoading('#contactForm');
        
        // POST /api/contact
        const response = await api.post('/contact', data);
        
        // Hide form, show success message
        document.getElementById('contactForm').classList.add('hidden');
        document.getElementById('successMessage').classList.remove('hidden');
        
        showNotification('Your message has been sent!', 'success');
    } catch (error) {
        showNotification('Failed to send message. Please try again.', 'error');
    }
}

// Send another message
function sendAnother() {
    document.getElementById('successMessage').classList.add('hidden');
    document.getElementById('contactForm').classList.remove('hidden');
    document.getElementById('contactForm').reset();
}
```

**Integration Points:**
- Contact form: `#contactForm`
- Success message: `#successMessage`
- Send another button: `#sendAnother`

---

## 7. admin.js (Most Complex)

**Purpose:** Complete admin dashboard functionality

**Key Functions Needed:**
```javascript
// Admin login
async function adminLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('adminUsername').value;
    const password = document.getElementById('adminPassword').value;
    
    try {
        // POST /api/admin/login
        const response = await api.post('/admin/login', { username, password });
        
        // Save token
        localStorage.setItem(APP_CONFIG.STORAGE_KEYS.ADMIN_TOKEN, response.token);
        localStorage.setItem(APP_CONFIG.STORAGE_KEYS.ADMIN_USER, JSON.stringify(response.admin));
        
        // Show dashboard
        showAdminDashboard();
    } catch (error) {
        showError('#loginError', 'Invalid username or password');
    }
}

// Load dashboard
async function loadDashboard() {
    try {
        // GET /api/admin/dashboard
        const response = await api.get('/admin/dashboard');
        
        // Update statistics
        document.getElementById('statTotalBookings').textContent = response.stats.total_bookings;
        document.getElementById('statPendingBookings').textContent = response.stats.pending_bookings;
        // ... etc
        
        // Load recent bookings
        renderRecentBookings(response.recent_bookings);
        renderUpcomingDepartures(response.upcoming_departures);
    } catch (error) {
        if (error.status === 401) {
            logout();
        }
    }
}

// Load bookings
async function loadBookings(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        // GET /api/admin/bookings
        const response = await api.get(`/admin/bookings?${params}`);
        
        renderBookingsTable(response.bookings);
    } catch (error) {
        showError('Failed to load bookings');
    }
}

// Load enquiries
async function loadEnquiries(status = 'all') {
    // GET /api/admin/enquiries?status=:status
}

// Navigation
function switchSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.admin-section').forEach(s => s.classList.add('hidden'));
    
    // Show selected section
    document.getElementById(`section-${sectionName}`).classList.remove('hidden');
    
    // Update active menu item
    document.querySelectorAll('.admin-menu-item').forEach(m => m.classList.remove('active'));
    document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');
    
    // Load section data
    switch(sectionName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'bookings':
            loadBookings();
            break;
        case 'enquiries':
            loadEnquiries();
            break;
        // ... etc
    }
}

// Logout
function logout() {
    localStorage.removeItem(APP_CONFIG.STORAGE_KEYS.ADMIN_TOKEN);
    localStorage.removeItem(APP_CONFIG.STORAGE_KEYS.ADMIN_USER);
    showLoginScreen();
}
```

**Integration Points:**
- Login screen: `#loginScreen`
- Dashboard: `#adminDashboard`
- All sections: `#section-*`
- Navigation: `.admin-menu-item`
- Stats: `#stat*`

---

## Common Patterns to Use

### API Calls with Error Handling
```javascript
try {
    showLoading('#someElement');
    const response = await api.get('/endpoint');
    // Process response
    hideLoading();
} catch (error) {
    hideLoading();
    showNotification(error.message, 'error');
}
```

### Form Validation
```javascript
function validateBookingForm() {
    const form = document.getElementById('bookingForm');
    
    if (!validateForm(form)) {
        return false;
    }
    
    // Additional custom validation
    const startDate = new Date(document.getElementById('startDate').value);
    if (startDate <= new Date()) {
        showNotification('Start date must be in the future', 'error');
        return false;
    }
    
    return true;
}
```

### Update Price Display
```javascript
function updatePriceDisplay(pricing) {
    document.getElementById('basePrice').textContent = formatCurrency(pricing.base_price);
    document.getElementById('travellersPrice').textContent = formatCurrency(pricing.travellers_price);
    document.getElementById('hotelUpgradePrice').textContent = formatCurrency(pricing.hotel_upgrade_price);
    document.getElementById('extrasPrice').textContent = formatCurrency(pricing.extras_price);
    document.getElementById('subtotal').textContent = formatCurrency(pricing.subtotal);
    document.getElementById('gst').textContent = formatCurrency(pricing.gst);
    document.getElementById('total').textContent = formatCurrency(pricing.total);
}
```

---

## Testing Checklist

For each JavaScript file, test:
- [ ] API calls work correctly
- [ ] Error handling works
- [ ] Loading indicators show
- [ ] Success messages display
- [ ] Forms validate properly
- [ ] Navigation works
- [ ] Mobile responsive
- [ ] Browser console has no errors

---

## Razorpay Integration

Add to `<head>` of booking.html:
```html
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
```

Test cards (use in test mode):
- Success: 4111 1111 1111 1111
- Failure: 4111 1111 1111 1112

---

## Next Steps

1. Start with `destinations.js` (simplest)
2. Then `packages.js`
3. Then `package-details.js`
4. Then `contact.js` (simple form)
5. Then `booking.js` (most complex)
6. Then `my-bookings.js`
7. Finally `admin.js` (most comprehensive)

Test each file thoroughly before moving to the next!
