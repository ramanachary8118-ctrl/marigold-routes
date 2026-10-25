-- Marigold Routes Database Schema
-- PostgreSQL Database Schema

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS audit_logs CASCADE;
DROP TABLE IF EXISTS contact_enquiries CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS booking_extras CASCADE;
DROP TABLE IF EXISTS booking_travellers CASCADE;
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS package_itineraries CASCADE;
DROP TABLE IF EXISTS packages CASCADE;
DROP TABLE IF EXISTS destinations CASCADE;
DROP TABLE IF EXISTS admins CASCADE;

-- Admins table
CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    full_name VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_superadmin BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_admins_username ON admins(username);
CREATE INDEX idx_admins_email ON admins(email);

-- Destinations table
CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    main_image VARCHAR(500),
    highlights JSONB,
    best_months JSONB,
    recommended_duration INTEGER,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_destinations_slug ON destinations(slug);
CREATE INDEX idx_destinations_category ON destinations(category);
CREATE INDEX idx_destinations_active ON destinations(is_active);

-- Packages table
CREATE TABLE packages (
    id SERIAL PRIMARY KEY,
    destination_id INTEGER NOT NULL REFERENCES destinations(id) ON DELETE RESTRICT,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    duration_days INTEGER NOT NULL,
    duration_nights INTEGER NOT NULL,
    base_price INTEGER NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    inclusions JSONB,
    exclusions JSONB,
    accommodation_type VARCHAR(100),
    hotel_upgrade_superior INTEGER DEFAULT 900,
    hotel_upgrade_luxury INTEGER DEFAULT 2400,
    highlights JSONB,
    main_image VARCHAR(500),
    gallery_images JSONB,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_packages_slug ON packages(slug);
CREATE INDEX idx_packages_destination ON packages(destination_id);
CREATE INDEX idx_packages_active ON packages(is_active);
CREATE INDEX idx_packages_featured ON packages(is_featured);

-- Package Itineraries table
CREATE TABLE package_itineraries (
    id SERIAL PRIMARY KEY,
    package_id INTEGER NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
    day_number INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    activities JSONB,
    meals JSONB,
    accommodation VARCHAR(200),
    UNIQUE(package_id, day_number)
);

CREATE INDEX idx_itineraries_package ON package_itineraries(package_id);

-- Customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_email ON customers(email);

-- Bookings table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    reference VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    package_id INTEGER NOT NULL REFERENCES packages(id) ON DELETE RESTRICT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    adults INTEGER NOT NULL,
    children INTEGER DEFAULT 0,
    hotel_category VARCHAR(50) DEFAULT 'standard',
    special_requests TEXT,
    package_snapshot JSONB NOT NULL,
    base_price INTEGER NOT NULL,
    travellers_price INTEGER DEFAULT 0,
    hotel_upgrade_price INTEGER DEFAULT 0,
    extras_price INTEGER DEFAULT 0,
    subtotal INTEGER NOT NULL,
    gst INTEGER NOT NULL,
    total_amount INTEGER NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'pending',
    cancelled_at TIMESTAMP,
    cancellation_reason TEXT,
    refund_amount INTEGER,
    refund_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_bookings_reference ON bookings(reference);
CREATE INDEX idx_bookings_customer ON bookings(customer_id);
CREATE INDEX idx_bookings_package ON bookings(package_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_start_date ON bookings(start_date);
CREATE INDEX idx_bookings_created_at ON bookings(created_at);

-- Booking Travellers table
CREATE TABLE booking_travellers (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    full_name VARCHAR(200) NOT NULL,
    age INTEGER,
    is_child BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_travellers_booking ON booking_travellers(booking_id);

-- Booking Extras table
CREATE TABLE booking_extras (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    service_name VARCHAR(100) NOT NULL,
    service_description VARCHAR(200),
    price INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1
);

CREATE INDEX idx_extras_booking ON booking_extras(booking_id);

-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id) ON DELETE RESTRICT,
    razorpay_order_id VARCHAR(100) UNIQUE,
    razorpay_payment_id VARCHAR(100) UNIQUE,
    razorpay_signature VARCHAR(500),
    amount INTEGER NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    status VARCHAR(50) DEFAULT 'pending',
    payment_method VARCHAR(50),
    webhook_received BOOLEAN DEFAULT FALSE,
    webhook_data JSONB,
    refund_id VARCHAR(100),
    refund_amount INTEGER,
    refund_status VARCHAR(50),
    refunded_at TIMESTAMP,
    error_code VARCHAR(100),
    error_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMP
);

CREATE INDEX idx_payments_booking ON payments(booking_id);
CREATE INDEX idx_payments_order_id ON payments(razorpay_order_id);
CREATE INDEX idx_payments_payment_id ON payments(razorpay_payment_id);
CREATE INDEX idx_payments_status ON payments(status);

-- Contact Enquiries table
CREATE TABLE contact_enquiries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'unread',
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    replied_at TIMESTAMP
);

CREATE INDEX idx_enquiries_status ON contact_enquiries(status);
CREATE INDEX idx_enquiries_created_at ON contact_enquiries(created_at);

-- Audit Logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER REFERENCES admins(id) ON DELETE SET NULL,
    user_type VARCHAR(50),
    user_identifier VARCHAR(200),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id INTEGER,
    description TEXT,
    metadata JSONB,
    ip_address VARCHAR(50),
    user_agent TEXT,
    status VARCHAR(50) DEFAULT 'success',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_audit_admin ON audit_logs(admin_id);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created_at ON audit_logs(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add triggers for updated_at
CREATE TRIGGER update_admins_updated_at BEFORE UPDATE ON admins
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_destinations_updated_at BEFORE UPDATE ON destinations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_packages_updated_at BEFORE UPDATE ON packages
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookings_updated_at BEFORE UPDATE ON bookings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_enquiries_updated_at BEFORE UPDATE ON contact_enquiries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE destinations IS 'Travel destinations across India';
COMMENT ON TABLE packages IS 'Travel packages with pricing and itineraries';
COMMENT ON TABLE bookings IS 'Customer bookings with complete pricing snapshot';
COMMENT ON TABLE payments IS 'Payment transactions via Razorpay';
COMMENT ON TABLE audit_logs IS 'Audit trail for important system actions';
