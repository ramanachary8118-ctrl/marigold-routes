# Marigold Routes - Travel Booking Platform

A complete full-stack travel booking website featuring guided trips across India. This platform includes a responsive frontend, Flask backend, PostgreSQL database, Razorpay payment integration, and email notifications.

## 🌟 Features

### Customer Features
- Browse 8 curated destinations across India
- View detailed travel packages with day-by-day itineraries
- Real-time price calculation with transparent breakdown
- Secure booking system with unique reference numbers
- Multiple hotel categories (Standard, Superior, Luxury)
- Optional extras (airport pickup, travel insurance, photographer)
- Booking lookup and management
- Guest booking access (no forced registration)
- Contact form for enquiries

### Admin Features
- Secure admin dashboard
- Booking management and tracking
- Destination and package management
- Contact enquiry management
- Revenue and booking reports
- Audit logging for important actions

### Technical Features
- Server-side pricing engine (never trust frontend prices)
- Razorpay payment gateway integration
- Email notifications via Resend
- PostgreSQL database with proper relationships
- RESTful API architecture
- Security best practices (CSRF protection, input validation, secure sessions)
- Responsive mobile-first design
- Comprehensive error handling

## 📋 Prerequisites

- **Python 3.9+**
- **PostgreSQL 12+** (or Supabase account)
- **Node.js** (optional, for frontend development tools)
- **Git**

## 🚀 Quick Start (Windows)

### 1. Clone the Repository

```powershell
git clone <repository-url>
cd "MARIGOLD ROUTES"
```

### 2. Set Up Python Virtual Environment

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Python Dependencies

```powershell
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### 4. Set Up Database

#### Option A: Local PostgreSQL

1. Install PostgreSQL from https://www.postgresql.org/download/windows/
2. Create a database:

```powershell
# Open psql command line
psql -U postgres

# In psql:
CREATE DATABASE marigold_routes;
CREATE USER marigold_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE marigold_routes TO marigold_user;
\q
```

#### Option B: Supabase (Recommended for Production)

1. Create account at https://supabase.com
2. Create a new project
3. Go to Project Settings → Database
4. Copy the connection string

### 5. Configure Environment Variables

```powershell
# Copy the example environment file
copy .env.example .env

# Edit .env file with your settings
notepad .env
```

**Required Configuration:**

```env
DATABASE_URL=postgresql://username:password@localhost:5432/marigold_routes
SECRET_KEY=your-secret-key-here
RAZORPAY_KEY_ID=rzp_test_XXXXXXXXXX
RAZORPAY_KEY_SECRET=your_key_secret
RESEND_API_KEY=re_XXXXXXXXXX
```

### 6. Initialize Database

```powershell
# Run migrations (from backend directory)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Create Admin User

```powershell
# Run Python interactive shell
python

# In Python shell:
from app import create_app, db
from app.models import Admin

app = create_app()
with app.app_context():
    admin = Admin(
        username='admin',
        email='admin@marigoldroutes.example',
        full_name='Administrator',
        is_superadmin=True
    )
    admin.set_password('admin123')  # Change this password!
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully!")

exit()
```

### 8. Seed Sample Data (Optional)

```powershell
# Run the seed script
python database/seed/seed_data.py
```

### 9. Start the Backend Server

```powershell
# Make sure you're in the backend directory with venv activated
python run.py
```

The backend will start at `http://localhost:5000`

### 10. Serve the Frontend

```powershell
# Open a new PowerShell window
cd frontend

# Option 1: Use Python's built-in server
python -m http.server 3000

# Option 2: Use Node.js http-server (if installed)
# npm install -g http-server
# http-server -p 3000
```

The frontend will be available at `http://localhost:3000`

### 11. Access the Application

- **Website**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3000/admin.html
- **API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123` (change this immediately!)

## 🔧 Configuration

### Razorpay Setup (Payment Gateway)

1. Create account at https://razorpay.com
2. Go to Settings → API Keys
3. Generate Test Keys (for development)
4. Add keys to `.env`:
   ```env
   RAZORPAY_KEY_ID=rzp_test_XXXXXXXXXX
   RAZORPAY_KEY_SECRET=your_secret_key
   ```
5. For webhooks, set up: `https://your-backend-url.com/api/payments/webhook`

### Resend Setup (Email Notifications)

1. Create account at https://resend.com
2. Generate API key
3. Verify your sending domain (or use sandbox for testing)
4. Add to `.env`:
   ```env
   RESEND_API_KEY=re_XXXXXXXXXX
   SENDER_EMAIL=noreply@yourdomain.com
   ```

## 📚 API Documentation

### Endpoints

#### Destinations
- `GET /api/destinations` - List all destinations
- `GET /api/destinations/:id` - Get destination details

#### Packages
- `GET /api/packages` - List all packages
- `GET /api/packages/:id` - Get package details

#### Bookings
- `POST /api/bookings` - Create new booking
- `POST /api/bookings/quote` - Get price quote
- `GET /api/bookings/:reference` - Get booking by reference
- `POST /api/bookings/lookup` - Look up booking (reference + email)
- `POST /api/bookings/:id/cancel` - Cancel booking

