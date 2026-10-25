"""
Seed Data Script for Marigold Routes
Populates the database with sample destinations and packages
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.app import create_app, db
from backend.app.models import Destination, Package, PackageItinerary, Admin

def seed_destinations():
    """Seed destinations"""
    destinations = [
        {
            'name': 'Manali',
            'slug': 'manali',
            'description': 'Nestled in the mountains of Himachal Pradesh, Manali offers stunning views, adventure sports, and serene landscapes.',
            'category': 'mountains',
            'region': 'Himachal Pradesh',
            'main_image': '/assets/images/manali.jpg',
            'highlights': ['Snow-capped peaks', 'Adventure sports', 'Solang Valley', 'Rohtang Pass', 'Ancient temples'],
            'best_months': ['March', 'April', 'May', 'September', 'October', 'November'],
            'recommended_duration': 4,
            'is_active': True
        },
        {
            'name': 'Goa',
            'slug': 'goa',
            'description': 'India\'s beach paradise with golden sands, vibrant nightlife, Portuguese heritage, and delicious seafood.',
            'category': 'coast',
            'region': 'Goa',
            'main_image': '/assets/images/goa.jpg',
            'highlights': ['Pristine beaches', 'Water sports', 'Portuguese forts', 'Beach shacks', 'Nightlife'],
            'best_months': ['November', 'December', 'January', 'February', 'March'],
            'recommended_duration': 5,
            'is_active': True
        },
        {
            'name': 'Kerala Backwaters',
            'slug': 'kerala-backwaters',
            'description': 'Experience the tranquil backwaters of Kerala on traditional houseboats, surrounded by lush greenery and village life.',
            'category': 'backwaters',
            'region': 'Kerala',
            'main_image': '/assets/images/kerala.jpg',
            'highlights': ['Houseboat stays', 'Village tours', 'Ayurvedic treatments', 'Traditional cuisine', 'Wildlife sanctuaries'],
            'best_months': ['September', 'October', 'November', 'December', 'January', 'February'],
            'recommended_duration': 4,
            'is_active': True
        },
        {
            'name': 'Jaipur',
            'slug': 'jaipur',
            'description': 'The Pink City of India, rich in royal heritage with magnificent forts, palaces, and vibrant bazaars.',
            'category': 'heritage',
            'region': 'Rajasthan',
            'main_image': '/assets/images/jaipur.jpg',
            'highlights': ['Amber Fort', 'City Palace', 'Hawa Mahal', 'Traditional markets', 'Royal cuisine'],
            'best_months': ['October', 'November', 'December', 'January', 'February', 'March'],
            'recommended_duration': 3,
            'is_active': True
        },
        {
            'name': 'Rishikesh',
            'slug': 'rishikesh',
            'description': 'The Yoga Capital of the World, offering spiritual experiences, river rafting, and scenic mountain views.',
            'category': 'mountains',
            'region': 'Uttarakhand',
            'main_image': '/assets/images/rishikesh.jpg',
            'highlights': ['Yoga and meditation', 'River rafting', 'Ganga Aarti', 'Lakshman Jhula', 'Adventure sports'],
            'best_months': ['March', 'April', 'May', 'September', 'October', 'November'],
            'recommended_duration': 3,
            'is_active': True
        },
        {
            'name': 'Udaipur',
            'slug': 'udaipur',
            'description': 'The City of Lakes, known for romantic palaces, serene lake views, and royal hospitality.',
            'category': 'heritage',
            'region': 'Rajasthan',
            'main_image': '/assets/images/udaipur.jpg',
            'highlights': ['Lake Palace', 'City Palace', 'Boat rides', 'Sunset views', 'Traditional crafts'],
            'best_months': ['October', 'November', 'December', 'January', 'February', 'March'],
            'recommended_duration': 3,
            'is_active': True
        },
        {
            'name': 'Andaman Islands',
            'slug': 'andaman-islands',
            'description': 'Tropical paradise with crystal-clear waters, pristine beaches, coral reefs, and underwater adventures.',
            'category': 'coast',
            'region': 'Andaman and Nicobar Islands',
            'main_image': '/assets/images/andaman.jpg',
            'highlights': ['Scuba diving', 'White sand beaches', 'Coral reefs', 'Island hopping', 'Water sports'],
            'best_months': ['October', 'November', 'December', 'January', 'February', 'March', 'April', 'May'],
            'recommended_duration': 6,
            'is_active': True
        },
        {
            'name': 'Coorg',
            'slug': 'coorg',
            'description': 'Scotland of India, featuring lush coffee plantations, misty hills, and cascading waterfalls.',
            'category': 'mountains',
            'region': 'Karnataka',
            'main_image': '/assets/images/coorg.jpg',
            'highlights': ['Coffee plantations', 'Waterfalls', 'Wildlife sanctuaries', 'Trekking', 'Coorg cuisine'],
            'best_months': ['October', 'November', 'December', 'January', 'February', 'March'],
            'recommended_duration': 3,
            'is_active': True
        }
    ]
    
    print("Seeding destinations...")
    for dest_data in destinations:
        dest = Destination(**dest_data)
        db.session.add(dest)
    
    db.session.commit()
    print(f"✓ Created {len(destinations)} destinations")

def seed_packages():
    """Seed travel packages"""
    # Get destinations
    manali = Destination.query.filter_by(slug='manali').first()
    goa = Destination.query.filter_by(slug='goa').first()
    kerala = Destination.query.filter_by(slug='kerala-backwaters').first()
    jaipur = Destination.query.filter_by(slug='jaipur').first()
    
    packages = []
    
    if manali:
        # Manali Adventure Package
        pkg = Package(
            destination_id=manali.id,
            name='Manali Mountain Adventure',
            slug='manali-mountain-adventure',
            description='Experience the thrill of the Himalayas with adventure activities, scenic views, and mountain culture.',
            duration_days=5,
            duration_nights=4,
            base_price=18500,
            inclusions=['4 nights accommodation', 'Daily breakfast', 'Solang Valley visit', 'Local sightseeing', 'All transfers'],
            exclusions=['Lunch and dinner', 'Adventure activity costs', 'Personal expenses', 'Travel insurance'],
            accommodation_type='3-star hotels',
            highlights=['Rohtang Pass excursion', 'Solang Valley activities', 'Hidimba Temple visit', 'Mall Road shopping'],
            main_image='/assets/images/packages/manali-adventure.jpg',
            is_active=True,
            is_featured=True,
            display_order=1
        )
        packages.append(pkg)
        
        # Manali itinerary
        itinerary = [
            {
                'day_number': 1,
                'title': 'Arrival in Manali',
                'description': 'Arrive in Manali, check into your hotel. Evening at leisure to explore Mall Road and local markets.',
                'activities': ['Hotel check-in', 'Mall Road walk', 'Local market exploration'],
                'meals': ['Dinner'],
                'accommodation': 'Hotel in Manali'
            },
            {
                'day_number': 2,
                'title': 'Solang Valley Adventure',
                'description': 'Full day excursion to Solang Valley. Enjoy adventure activities like paragliding, zorbing, and cable car rides.',
                'activities': ['Solang Valley visit', 'Adventure activities', 'Cable car ride'],
                'meals': ['Breakfast'],
                'accommodation': 'Hotel in Manali'
            },
            {
                'day_number': 3,
                'title': 'Rohtang Pass Excursion',
                'description': 'Visit the spectacular Rohtang Pass (subject to permit availability). Experience snow-clad mountains and breathtaking views.',
                'activities': ['Rohtang Pass visit', 'Snow activities', 'Photography'],
                'meals': ['Breakfast'],
                'accommodation': 'Hotel in Manali'
            },
            {
                'day_number': 4,
                'title': 'Local Sightseeing',
                'description': 'Visit Hidimba Temple, Manu Temple, Vashisht Hot Springs, and Buddhist monasteries.',
                'activities': ['Temple visits', 'Hot springs', 'Monastery tour'],
                'meals': ['Breakfast'],
                'accommodation': 'Hotel in Manali'
            },
            {
                'day_number': 5,
                'title': 'Departure',
                'description': 'Check out from hotel. Departure with beautiful memories of the mountains.',
                'activities': ['Hotel check-out', 'Departure transfers'],
                'meals': ['Breakfast'],
                'accommodation': None
            }
        ]
    
    if goa:
        # Goa Beach Package
        pkg = Package(
            destination_id=goa.id,
            name='Goa Beach Paradise',
            slug='goa-beach-paradise',
            description='Relax on pristine beaches, explore Portuguese heritage, and enjoy Goa\'s vibrant nightlife.',
            duration_days=5,
            duration_nights=4,
            base_price=16500,
            inclusions=['4 nights accommodation', 'Daily breakfast', 'North and South Goa tours', 'All transfers'],
            exclusions=['Lunch and dinner', 'Water sports', 'Personal expenses', 'Entry fees'],
            accommodation_type='Beach resort',
            highlights=['Beach hopping', 'Water sports', 'Fort visits', 'Sunset cruises'],
            main_image='/assets/images/packages/goa-beach.jpg',
            is_active=True,
            is_featured=True,
            display_order=2
        )
        packages.append(pkg)
    
    if kerala:
        # Kerala Backwaters Package
        pkg = Package(
            destination_id=kerala.id,
            name='Kerala Backwaters Serenity',
            slug='kerala-backwaters-serenity',
            description='Cruise through tranquil backwaters on traditional houseboats, experiencing Kerala\'s natural beauty.',
            duration_days=4,
            duration_nights=3,
            base_price=21500,
            inclusions=['2 nights hotel', '1 night houseboat', 'All meals on houseboat', 'Backwater cruise', 'Transfers'],
            exclusions=['Meals at hotel', 'Personal expenses', 'Additional activities'],
            accommodation_type='Hotel + Houseboat',
            highlights=['Houseboat cruise', 'Village tours', 'Kathakali performance', 'Ayurvedic massage'],
            main_image='/assets/images/packages/kerala-backwaters.jpg',
            is_active=True,
            is_featured=True,
            display_order=3
        )
        packages.append(pkg)
    
    if jaipur:
        # Jaipur Heritage Package
        pkg = Package(
            destination_id=jaipur.id,
            name='Royal Jaipur Heritage',
            slug='royal-jaipur-heritage',
            description='Explore the Pink City\'s magnificent forts, palaces, and experience royal Rajasthani culture.',
            duration_days=4,
            duration_nights=3,
            base_price=14500,
            inclusions=['3 nights accommodation', 'Daily breakfast', 'All sightseeing', 'Elephant ride at Amber Fort', 'Transfers'],
            exclusions=['Lunch and dinner', 'Monument entry fees', 'Personal expenses'],
            accommodation_type='Heritage hotel',
            highlights=['Amber Fort', 'City Palace', 'Hawa Mahal', 'Jantar Mantar', 'Local bazaars'],
            main_image='/assets/images/packages/jaipur-heritage.jpg',
            is_active=True,
            display_order=4
        )
        packages.append(pkg)
    
    print("Seeding packages...")
    for pkg in packages:
        db.session.add(pkg)
        db.session.flush()
        
        # Add itinerary for Manali package
        if pkg.slug == 'manali-mountain-adventure':
            for day_data in itinerary:
                day = PackageItinerary(package_id=pkg.id, **day_data)
                db.session.add(day)
    
    db.session.commit()
    print(f"✓ Created {len(packages)} packages")

def seed_admin():
    """Create default admin user"""
    admin = Admin.query.filter_by(username='admin').first()
    
    if not admin:
        print("Creating default admin user...")
        admin = Admin(
            username='admin',
            email='admin@marigoldroutes.example',
            full_name='System Administrator',
            is_superadmin=True,
            is_active=True
        )
        admin.set_password('admin123')  # Change this password!
        db.session.add(admin)
        db.session.commit()
        print("✓ Created admin user (username: admin, password: admin123)")
        print("⚠️  IMPORTANT: Change the admin password immediately!")
    else:
        print("✓ Admin user already exists")

def main():
    """Main seed function"""
    print("\n" + "="*50)
    print("Marigold Routes - Database Seeding")
    print("="*50 + "\n")
    
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("✓ Database tables ready\n")
        
        # Seed data
        try:
            seed_destinations()
            print()
            seed_packages()
            print()
            seed_admin()
            print()
            print("="*50)
            print("✓ Database seeding completed successfully!")
            print("="*50)
            print("\nYou can now:")
            print("1. Start the backend server: python run.py")
            print("2. Access the website at http://localhost:3000")
            print("3. Login to admin at http://localhost:3000/admin.html")
            print("   Username: admin")
            print("   Password: admin123 (CHANGE THIS!)")
            print()
        except Exception as e:
            print(f"\n❌ Error during seeding: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()
