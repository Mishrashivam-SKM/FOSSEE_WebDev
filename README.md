# Chemical Equipment Parameter Visualizer

A hybrid application for data visualization and analytics of chemical equipment parameters. This project provides both a **Web Application** (React.js) and a **Desktop Application** (PyQt5) that share a common **Django REST API** backend.

## 📁 Project Structure

```
FOSSEE/
├── backend/              # Django REST API backend
│   ├── config/          # Django settings and configuration
│   ├── apps/
│   │   ├── authentication/  # JWT authentication
│   │   └── equipment/       # Equipment & dataset management
│   ├── core/            # Shared utilities
│   └── manage.py
├── frontend/            # React.js web application
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── pages/       # Page components
│   │   ├── hooks/       # Custom React hooks
│   │   ├── services/    # API services
│   │   └── context/     # React context providers
│   └── package.json
├── desktop/             # PyQt5 desktop application
│   ├── ui/             # UI components (windows, dialogs, widgets)
│   ├── services/       # API client
│   ├── models/         # Data models
│   ├── charts/         # Matplotlib charts
│   ├── utils/          # Utilities
│   └── main.py
└── sample_data/         # Sample CSV files
```

## ✨ Features

- **CSV Upload**: Upload equipment data from CSV files
- **Data Visualization**: Interactive charts (bar charts, pie charts)
- **Parameter Analysis**: Statistical summaries (averages, ranges, distribution)
- **History Management**: Store and manage last 5 datasets
- **PDF Reports**: Download equipment analysis as PDF
- **Authentication**: User registration and JWT-based login

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Installation

See [INSTALLATION.md](./INSTALLATION.md) for detailed setup instructions.

**Quick Setup:**

```bash
# 1. Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver

# 2. Frontend (new terminal)
cd frontend
npm install
cp .env.example .env
npm run dev

# 3. Desktop (optional, new terminal)
cd desktop
pip install -r requirements.txt
cp .env.example .env
python main.py
```

The API will be at `http://localhost:8000/api/` and web app at `http://localhost:3000/`

## 📊 Sample Data

A sample CSV file is provided at `sample_data/sample_equipment_data.csv`. 

### Required CSV Format

| Column | Type | Description |
|--------|------|-------------|
| Equipment Name | String | Name of the equipment |
| Type | String | Equipment type (Pump, Reactor, etc.) |
| Flowrate | Number | Flow rate value |
| Pressure | Number | Pressure value |
| Temperature | Number | Temperature value |

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Datasets
- `GET /api/datasets/` - List all datasets
- `POST /api/datasets/upload/` - Upload CSV file
- `GET /api/datasets/{id}/` - Get dataset details
- `DELETE /api/datasets/{id}/` - Delete dataset
- `GET /api/datasets/{id}/analytics/` - Get analytics
- `GET /api/datasets/{id}/equipment/` - Get equipment list
- `GET /api/datasets/{id}/pdf/` - Download PDF report

## 🛠 Technologies

### Backend
- **Django 5.x** - Web framework
- **Django REST Framework** - API development
- **SimpleJWT** - JWT authentication
- **Pandas** - Data processing
- **ReportLab** - PDF generation
- **SQLite** - Database

### Web Frontend
- **React.js 18** - UI framework
- **Vite** - Build tool
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **React Router** - Navigation

### Desktop Application
- **PyQt5** - Desktop UI framework
- **Matplotlib** - Data visualization
- **Requests** - HTTP client
- **Pandas** - Data processing

## 📝 Configuration

### Backend
Edit `backend/config/settings/development.py` for development settings.

### Web Frontend
Edit `frontend/.env`:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Desktop App
Edit `desktop/.env`:
```
API_BASE_URL=http://localhost:8000/api
```

## 📖 Usage

1. **Start the backend server** first
2. **Register/Login** through either the web or desktop app
3. **Upload a CSV file** with equipment data
4. **View analytics** and charts on the dashboard
5. **Download PDF reports** for detailed analysis
6. **Manage history** - old datasets are automatically removed (keeps last 5)

## 🚀 Deployment

This application is deployment-ready for production environments.

### Quick Deploy

- **Backend**: Deploy to [Railway](https://railway.app) with one click
- **Frontend**: Deploy to [Vercel](https://vercel.com) or [Netlify](https://netlify.com)
- **Desktop**: Configure to use deployed backend API

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

### Deployment Files

- `railway.json` - Railway configuration for backend
- `backend/Procfile` - Process configuration for Railway
- `frontend/vercel.json` - Vercel configuration
- `frontend/netlify.toml` - Netlify configuration

## 📦 Project Structure Details

### Backend (`backend/`)
```
backend/
├── config/              # Django project configuration
│   ├── settings/       # Environment-specific settings
│   │   ├── base.py    # Shared settings
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI application
├── apps/
│   ├── authentication/ # JWT authentication
│   │   ├── views.py   # Login, register, logout
│   │   ├── serializers.py
│   │   └── urls.py
│   └── equipment/     # Equipment & dataset management
│       ├── models.py  # Dataset, Equipment models
│       ├── views.py   # API views
│       ├── serializers.py
│       ├── services/  # Business logic
│       │   ├── analytics.py    # Statistical analysis
│       │   ├── csv_parser.py   # CSV processing
│       │   └── pdf_generator.py # PDF reports
│       └── urls.py
├── core/              # Shared utilities
│   ├── exceptions.py  # Custom exceptions
│   └── pagination.py  # API pagination
└── manage.py
```

### Frontend (`frontend/src/`)
```
frontend/src/
├── components/
│   ├── charts/        # Chart.js components
│   └── common/        # Reusable UI components
│       ├── Layout.jsx # Main layout with sidebar
│       ├── Navbar.jsx
│       └── ...
├── pages/             # Page components
│   ├── Dashboard/     # Main dashboard
│   ├── Upload/        # CSV upload
│   ├── History/       # Dataset history
│   ├── Analysis/      # Detailed analysis
│   ├── Login/
│   └── Register/
├── hooks/             # Custom React hooks
│   ├── useAuth.js
│   ├── useEquipmentData.js
│   └── useFileUpload.js
├── services/          # API integration
│   ├── api.js         # Axios instance with interceptors
│   ├── authService.js
│   └── equipmentService.js
├── context/           # React Context
│   └── AuthContext.jsx
├── utils/             # Utilities
│   ├── constants.js
│   └── formatters.js
└── styles/
    └── global.css     # Global styles
```

### Desktop (`desktop/`)
```
desktop/
├── ui/
│   ├── main_window.py    # Main application window
│   ├── theme.py          # Theme constants
│   ├── components/       # Reusable UI components
│   └── widgets/          # Page widgets
│       ├── dashboard_widget.py
│       ├── upload_widget.py
│       ├── history_widget.py
│       ├── analysis_widget.py
│       ├── login_widget.py
│       └── register_widget.py
├── services/
│   ├── api_client.py     # HTTP client for backend
│   └── auth_manager.py   # Token management
├── utils/
│   └── helpers.py        # Formatting utilities
└── main.py               # Application entry point
```

## 🔒 Security

- JWT-based authentication with token refresh
- CORS protection
- CSRF protection
- XSS protection
- Secure password hashing (Django's PBKDF2)
- Environment-based configuration
- HTTPS enforced in production

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Quick contribution steps:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines on code style, testing, and pull requests.

## 📄 License

This project is developed for FOSSEE.

## 👥 Authors

FOSSEE Team

## 🙏 Acknowledgments

- FOSSEE for project requirements and support
- Django REST Framework for robust API development
- React and Vite for modern frontend development
- PyQt5 for cross-platform desktop application
