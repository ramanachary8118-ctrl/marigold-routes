# Marigold Routes - Quick Start Guide

Get up and running in 15 minutes!

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.9 or higher
- [ ] PostgreSQL 12+ (or Supabase account)
- [ ] Git
- [ ] Code editor (VS Code recommended)

## Step 1: Clone and Setup (2 minutes)

```powershell
# Clone the repository (or navigate to your existing folder)
cd "C:\Users\Ramana chary\OneDrive\Desktop\MARIGOLD ROUTES"

# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get an execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Database Setup (5 minutes)

### Option A: Local PostgreSQL

```powershell
# Install PostgreSQL from https://www.postgresql.org/download/windows/

# Open psql
psql -U postgres

# Create database
CREATE DATABASE marigold_routes;
CREATE USER marigold_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE marigold_routes TO marigold_user;
\q
```

### Option B: Supabase (Recommended)

1. Go to https://supabase.com
2. Create new project
3. Copy connection string from Settings → Database
4. Format: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`

## Step 3: Configure Environment (2 minutes)

```powershell
# Copy environment template
copy .env.example .env

# Edit .env file
notepad .env
```

**Minimal configuration to get started:**
```env
DATABASE_URL=postgresql://marigold_user:your_password@localhost:5432/marigold_routes
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:5000
```

## Step 4: Initialize Database (3 minutes)

```powershell
# Run migrations (from backend directory)
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed sample data
cd ..
python database/seed/seed_data.py
```

You should see:
```
✓ Database tables ready
✓ Created 8 destinations
✓ Created 4 packages
✓ Created admin user (username: admin, password: admin123)
✓ Database seeding completed successfully!
```

## Step 5: Start the Backend (1 minute)

```powershell
# Make sure you're in backend directory with venv activated
cd backend
python run.py
```

You should see:
```
╔═══════════════════════════════════════════════════╗
║         Marigold Routes Backend Server            ║
╠═══════════════════════════════════════════════════╣
║  Running on: http://0.0.0.0:5000                 ║
║  Debug mode: True                                 ║
║  Environment: development                         ║
╚═══════════════════════════════════════════════════╝
```

## Step 6: Test the API (1 minute)

Open a new PowerShell window and test:

```powershell
# Health check
curl http://localhost:5000/api/health

# Get destinations
curl http://localhost:5000/api/destinations

# Get packages
curl http://localhost:5000/api/packages
```

Or open in browser:
- http://localhost:5000/api/health
- http://localhost:5000/api/destinations
- http://localhost:5000/api/packages

## Step 7: Start the Frontend (1 minute)

```powershell
# Open a NEW PowerShell window
cd "C:\Users\Ramana chary\OneDrive\Desktop\MARIGOLD ROUTES\frontend"

# Start simple HTTP server
python -m http.server 3000
```

## Step 8: Access the Application

Open your browser and visit:

- **Website:** http://localhost:3000
- **Admin Dashboard:** http://localhost:3000/admin.html
  - Username: `admin`
  - Password: `admin123` ⚠️ Change this immediately!

## What Works Right Now

✅ **Backend APIs:**
- Health check
- Get destinations
- Get packages
- Create bookings (via API)
- Admin login
- Dashboard statistics

✅ **Frontend Pages:**
- All HTML pages load
- Responsive design works
- Forms are structured
- Admin dashboard displays

⚠️ **What Doesn't Work Yet:**
- Frontend-backend connection (needs JavaScript)
- Actual booking flow (needs booking.js)
- Payment processing (needs Razorpay keys)
- Email notifications (needs Resend key)

## Quick Test Checklist

- [ ] Backend starts without errors
- [ ] Health check returns "ok"
- [ ] Can see destinations in API response
- [ ] Can see packages in API response
- [ ] Frontend pages load
- [ ] Can login to admin dashboard
- [ ] Admin dashboard shows statistics

## Common Issues & Fixes

### Issue: "ModuleNotFoundError"
**Fix:** Activate virtual environment and reinstall:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "Database connection error"
**Fix:** Check your DATABASE_URL in `.env` and ensure PostgreSQL is running

### Issue: "Port already in use"
**Fix:** Kill the process:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue: "Flask command not found"
**Fix:** Ensure virtual environment is activated

## Next Steps

Now that you're running:

1. **Test the APIs** using Postman or curl
2. **Explore the database** using psql or Supabase dashboard
3. **Read** `docs/IMPLEMENTATION_STATUS.md` to understand what's complete
4. **Start building** the JavaScript files to connect frontend to backend

## Need Help?

1. Check `README.md` for detailed documentation
2. Check `docs/IMPLEMENTATION_STATUS.md` for feature status
3. Check the code comments for implementation notes
4. Review the API endpoints in route files

## Development Workflow

```
Terminal 1: Backend Server
cd backend
.\venv\Scripts\Activate.ps1
python run.py

Terminal 2: Frontend Server
cd frontend
python -m http.server 3000

Terminal 3: Database/Commands
cd backend
.\venv\Scripts\Activate.ps1
# Run flask commands, migrations, etc.
```

---

**Congratulations! Your Marigold Routes development environment is ready! 🎉**
