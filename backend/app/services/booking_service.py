"""
Booking Service - Business logic for bookings
"""
from app import db
from app.models import Booking, Customer, Package, BookingExtra
from app.services.pricing_service import PricingService
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError


class BookingService:
    """Service for managing bookings"""
    
    @staticmethod
    def create_booking(booking_data):
        """
        Create a new booking with validation
        
        Args:
            booking_data: dict containing booking information
        
        Returns:
            Booking object
        
        Raises:
            ValueError: If validation fails
        """
        # Validate required fields
        required_fields = ['package_id', 'start_date', 'adults', 'customer']
        for field in required_fields:
            if field not in booking_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Get package
        package = Package.query.get(booking_data['package_id'])
        if not package:
            raise ValueError("Package not found")
        
        if not package.is_active:
            raise ValueError("Package is not available")
        
        # Validate dates
        start_date = datetime.strptime(booking_data['start_date'], '%Y-%m-%d').date()
        today = datetime.utcnow().date()
        
        if start_date <= today:
            raise ValueError("Start date must be in the future")
        
        # Calculate end date
        end_date = start_date + timedelta(days=package.duration_nights)
        
        # Validate traveller counts
        adults = int(booking_data.get('adults', 2))
        children = int(booking_data.get('children', 0))
        
        if adults < 1 or adults > 10:
            raise ValueError("Number of adults must be between 1 and 10")
        if children < 0 or children > 5:
            raise ValueError("Number of children must be between 0 and 5")
        
        # Get or create customer
        customer_data = booking_data['customer']
        customer = Customer.query.filter_by(email=customer_data['email']).first()
        
        if not customer:
            customer = Customer(
                full_name=customer_data['full_name'],
                email=customer_data['email'],
                phone=customer_data['phone']
            )
            db.session.add(customer)
            db.session.flush()  # Get customer ID
        
        # Calculate pricing
        hotel_category = booking_data.get('hotel_category', 'standard')
        airport_pickup = booking_data.get('airport_pickup', False)
        insurance = booking_data.get('insurance', False)
        photographer = booking_data.get('photographer', False)
        
        pricing = PricingService.calculate_booking_price(
            package=package,
            adults=adults,
            children=children,
            nights=package.duration_nights,
            hotel_category=hotel_category,
            airport_pickup=airport_pickup,
            insurance=insurance,
            photographer=photographer
        )
        
        # Create package snapshot
        package_snapshot = {
            'package_id': package.id,
            'package_name': package.name,
            'destination_name': package.destination.name if package.destination else None,
            'duration_days': package.duration_days,
            'duration_nights': package.duration_nights,
            'base_price': package.base_price,
            'inclusions': package.inclusions,
            'exclusions': package.exclusions,
        }
        
        # Generate unique reference
        max_attempts = 10
        reference = None
        
        for _ in range(max_attempts):
            ref = Booking.generate_reference()
            if not Booking.query.filter_by(reference=ref).first():
                reference = ref
                break
        
        if not reference:
            raise ValueError("Could not generate unique booking reference")
        
        # Create booking
        booking = Booking(
            reference=reference,
            customer_id=customer.id,
            package_id=package.id,
            start_date=start_date,
            end_date=end_date,
            adults=adults,
            children=children,
            hotel_category=hotel_category,
            special_requests=booking_data.get('special_requests'),
            package_snapshot=package_snapshot,
            base_price=pricing['base_price'],
            travellers_price=pricing['travellers_price'],
            hotel_upgrade_price=pricing['hotel_upgrade_price'],
            extras_price=pricing['extras_price'],
            subtotal=pricing['subtotal'],
            gst=pricing['gst'],
            total_amount=pricing['total'],
            currency=pricing['currency'],
            status='pending',
            payment_status='pending'
        )
        
        db.session.add(booking)
        db.session.flush()  # Get booking ID
        
        # Add extras
        for extra in pricing['extras_breakdown']:
            booking_extra = BookingExtra(
                booking_id=booking.id,
                service_name=extra['name'],
                price=extra['price'],
                quantity=extra['quantity']
            )
            db.session.add(booking_extra)
        
        # Commit transaction
        try:
            db.session.commit()
            return booking
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError(f"Database error: {str(e)}")
    
    @staticmethod
    def get_booking(booking_id=None, reference=None):
        """Get booking by ID or reference"""
        if booking_id:
            return Booking.query.get(booking_id)
        elif reference:
            return Booking.query.filter_by(reference=reference).first()
        return None
    
    @staticmethod
    def lookup_booking(reference, email):
        """Look up booking by reference and email (secure guest access)"""
        booking = Booking.query.filter_by(reference=reference).first()
        
        if not booking:
            return None
        
        # Verify email matches
        if booking.customer.email.lower() != email.lower():
            return None
        
        return booking
    
    @staticmethod
    def cancel_booking(booking, reason=None):
        """
        Cancel a booking
        
        Args:
            booking: Booking object
            reason: Cancellation reason
        
        Returns:
            Updated booking
        """
        if booking.status == 'cancelled':
            raise ValueError("Booking is already cancelled")
        
        booking.status = 'cancelled'
        booking.cancelled_at = datetime.utcnow()
        booking.cancellation_reason = reason
        
        # Calculate refund based on cancellation policy
        # This is a placeholder - actual policy should be configurable
        days_until_departure = (booking.start_date - datetime.utcnow().date()).days
        
        if days_until_departure >= 30:
            refund_percentage = 0.90  # 90% refund
        elif days_until_departure >= 15:
            refund_percentage = 0.75  # 75% refund
        elif days_until_departure >= 8:
            refund_percentage = 0.50  # 50% refund
        elif days_until_departure >= 3:
            refund_percentage = 0.25  # 25% refund
        else:
            refund_percentage = 0.0  # No refund
        
        if booking.payment_status == 'success':
            booking.refund_amount = int(booking.total_amount * refund_percentage)
            booking.refund_status = 'requested'
        
        db.session.commit()
        return booking
    
    @staticmethod
    def update_booking_status(booking, status, payment_status=None):
        """Update booking status"""
        valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
        
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        booking.status = status
        
        if payment_status:
            booking.payment_status = payment_status
        
        db.session.commit()
        return booking
