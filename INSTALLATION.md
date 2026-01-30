# Installation Guide

Complete installation instructions for the Chemical Equipment Visualizer.

## System Requirements

### Backend
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment tool (venv, virtualenv, or conda)

### Frontend
- Node.js 18 or higher
- npm or yarn package manager

### Desktop
- Python 3.9 or higher
- PyQt5 dependencies (platform-specific)

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# Using venv (recommended)
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and set your configuration
# At minimum, generate a new DJANGO_SECRET_KEY
```

Generate a secure secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Start Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

### 3. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (default points to localhost:8000)
```

### 4. Start Development Server
```bash
# Using npm
npm run dev

# Or using yarn
yarn dev
```

The web app will be available at: `http://localhost:3000/`

## Desktop Application Setup

### 1. Navigate to Desktop Directory
```bash
cd desktop
```

### 2. Create Virtual Environment (or use backend's venv)
```bash
# Create new virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Platform-Specific Notes

#### macOS
PyQt5 should install without issues. If you encounter problems:
```bash
brew install pyqt5
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg
```

#### Windows
PyQt5 should install via pip without issues.

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env to point to your backend
# Default: http://localhost:8000/api
```

### 5. Run Desktop Application
```bash
python main.py
```

## Verification

### Test Backend
```bash
# Check API health
curl http://localhost:8000/api/

# Or visit in browser
open http://localhost:8000/api/
```

### Test Frontend
1. Open browser to `http://localhost:3000/`
2. Register a new user
3. Login
4. Upload sample CSV from `sample_data/sample_equipment_data.csv`
5. View dashboard and analytics

### Test Desktop
1. Run `python main.py` from desktop directory
2. Register or login
3. Upload CSV file
4. View visualizations

## Troubleshooting

### Backend Issues

**Port 8000 already in use**
```bash
# Find and kill process using port 8000
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Database errors**
```bash
# Delete database and recreate
rm db.sqlite3
python manage.py migrate
```

**Module not found errors**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use**
```bash
# Kill process on port 3000
# macOS/Linux:
lsof -ti:3000 | xargs kill -9

# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**npm install fails**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**CORS errors**
- Ensure backend is running
- Check that `VITE_API_URL` in `.env` matches backend URL
- Verify CORS settings in backend `settings/development.py`

### Desktop Issues

**PyQt5 import errors**
```bash
# Reinstall PyQt5
pip uninstall PyQt5
pip install PyQt5
```

**API connection errors**
- Ensure backend is running
- Check `CEV_API_URL` in `.env`
- Verify network connectivity

**qtawesome icons not showing**
```bash
# Install qtawesome
pip install qtawesome
```

## Development Workflow

### Typical Development Session

1. **Start Backend**
   ```bash
   cd backend
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Start Frontend** (in new terminal)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Start Desktop** (optional, in new terminal)
   ```bash
   cd desktop
   source venv/bin/activate
   python main.py
   ```

### Making Changes

- **Backend**: Changes auto-reload with Django dev server
- **Frontend**: Changes auto-reload with Vite HMR
- **Desktop**: Restart application to see changes

## Next Steps

- Read [README.md](./README.md) for project overview
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment
- Check `sample_data/` for example CSV files
- Explore API at `http://localhost:8000/api/`

## Getting Help

If you encounter issues:

1. Check this troubleshooting section
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify environment configuration
5. Check that all services are running

## Uninstallation

### Remove Virtual Environments
```bash
# Backend
rm -rf backend/venv

# Desktop
rm -rf desktop/venv
```

### Remove Node Modules
```bash
rm -rf frontend/node_modules
```

### Remove Database
```bash
rm backend/db.sqlite3
```

### Remove Environment Files
```bash
rm backend/.env
rm frontend/.env
rm desktop/.env
```
