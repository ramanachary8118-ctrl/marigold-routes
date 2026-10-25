"""
Pricing Service - Server-side price calculation
"""
from flask import current_app


class PricingService:
    """
    Server-side pricing engine
    NEVER trust prices from the frontend - always calculate on backend
    """
    
    # Service prices (per booking unless specified)
    EXTRAS_PRICING = {
        'airport_pickup': 1800,
        'insurance': 650,  # per person
        'photographer': 3500,
    }
    
    # Hotel upgrade prices (per night per room, assuming twin sharing)
    HOTEL_UPGRADES = {
        'standard': 0,
        'superior': 900,
        'luxury': 2400,
    }
    
    @staticmethod
    def calculate_booking_price(package, adults, children, nights, hotel_category='standard',
                                 airport_pickup=False, insurance=False, photographer=False):
        """
        Calculate complete booking price with itemized breakdown
        
        Args:
            package: Package object
            adults: Number of adults
            children: Number of children
            nights: Number of nights
            hotel_category: Hotel category (standard, superior, luxury)
            airport_pickup: Boolean
            insurance: Boolean
            photographer: Boolean
        
        Returns:
            dict with complete price breakdown
        """
        
        # Validate inputs
        if adults < 1:
            raise ValueError("At least 1 adult required")
        if adults > 10:
            raise ValueError("Maximum 10 adults allowed")
        if children < 0 or children > 5:
            raise ValueError("Invalid number of children")
        
        # Get pricing config
        gst_rate = current_app.config.get('GST_RATE', 0.05)
        child_discount_rate = current_app.config.get('CHILD_DISCOUNT_RATE', 0.30)
        
        # Base package price (includes first 2 adults, twin sharing)
        base_price = package.base_price
        
        # Calculate additional adults cost
        # Base price covers 2 adults. Additional adults pay 70% of base
        additional_adults = max(0, adults - 2)
        additional_adults_cost = int(additional_adults * base_price * 0.7)
        
        # Calculate children cost
        # Children pay 70% of adult fare (30% discount)
        child_price = int(base_price * (1 - child_discount_rate))
        children_cost = children * child_price
        
        # Total travellers cost (beyond base 2 adults)
        travellers_cost = additional_adults_cost + children_cost
        
        # Hotel upgrade cost
        # Calculate per night for all rooms needed
        # Assuming twin sharing: rooms = ceil(adults / 2)
        import math
        rooms_needed = math.ceil(adults / 2)
        
        # Get upgrade price per night from package or default
        if hotel_category == 'superior':
            upgrade_per_night = package.hotel_upgrade_superior or PricingService.HOTEL_UPGRADES['superior']
        elif hotel_category == 'luxury':
            upgrade_per_night = package.hotel_upgrade_luxury or PricingService.HOTEL_UPGRADES['luxury']
        else:
            upgrade_per_night = 0
        
        hotel_upgrade_cost = upgrade_per_night * nights * rooms_needed
        
        # Extras
        extras_cost = 0
        extras_breakdown = []
        
        if airport_pickup:
            cost = PricingService.EXTRAS_PRICING['airport_pickup']
            extras_cost += cost
            extras_breakdown.append({
                'name': 'Airport pick-up and drop',
                'price': cost,
                'quantity': 1
            })
        
        if insurance:
            cost = PricingService.EXTRAS_PRICING['insurance'] * (adults + children)
            extras_cost += cost
            extras_breakdown.append({
                'name': 'Travel insurance',
                'price': PricingService.EXTRAS_PRICING['insurance'],
                'quantity': adults + children
            })
        
        if photographer:
            cost = PricingService.EXTRAS_PRICING['photographer']
            extras_cost += cost
            extras_breakdown.append({
                'name': 'Half-day photographer',
                'price': cost,
                'quantity': 1
            })
        
        # Calculate subtotal
        subtotal = base_price + travellers_cost + hotel_upgrade_cost + extras_cost
        
        # Calculate GST
        gst = int(subtotal * gst_rate)
        
        # Calculate total
        total = subtotal + gst
        
        # Return complete breakdown
        return {
            'base_price': base_price,
            'travellers_price': travellers_cost,
            'travellers_breakdown': {
                'additional_adults': additional_adults,
                'additional_adults_cost': additional_adults_cost,
                'children': children,
                'children_cost': children_cost,
            },
            'hotel_upgrade_price': hotel_upgrade_cost,
            'hotel_upgrade_breakdown': {
                'category': hotel_category,
                'rooms_needed': rooms_needed,
                'nights': nights,
                'per_night_per_room': upgrade_per_night,
            },
            'extras_price': extras_cost,
            'extras_breakdown': extras_breakdown,
            'subtotal': subtotal,
            'gst': gst,
            'gst_rate': gst_rate,
            'total': total,
            'currency': package.currency or 'INR',
        }
    
    @staticmethod
    def validate_price(submitted_total, calculated_price):
        """
        Validate that the price submitted from frontend matches server calculation
        Returns True if valid, False otherwise
        """
        # Allow small rounding differences (up to 1 rupee)
        difference = abs(submitted_total - calculated_price['total'])
        return difference <= 1