#### Payments
- `POST /api/payments/create-order` - Create Razorpay order
- `POST /api/payments/verify` - Verify payment
- `POST /api/payments/webhook` - Payment webhook

#### Contact
- `POST /api/contact` - Submit contact enquiry

#### Admin (Protected)
- `POST /api/admin/login` - Admin login
- `GET /api/admin/dashboard` - Dashboard statistics
- `GET /api/admin/bookings` - List all bookings
- `GET /api/admin/enquiries` - List enquiries

## 🧪 Testing

```powershell
# Run tests
cd backend
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_booking_service.py
```

## 🚢 Deployment

### Frontend Deployment (Netlify)

1. Create account at https://netlify.com
2. Connect your Git repository
3. Build settings:
   - Base directory: `frontend`
   - Publish directory: `frontend`
4. Environment variables:
   - Set `BACKEND_URL` to your backend URL
5. Deploy!

### Backend Deployment (Render / Railway / Heroku)

#### Using Render:

1. Create account at https://render.com
2. Create new Web Service
3. Connect repository
4. Settings:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && gunicorn run:app`
5. Add environment variables
6. Deploy!

#### Using Railway:

1. Create account at https://railway.app
2. Create new project from GitHub
3. Add PostgreSQL database
4. Configure environment variables
5. Deploy automatically on git push

### Database Deployment (Supabase)

1. Create Supabase project at https://supabase.com
2. Get connection string from Project Settings → Database
3. Update `DATABASE_URL` in production environment
4. Run migrations:
   ```powershell
   flask db upgrade
   ```

## 🔒 Security Checklist

Before going to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Change default admin password
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use HTTPS for frontend and backend
- [ ] Verify CORS origins are correctly configured
- [ ] Enable Razorpay webhook signature verification
- [ ] Set up rate limiting
- [ ] Configure proper database backups
- [ ] Review and test cancellation policy
- [ ] Test payment flows thoroughly
- [ ] Enable logging and monitoring
- [ ] Review privacy policy and terms

## 📝 Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Flask secret key | Yes | Random string |
| `JWT_SECRET_KEY` | JWT token secret | Yes | Random string |
| `RAZORPAY_KEY_ID` | Razorpay public key | Yes | `rzp_test_XXXXX` |
| `RAZORPAY_KEY_SECRET` | Razorpay secret key | Yes | Secret string |
| `RESEND_API_KEY` | Resend email API key | Yes | `re_XXXXX` |
| `FRONTEND_URL` | Frontend URL | Yes | `http://localhost:3000` |
| `BACKEND_URL` | Backend URL | Yes | `http://localhost:5000` |

## 🐛 Troubleshooting

### Database Connection Error

```
Could not connect to database
```

**Solution**: Verify PostgreSQL is running and credentials are correct in `.env`

### Import Error

```
ModuleNotFoundError: No module named 'flask'
```

**Solution**: Activate virtual environment and install requirements:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Port Already in Use

```
Address already in use
```

**Solution**: Kill the process using the port or change the port:
```powershell
# Find process
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### CORS Error

```
CORS policy: No 'Access-Control-Allow-Origin' header
```

**Solution**: Verify `FRONTEND_URL` in backend `.env` matches your actual frontend URL

## 📖 Project Structure

```
marigold-routes/
├── frontend/                  # Frontend HTML/CSS/JS
│   ├── index.html
│   ├── destinations.html
│   ├── packages.html
│   ├── booking.html
│   ├── my-bookings.html
│   ├── admin.html
│   └── assets/
│       ├── css/
│       └── js/
├── backend/                   # Flask backend
│   ├── app/
│   │   ├── __init__.py       # App factory
│   │   ├── config.py         # Configuration
│   │   ├── models/           # Database models
│   │   ├── routes/           # API endpoints
│   │   ├── services/         # Business logic
│   │   └── utils/            # Helper functions
│   ├── migrations/           # Database migrations
│   ├── tests/                # Test files
│   ├── requirements.txt      # Python dependencies
│   └── run.py               # Application entry point
├── database/
│   ├── schema.sql           # Database schema
│   └── seed/                # Seed data scripts
├── docs/                     # Documentation
├── .env.example             # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🤝 Contributing

This is a sample project for demonstration purposes.

## 📄 License

This is a sample project. All destinations, packages, prices, and contact information are provided as examples for illustrative purposes only.

## 📞 Support

For issues or questions about this sample project, please refer to the documentation in the `docs/` directory.

## ⚠️ Important Notes

1. **This is a demonstration project** - Not for actual commercial use without proper legal review
2. **Placeholder Content** - All destinations, prices, and policies are examples
3. **Test Mode Only** - Use Razorpay test keys only; never process real payments without proper business setup
4. **Legal Compliance** - Create actual privacy policy, terms, and cancellation policy with legal counsel
5. **Security** - Review and enhance security measures before any production use

## 🎯 Next Steps

After installation:

1. Review and customize business policies
2. Add real destination and package data
3. Configure actual payment gateway account
4. Set up email templates
5. Add actual company information
6. Test all workflows thoroughly
7. Set up monitoring and logging
8. Create backup strategy
9. Plan for scalability

---

**Built with ❤️ as a full-stack travel booking platform demonstration**
