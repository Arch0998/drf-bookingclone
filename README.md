# 🏨 DRF Booking Clone

A
comprehensive
hotel
booking
system
built
with
Django
REST
Framework,
featuring
modern
authentication,
payment
processing,
and
full
API
documentation.
This
project
demonstrates
best
practices
in
Django
development
and
can
serve
as
a
foundation
for
real-world
booking
applications.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://django-rest-framework.org)
[![Docker](https://img.shields.io/badge/Docker-supported-blue.svg)](https://docker.com)

---

## 🚀 Features

### Core Functionality

-
*
*🔐
User
Management
**:
Registration,
JWT
authentication,
user
profiles
with
roles (
Guest/Owner)
-
*
*🏨
Hotel
Management
**:
Full
CRUD
operations
for
hotels
with
advanced
filtering
and
search
-
*
*🛏️
Room
Management
**:
Room
types,
amenities,
availability
tracking,
photo
uploads
-
*
*📅
Booking
System
**:
Availability
checks,
booking
statuses,
date
validation
-
*
*💳
Payment
Integration
**:
Stripe
payment
processing
with
secure
webhooks
-
*
*⭐
Review
System
**:
Ratings,
comments,
photo
uploads,
automatic
hotel
rating
calculation
-
*
*🌍
Location
Management
**:
Country
and
city-based
hotel
organization

### Technical Features

-
*
*📖
API
Documentation
**:
Complete
OpenAPI/Swagger
documentation
with
drf-spectacular
-
*
*🔒
Authentication
**:
JWT
tokens
with
refresh
functionality
-
*
*🧪
Testing
**:
Comprehensive
test
coverage
for
all
components
-
*
*🐳
Docker
Support
**:
Containerized
development
and
deployment
-
*
*👤
Admin
Interface
**:
Enhanced
Django
admin
with
search,
filters,
and
autocomplete
-
*
*🎨
Code
Quality
**:
Black
formatting,
structured
project
organization

---

## 🏗️ Architecture

```
drf-bookingclone/
├── 📁 booking_clone/         # Project configuration & settings
│   ├── settings/            # Environment-specific settings (dev/prod)
│   ├── urls.py             # Main URL configuration
│   └── management/         # Custom Django commands
├── 📁 users/               # User management & authentication
├── 📁 hotels/              # Hotels, rooms, locations, amenities
├── 📁 bookings/            # Booking logic & availability
├── 📁 payments/            # Stripe integration & payment processing
├── 📁 reviews/             # Hotel reviews & ratings
├── 🐳 docker-compose.yml   # Docker orchestration
├── 🐳 Dockerfile          # Container configuration
└── 📋 requirements.txt     # Python dependencies
```

---

## 🛠️ Technology Stack

-
*
*Backend
**:
Django
5.2.6,
Django
REST
Framework
3.16.1
-
*
*Database
**:
PostgreSQL
-
*
*Authentication
**:
JWT (
djangorestframework-simplejwt)
-
*
*Payments
**:
Stripe
API
-
*
*Documentation
**:
drf-spectacular (
OpenAPI
3.0)
-
*
*Image
Processing
**:
Pillow
-
*
*Containerization
**:
Docker &
Docker
Compose

---

## 🚀 Quick Start

### Prerequisites

-
Docker
and
Docker
Compose
-
Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd drf-bookingclone
```

### 2. Environment Configuration

Create
a
`.env`
file
in
the
project
root:

```env
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_SETTINGS_MODULE=booking_clone.settings.dev

# Database (PostgreSQL)
POSTGRES_DB=booking_db
POSTGRES_USER=booking_user
POSTGRES_PASSWORD=secure_password_123
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
```

### 3. Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

The
application
will
be
available
at:

-
*
*API
**: http://localhost:8000/
-
*
*Admin
Panel
**: http://localhost:8000/admin/
-
*
*API
Documentation
**: http://localhost:8000/api/docs/

### 4. Create Superuser

```bash
docker-compose exec app python manage.py createsuperuser
```

### 5. Load Sample Data (Optional)

```bash
# Create comprehensive test data for development/testing
docker-compose exec app python manage.py seed_all
```

*
*What
`seed_all`
command
creates:
**

-
*
*👤
Test
Users
**:
6
users
with
different
roles (
admin,
hotel
owners,
guests)
    -
    `admin` (
    superuser):
    admin@booking.com /
    admin123
    -
    `john_owner`,
    `maria_owner`,
    `alex_owner` (
    hotel
    owners)
    -
    `emma_guest`,
    `mike_guest` (
    regular
    guests)
-
*
*📍
Sample
Locations
**:
8
popular
cities (
New
York,
Paris,
Tokyo,
London,
Rome,
Barcelona,
Berlin,
Dubai)
-
*
*🛏️
Room
Types
**:
5
different
types (
Standard,
Deluxe,
Suite,
Family,
Penthouse)
-
*
*✨
Hotel
Amenities
**:
8
common
amenities (
WiFi,
AC,
TV,
Mini
Bar,
Safe,
Coffee
Maker,
Balcony,
Bathtub)
-
*
*🏨
Hotels
**:
10
hotels
distributed
across
locations
with
realistic
names
and
descriptions
-
*
*🚪
Hotel
Rooms
**:
Multiple
rooms
per
hotel
with
different
types,
prices,
and
amenity
combinations
-
*
*📅
Sample
Bookings
**:
Test
bookings
with
different
statuses
and
dates
-
*
*⭐
Hotel
Reviews
**:
Sample
reviews
with
ratings
and
comments

This
command
*
*clears
all
existing
data
**
first,
then
creates
a
complete
test
dataset
perfect
for
development,
testing,
and
demonstration
purposes.

---

## 📚 API Documentation

### Interactive Documentation

-
*
*Swagger
UI
**: http://localhost:8000/api/docs/
-
*
*ReDoc
**: http://localhost:8000/api/redoc/
-
*
*OpenAPI
Schema
**: http://localhost:8000/api/schema/

### Main Endpoints

#### 👤 User Management

```
POST   /users/register/           # User registration
POST   /users/token/              # Obtain JWT token
POST   /users/token/refresh/      # Refresh JWT token
POST   /users/token/verify/       # Verify JWT token
GET    /users/profile/            # Get current user profile
PUT    /users/profile/            # Update user profile
```

#### 🏨 Hotel Management

```
GET    /hotels/                   # List hotels (with filtering & search)
POST   /hotels/                   # Create hotel (owners only)
GET    /hotels/{id}/              # Hotel details
PUT    /hotels/{id}/              # Update hotel (owner only)
DELETE /hotels/{id}/              # Delete hotel (owner only)
GET    /hotels/my-hotels/         # List current owner's hotels
GET    /hotels/{id}/rooms/        # List hotel rooms
POST   /hotels/{id}/add-room/     # Add room to hotel (owner only)
```

#### 🌍 Reference Data

```
GET    /hotels/locations/         # List locations
GET    /hotels/room-types/        # List room types
GET    /hotels/amenities/         # List amenities
```

#### 🛏️ Room Management

```
GET    /rooms/                    # List all rooms
POST   /rooms/                    # Create room (owners only)
GET    /rooms/{id}/               # Room details
PUT    /rooms/{id}/               # Update room (owner only)
DELETE /rooms/{id}/               # Delete room (owner only)
```

#### 📅 Booking Management

```
GET    /bookings/                 # List user's bookings
POST   /bookings/                 # Create booking
GET    /bookings/{id}/            # Booking details
PUT    /bookings/{id}/            # Update booking
DELETE /bookings/{id}/            # Cancel booking
```

#### 💳 Payment Processing

```
GET    /payments/                 # List user's payments
POST   /payments/                 # Create payment session
GET    /payments/{id}/            # Payment details
POST   /payments/webhook/         # Stripe webhook endpoint
```

#### ⭐ Review System

```
GET    /reviews/                  # List reviews
POST   /reviews/                  # Create review
GET    /reviews/{id}/             # Review details
PUT    /reviews/{id}/             # Update review (author only)
DELETE /reviews/{id}/             # Delete review (author only)
```

### Filtering & Search

#### Hotels

-
*
*Filter
by
**:
`location__city`,
`location__country`,
`min_rating`,
`min_price`,
`max_price`
-
*
*Search
by
**:
`name`,
`description`,
`address`
-
*
*Order
by
**:
`rating`,
`name`

#### Rooms

-
*
*Filter
by
**:
`hotel`,
`room_type`,
`is_available`
-
*
*Order
by
**:
`price`

#### Bookings

-
*
*Filter
by
**:
`status`,
`check_in`,
`check_out`
-
*
*Order
by
**:
`created_at`,
`check_in`

---

## 🐳 Docker Configuration

### Services

-
*
*app
**:
Django
application
server
-
*
*db
**:
PostgreSQL
database
-
*
*volumes
**:
Persistent
data
storage

### Development Workflow

```bash
# Start services
docker-compose up

# View logs
docker-compose logs -f app

# Execute commands
docker-compose exec app python manage.py <command>

# Rebuild after changes
docker-compose up --build

# Stop services
docker-compose down
```

---

## 👨‍💼 Admin Interface

Access
at http://localhost:8000/admin/

### Features

-
*
*User
Management
**:
View/edit
users
with
role
filtering
-
*
*Hotel
Management
**:
Full
CRUD
with
search
and
filters
-
*
*Booking
Overview
**:
Status
tracking,
date
filters
-
*
*Payment
Monitoring
**:
Transaction
status,
amounts
-
*
*Review
Moderation
**:
Rating
overview,
photo
previews
-
*
*Reference
Data
**:
Locations,
room
types,
amenities

### Admin Enhancements

-
Search
functionality
across
all
models
-
Date
range
filters
for
bookings/payments
-
ForeignKey
autocomplete
for
better
UX
-
Image
previews
for
photos
-
Custom
list
displays
and
filters

---

## 🔒 Security Features

-
*
*JWT
Authentication
**:
Secure
token-based
auth
-
*
*Permission
Classes
**:
Role-based
access
control
-
*
*Input
Validation
**:
Comprehensive
serializer
validation
-
*
*SQL
Injection
Protection
**:
Django
ORM
usage
-
*
*CORS
Configuration
**:
Controlled
cross-origin
requests
-
*
*Environment
Variables
**:
Sensitive
data
protection
-
*
*Rate
Limiting
**:
API
abuse
prevention (
configurable)

---

## 🤝 Contributing

1.
Fork
the
repository
2.
Create
a
feature
branch (
`git checkout -b feature/amazing-feature`)
3.
Commit
your
changes (
`git commit -m 'Add amazing feature'`)
4.
Push
to
the
branch (
`git push origin feature/amazing-feature`)
5.
Open
a
Pull
Request

---

## 🙏 Acknowledgments

-
Django
REST
Framework
team
for
the
excellent
framework
-
Stripe
for
payment
processing
capabilities
-
drf-spectacular
for
API
documentation
-
The
Django
community
for
continuous
support

---
