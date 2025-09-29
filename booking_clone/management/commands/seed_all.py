# booking_clone/management/commands/seed_all.py
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from bookings.models import Booking
from hotels.models import Location, Hotel, Room, RoomType, Amenity
from reviews.models import Review
from users.models import User


class Command(BaseCommand):
    help = "Seed database with test data"

    def handle(self, *args, **options):
        self.stdout.write("🗑️  Clearing existing data...")

        # Clear existing data in correct order
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Room.objects.all().delete()
        Hotel.objects.all().delete()
        Location.objects.all().delete()
        RoomType.objects.all().delete()
        Amenity.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("👤 Creating users...")

        # Create users
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@booking.com",
            password="admin123",
            first_name="Admin",
            last_name="User",
            role="guest",
        )

        john = User.objects.create_user(
            username="john_owner",
            email="john@hotels.com",
            password="admin123",
            first_name="John",
            last_name="Smith",
            role="owner",
        )

        maria = User.objects.create_user(
            username="maria_owner",
            email="maria@hotels.com",
            password="admin123",
            first_name="Maria",
            last_name="Garcia",
            role="owner",
        )

        alex = User.objects.create_user(
            username="alex_owner",
            email="alex@hotels.com",
            password="admin123",
            first_name="Alex",
            last_name="Johnson",
            role="owner",
        )

        emma = User.objects.create_user(
            username="emma_guest",
            email="emma@email.com",
            password="admin123",
            first_name="Emma",
            last_name="Wilson",
            role="guest",
        )

        mike = User.objects.create_user(
            username="mike_guest",
            email="mike@email.com",
            password="admin123",
            first_name="Mike",
            last_name="Brown",
            role="guest",
        )

        self.stdout.write("📍 Creating locations...")

        # Create locations
        ny = Location.objects.create(country="USA", city="New York")
        paris = Location.objects.create(country="France", city="Paris")
        tokyo = Location.objects.create(country="Japan", city="Tokyo")
        london = Location.objects.create(country="UK", city="London")
        rome = Location.objects.create(country="Italy", city="Rome")
        barcelona = Location.objects.create(country="Spain", city="Barcelona")
        berlin = Location.objects.create(country="Germany", city="Berlin")
        dubai = Location.objects.create(country="UAE", city="Dubai")

        self.stdout.write("🛏️  Creating room types...")

        # Create room types
        standard = RoomType.objects.create(
            name="Standard Room",
            description="Comfortable room with essential amenities",
            max_guests=2,
            size=25.0,
            bed_count=1,
        )

        deluxe = RoomType.objects.create(
            name="Deluxe Room",
            description="Spacious room with premium amenities",
            max_guests=2,
            size=35.0,
            bed_count=1,
        )

        suite = RoomType.objects.create(
            name="Suite",
            description="Large suite with separate living area",
            max_guests=4,
            size=60.0,
            bed_count=2,
        )

        family = RoomType.objects.create(
            name="Family Room",
            description="Spacious room perfect for families",
            max_guests=4,
            size=45.0,
            bed_count=2,
        )

        penthouse = RoomType.objects.create(
            name="Penthouse",
            description="Luxury top-floor suite with panoramic views",
            max_guests=6,
            size=120.0,
            bed_count=3,
        )

        self.stdout.write("✨ Creating amenities...")

        # Create amenities
        wifi = Amenity.objects.create(
            name="Free WiFi", description="High-speed wireless internet access"
        )
        ac = Amenity.objects.create(
            name="Air Conditioning", description="Climate control in all rooms"
        )
        tv = Amenity.objects.create(
            name="TV", description="Flat-screen TV with cable channels"
        )
        minibar = Amenity.objects.create(
            name="Mini Bar", description="Stocked mini refrigerator"
        )
        safe = Amenity.objects.create(
            name="Safe", description="In-room safe for valuables"
        )
        coffee = Amenity.objects.create(
            name="Coffee Maker",
            description="In-room coffee and tea facilities",
        )
        balcony = Amenity.objects.create(
            name="Balcony", description="Private balcony with view"
        )
        bathtub = Amenity.objects.create(
            name="Bathtub", description="Full-size bathtub"
        )

        self.stdout.write("🏨 Creating hotels...")

        # Create hotels
        hotel1 = Hotel.objects.create(
            owner=john,
            name="Grand Plaza Hotel New York",
            description="Luxury hotel in the heart of Manhattan with stunning city views",
            location=ny,
            address="123 Fifth Avenue, Manhattan",
            rating=4.8,
        )

        hotel2 = Hotel.objects.create(
            owner=john,
            name="Eiffel Tower Suites",
            description="Elegant Parisian hotel with views of the Eiffel Tower",
            location=paris,
            address="45 Rue de la Tour, Paris",
            rating=4.9,
        )

        hotel3 = Hotel.objects.create(
            owner=maria,
            name="Tokyo Sky Hotel",
            description="Modern hotel in Shibuya with traditional Japanese hospitality",
            location=tokyo,
            address="2-1-1 Shibuya, Tokyo",
            rating=4.7,
        )

        hotel4 = Hotel.objects.create(
            owner=maria,
            name="Westminster Palace Inn",
            description="Historic hotel near Big Ben and Westminster Abbey",
            location=london,
            address="78 Parliament Street, London",
            rating=4.6,
        )

        hotel5 = Hotel.objects.create(
            owner=maria,
            name="Colosseum View Hotel",
            description="Charming hotel with views of the ancient Colosseum",
            location=rome,
            address="Via dei Fori Imperiali 15, Rome",
            rating=4.5,
        )

        hotel6 = Hotel.objects.create(
            owner=alex,
            name="Barcelona Beach Resort",
            description="Beachfront hotel with Mediterranean cuisine",
            location=barcelona,
            address="Passeig Marítim 89, Barcelona",
            rating=4.7,
        )

        hotel7 = Hotel.objects.create(
            owner=alex,
            name="Berlin Central Hotel",
            description="Contemporary hotel in the city center",
            location=berlin,
            address="Unter den Linden 50, Berlin",
            rating=4.4,
        )

        hotel8 = Hotel.objects.create(
            owner=alex,
            name="Dubai Luxury Towers",
            description="Ultra-luxury hotel with private beach access",
            location=dubai,
            address="Sheikh Zayed Road, Dubai",
            rating=4.9,
        )

        hotel9 = Hotel.objects.create(
            owner=john,
            name="Statue of Liberty Hotel",
            description="Waterfront hotel with harbor views",
            location=ny,
            address="456 Battery Park, New York",
            rating=4.3,
        )

        hotel10 = Hotel.objects.create(
            owner=maria,
            name="Louvre Museum Hotel",
            description="Boutique hotel steps from the Louvre",
            location=paris,
            address="12 Rue de Rivoli, Paris",
            rating=4.6,
        )

        self.stdout.write("🚪 Creating rooms...")

        # Create rooms for each hotel
        # Hotel 1 - Grand Plaza
        room1 = Room.objects.create(
            hotel=hotel1,
            number="101",
            room_type=standard,
            price=150.00,
            is_available=True,
            max_guests=2,
        )
        room1.amenities.set([wifi, ac, tv, coffee])

        room2 = Room.objects.create(
            hotel=hotel1,
            number="102",
            room_type=deluxe,
            price=220.00,
            is_available=True,
            max_guests=2,
        )
        room2.amenities.set([wifi, ac, tv, minibar, safe, coffee, balcony])

        room3 = Room.objects.create(
            hotel=hotel1,
            number="201",
            room_type=suite,
            price=450.00,
            is_available=True,
            max_guests=4,
        )
        room3.amenities.set(
            [wifi, ac, tv, minibar, safe, coffee, balcony, bathtub]
        )

        # Hotel 2 - Eiffel Tower
        room4 = Room.objects.create(
            hotel=hotel2,
            number="301",
            room_type=deluxe,
            price=280.00,
            is_available=True,
            max_guests=2,
        )
        room4.amenities.set([wifi, ac, tv, minibar, safe, coffee, balcony])

        room5 = Room.objects.create(
            hotel=hotel2,
            number="401",
            room_type=penthouse,
            price=850.00,
            is_available=True,
            max_guests=6,
        )
        room5.amenities.set(
            [wifi, ac, tv, minibar, safe, coffee, balcony, bathtub]
        )

        # Hotel 3 - Tokyo
        room6 = Room.objects.create(
            hotel=hotel3,
            number="205",
            room_type=standard,
            price=120.00,
            is_available=True,
            max_guests=2,
        )
        room6.amenities.set([wifi, ac, tv])

        room7 = Room.objects.create(
            hotel=hotel3,
            number="305",
            room_type=family,
            price=200.00,
            is_available=True,
            max_guests=4,
        )
        room7.amenities.set([wifi, ac, tv, coffee])

        # Hotel 4 - London
        room8 = Room.objects.create(
            hotel=hotel4,
            number="110",
            room_type=deluxe,
            price=190.00,
            is_available=True,
            max_guests=2,
        )
        room8.amenities.set([wifi, ac, tv, minibar, coffee])

        room9 = Room.objects.create(
            hotel=hotel4,
            number="210",
            room_type=suite,
            price=380.00,
            is_available=False,
            max_guests=4,
        )
        room9.amenities.set(
            [wifi, ac, tv, minibar, safe, coffee, balcony, bathtub]
        )

        # Hotel 5 - Rome
        room10 = Room.objects.create(
            hotel=hotel5,
            number="101",
            room_type=standard,
            price=140.00,
            is_available=True,
            max_guests=2,
        )
        room10.amenities.set([wifi, ac, tv])

        room11 = Room.objects.create(
            hotel=hotel5,
            number="202",
            room_type=deluxe,
            price=210.00,
            is_available=True,
            max_guests=2,
        )
        room11.amenities.set([wifi, ac, tv, minibar, safe, coffee, balcony])

        # Hotel 6 - Barcelona
        room12 = Room.objects.create(
            hotel=hotel6,
            number="505",
            room_type=suite,
            price=420.00,
            is_available=True,
            max_guests=4,
        )
        room12.amenities.set(
            [wifi, ac, tv, minibar, safe, coffee, balcony, bathtub]
        )

        room13 = Room.objects.create(
            hotel=hotel6,
            number="101",
            room_type=standard,
            price=130.00,
            is_available=True,
            max_guests=2,
        )
        room13.amenities.set([wifi, ac, tv])

        # Hotel 7 - Berlin
        room14 = Room.objects.create(
            hotel=hotel7,
            number="303",
            room_type=deluxe,
            price=180.00,
            is_available=True,
            max_guests=2,
        )
        room14.amenities.set([wifi, ac, tv, minibar, coffee])

        room15 = Room.objects.create(
            hotel=hotel7,
            number="404",
            room_type=family,
            price=250.00,
            is_available=True,
            max_guests=4,
        )
        room15.amenities.set([wifi, ac, tv, minibar, safe, coffee])

        # Hotel 8 - Dubai
        room16 = Room.objects.create(
            hotel=hotel8,
            number="1001",
            room_type=penthouse,
            price=1200.00,
            is_available=True,
            max_guests=6,
        )
        room16.amenities.set(
            [wifi, ac, tv, minibar, safe, coffee, balcony, bathtub]
        )

        room17 = Room.objects.create(
            hotel=hotel8,
            number="801",
            room_type=suite,
            price=650.00,
            is_available=True,
            max_guests=4,
        )
        room17.amenities.set(
            [wifi, ac, tv, minibar, safe, coffee, balcony, bathtub]
        )

        # Hotel 9 - NY Harbor
        room18 = Room.objects.create(
            hotel=hotel9,
            number="105",
            room_type=standard,
            price=110.00,
            is_available=True,
            max_guests=2,
        )
        room18.amenities.set([wifi, ac, tv])

        room19 = Room.objects.create(
            hotel=hotel9,
            number="205",
            room_type=deluxe,
            price=170.00,
            is_available=True,
            max_guests=2,
        )
        room19.amenities.set([wifi, ac, tv, minibar, coffee, balcony])

        # Hotel 10 - Louvre
        room20 = Room.objects.create(
            hotel=hotel10,
            number="201",
            room_type=deluxe,
            price=240.00,
            is_available=True,
            max_guests=2,
        )
        room20.amenities.set([wifi, ac, tv, minibar, safe, coffee])

        room21 = Room.objects.create(
            hotel=hotel10,
            number="301",
            room_type=suite,
            price=480.00,
            is_available=True,
            max_guests=4,
        )
        room21.amenities.set(
            [wifi, ac, tv, minibar, safe, coffee, balcony, bathtub]
        )

        self.stdout.write("📅 Creating bookings...")

        # Create bookings with created_at
        booking1 = Booking.objects.create(
            user=emma,
            room=room1,
            check_in=timezone.now().date() + timedelta(days=30),
            check_out=timezone.now().date() + timedelta(days=33),
        )
        # Manually set created_at to past date
        booking1.created_at = timezone.now() - timedelta(days=5)
        booking1.save()

        booking2 = Booking.objects.create(
            user=mike,
            room=room4,
            check_in=timezone.now().date() + timedelta(days=45),
            check_out=timezone.now().date() + timedelta(days=49),
        )
        booking2.created_at = timezone.now() - timedelta(days=3)
        booking2.save()

        booking3 = Booking.objects.create(
            user=emma,
            room=room12,
            check_in=timezone.now().date() + timedelta(days=90),
            check_out=timezone.now().date() + timedelta(days=97),
        )
        booking3.created_at = timezone.now() - timedelta(days=1)
        booking3.save()

        self.stdout.write("⭐ Creating reviews...")

        # Create reviews with created_at
        review1 = Review.objects.create(
            hotel=hotel1,
            user=emma,
            rating=5,
            comment="Amazing hotel! The room was spacious and the view was breathtaking. Staff was incredibly helpful.",
        )
        review1.created_at = timezone.now() - timedelta(days=10)
        review1.save()

        review2 = Review.objects.create(
            hotel=hotel2,
            user=mike,
            rating=5,
            comment="Perfect location near the Eiffel Tower. The breakfast was excellent and the room was very clean.",
        )
        review2.created_at = timezone.now() - timedelta(days=8)
        review2.save()

        review3 = Review.objects.create(
            hotel=hotel3,
            user=emma,
            rating=4,
            comment="Great experience overall. The hotel is modern and well-located. Would definitely stay again!",
        )
        review3.created_at = timezone.now() - timedelta(days=5)
        review3.save()

        # Success message
        self.stdout.write(
            self.style.SUCCESS("\n✅ Successfully seeded database!")
        )
        self.stdout.write("\n📊 Data created:")
        self.stdout.write(f"  • {User.objects.count()} Users")
        self.stdout.write(f"  • {Location.objects.count()} Locations")
        self.stdout.write(f"  • {Amenity.objects.count()} Amenities")
        self.stdout.write(f"  • {RoomType.objects.count()} Room Types")
        self.stdout.write(f"  • {Hotel.objects.count()} Hotels")
        self.stdout.write(f"  • {Room.objects.count()} Rooms")
        self.stdout.write(f"  • {Booking.objects.count()} Bookings")
        self.stdout.write(f"  • {Review.objects.count()} Reviews")

        self.stdout.write("\n🔑 Test credentials (all passwords: admin123):")
        self.stdout.write("  Admin:  admin / admin123")
        self.stdout.write("  Owner:  john_owner / admin123")
        self.stdout.write("  Owner:  maria_owner / admin123")
        self.stdout.write("  Owner:  alex_owner / admin123")
        self.stdout.write("  Guest:  emma_guest / admin123")
        self.stdout.write("  Guest:  mike_guest / admin123")
        self.stdout.write("\n🎉 You can now test the API!")
