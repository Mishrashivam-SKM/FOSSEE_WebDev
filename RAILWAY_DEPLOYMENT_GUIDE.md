# Railway Deployment - Quick Guide

## Fixed Issues

✅ Added root `requirements.txt` pointing to backend requirements
✅ Added root `Procfile` for process management
✅ Added `build.sh` for static file collection
✅ Configured `railway.json` with proper build command
✅ Updated deployment documentation

## Deployment Steps

### 1. Create Railway Project

1. Go to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository: `Mishrashivam-SKM/FOSSEE_WebDev`

### 2. Configure Environment Variables

In Railway dashboard, go to **Variables** and add:

```bash
# Required Variables
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=config.settings.production
DEBUG=False
PYTHONPATH=/app/backend

# Will be auto-filled after first deploy
DJANGO_ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

# Optional - Railway sets this automatically
PORT=8000
```

### 3. Generate Secret Key

Run this locally to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as `DJANGO_SECRET_KEY`.

### 4. Deploy

Railway will automatically:
1. Detect Python project
2. Install dependencies from `requirements.txt`
3. Run `build.sh` to collect static files
4. Execute `Procfile` to run migrations and start gunicorn
5. Assign a public URL

### 5. Update CORS Settings

After deployment, Railway will give you a URL like:
`https://your-app-name.up.railway.app`

Update the `DJANGO_ALLOWED_HOSTS` variable:
```
DJANGO_ALLOWED_HOSTS=your-app-name.up.railway.app
```

### 6. Verify Deployment

Test your API:
```bash
curl https://your-app-name.up.railway.app/api/
```

You should see a JSON response.

## Project Structure for Railway

```
FOSSEE/
├── requirements.txt      # Points to backend/requirements.txt
├── runtime.txt          # Python version (3.12.0)
├── Procfile            # Process: migrate + gunicorn
├── build.sh            # Build: collectstatic
├── railway.json        # Railway configuration
└── backend/
    ├── requirements.txt # Actual dependencies
    ├── manage.py
    └── config/
        └── settings/
            └── production.py  # Production settings
```

## How It Works

1. **Build Phase** (`build.sh`):
   - Installs dependencies
   - Collects static files with WhiteNoise

2. **Deploy Phase** (`Procfile`):
   - Changes to backend directory
   - Runs database migrations
   - Starts gunicorn server on Railway's PORT

3. **Runtime**:
   - WhiteNoise serves static files
   - Gunicorn handles requests
   - SQLite database persists in Railway volume

## Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `DJANGO_SECRET_KEY` | Django security key | `django-insecure-abc123...` |
| `DJANGO_SETTINGS_MODULE` | Settings file to use | `config.settings.production` |
| `DEBUG` | Debug mode (always False) | `False` |
| `DJANGO_ALLOWED_HOSTS` | Allowed domains | `app.up.railway.app` |
| `CORS_ALLOWED_ORIGINS` | Frontend URLs | `https://app.vercel.app` |
| `PYTHONPATH` | Python module path | `/app/backend` |
| `PORT` | Server port (auto-set) | `8000` |

## Troubleshooting

### Build Fails

**Error**: `pip: command not found`
- **Solution**: Already fixed! The root `requirements.txt` and `build.sh` handle this.

**Error**: `No module named 'config'`
- **Solution**: Add `PYTHONPATH=/app/backend` to environment variables.

### Deploy Fails

**Error**: `ModuleNotFoundError`
- **Solution**: Ensure `PYTHONPATH=/app/backend` is set.

**Error**: `DisallowedHost`
- **Solution**: Update `DJANGO_ALLOWED_HOSTS` with your Railway domain.

### Runtime Errors

**Error**: CORS errors from frontend
- **Solution**: Add your frontend URL to `CORS_ALLOWED_ORIGINS`.

**Error**: Static files not loading
- **Solution**: WhiteNoise is configured. Check that `build.sh` ran successfully.

## Database

Railway provides persistent storage for SQLite. Your `db.sqlite3` file will persist across deployments.

For production at scale, consider migrating to PostgreSQL:
1. Add PostgreSQL plugin in Railway
2. Railway will set `DATABASE_URL` automatically
3. The app will use PostgreSQL instead of SQLite

## Monitoring

In Railway dashboard:
- **Logs**: View real-time application logs
- **Metrics**: Monitor CPU, memory, network usage
- **Deployments**: View deployment history

## Cost

- **Free Tier**: $5 credit/month (enough for hobby projects)
- **Hobby Plan**: $5/month for more resources
- **Pro Plan**: $20/month for production apps

## Next Steps

After backend is deployed:

1. **Deploy Frontend** to Vercel/Netlify
2. **Update Frontend** `.env` with Railway API URL
3. **Update Backend** `CORS_ALLOWED_ORIGINS` with frontend URL
4. **Test** complete flow: register → login → upload → visualize

## Support

If you encounter issues:
1. Check Railway logs in dashboard
2. Verify all environment variables are set
3. Ensure `PYTHONPATH=/app/backend` is configured
4. Review [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions

---

**Your backend is now ready to deploy on Railway!** 🚀
