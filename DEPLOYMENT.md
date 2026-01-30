# Deployment Guide

This guide covers deploying the Chemical Equipment Visualizer to production.

## Architecture

- **Backend**: Django REST API on Railway (SQLite database)
- **Frontend**: React SPA on Vercel or Netlify
- **Desktop**: Standalone PyQt5 application (connects to deployed backend)

## Backend Deployment (Railway)

### Prerequisites
- Railway account (https://railway.app)
- GitHub repository connected to Railway

### Steps

1. **Create New Project on Railway**
   - Go to Railway dashboard
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Environment Variables**
   
   Add these variables in Railway dashboard:
   
   ```
   DJANGO_SECRET_KEY=<generate-a-secure-random-key>
   DJANGO_SETTINGS_MODULE=config.settings.production
   DEBUG=False
   DJANGO_ALLOWED_HOSTS=<your-railway-domain>.railway.app
   CORS_ALLOWED_ORIGINS=https://<your-frontend-domain>.vercel.app,https://<your-frontend-domain>.netlify.app
   PORT=8000
   ```

3. **Generate Secret Key**
   
   Run locally to generate a secure key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

4. **Deploy**
   - Railway will automatically detect the `railway.json` configuration
   - It will install dependencies, run migrations, and start the server
   - Your API will be available at: `https://<your-app>.railway.app/api/`

5. **Verify Deployment**
   ```bash
   curl https://<your-app>.railway.app/api/
   ```

### Database Persistence

Railway provides persistent storage for SQLite. Your `db.sqlite3` file will persist across deployments.

For production at scale, consider migrating to PostgreSQL:
1. Add PostgreSQL plugin in Railway
2. Railway will automatically set `DATABASE_URL`
3. The app will use PostgreSQL instead of SQLite

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI** (optional)
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Vercel Dashboard**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Add environment variable:
     ```
     VITE_API_URL=https://<your-railway-app>.railway.app/api
     ```
   - Deploy

3. **Deploy via CLI**
   ```bash
   cd frontend
   vercel
   ```

### Option 2: Netlify

1. **Deploy via Netlify Dashboard**
   - Go to https://netlify.com
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub repository
   - Set base directory to `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Add environment variable:
     ```
     VITE_API_URL=https://<your-railway-app>.railway.app/api
     ```
   - Deploy

2. **Deploy via CLI**
   ```bash
   npm install -g netlify-cli
   cd frontend
   netlify deploy --prod
   ```

### Verify Frontend

Visit your deployed URL and test:
- User registration
- Login
- CSV upload
- Data visualization
- PDF download

## Desktop Application Configuration

Update the desktop app to use your deployed backend:

1. **Create `.env` file in `desktop/` directory**
   ```bash
   cp desktop/.env.example desktop/.env
   ```

2. **Edit `desktop/.env`**
   ```
   CEV_API_URL=https://<your-railway-app>.railway.app/api
   ```

3. **Test Connection**
   ```bash
   cd desktop
   python main.py
   ```

## Post-Deployment Checklist

- [ ] Backend API is accessible and returns responses
- [ ] Frontend loads and connects to backend
- [ ] User registration works
- [ ] Login/logout works
- [ ] CSV upload works
- [ ] Data visualization displays correctly
- [ ] PDF download works
- [ ] Desktop app connects to deployed backend
- [ ] CORS is configured correctly
- [ ] HTTPS is enabled (automatic on Railway/Vercel/Netlify)

## Monitoring & Maintenance

### Railway
- View logs in Railway dashboard
- Monitor resource usage
- Set up alerts for downtime

### Vercel/Netlify
- View deployment logs
- Monitor bandwidth usage
- Set up custom domain (optional)

## Troubleshooting

### CORS Errors
- Ensure `CORS_ALLOWED_ORIGINS` in Railway includes your frontend URL
- Check that URLs don't have trailing slashes

### 502 Bad Gateway
- Check Railway logs for errors
- Verify `PORT` environment variable is set
- Ensure gunicorn is starting correctly

### Static Files Not Loading
- Run `python manage.py collectstatic` (done automatically in Railway)
- Verify WhiteNoise is in MIDDLEWARE

### Database Errors
- Check Railway logs
- Verify migrations ran successfully
- For SQLite: ensure persistent storage is enabled

## Scaling Considerations

For production at scale:

1. **Database**: Migrate from SQLite to PostgreSQL
2. **Media Files**: Use S3 or similar for file uploads
3. **Caching**: Add Redis for session/cache storage
4. **CDN**: Use Cloudflare or similar for static assets
5. **Monitoring**: Add Sentry for error tracking

## Security Best Practices

- ✅ Never commit `.env` files
- ✅ Use strong `DJANGO_SECRET_KEY`
- ✅ Keep `DEBUG=False` in production
- ✅ Regularly update dependencies
- ✅ Use HTTPS only (enforced by platforms)
- ✅ Implement rate limiting for API endpoints
- ✅ Regular security audits

## Cost Estimates

- **Railway**: Free tier available, ~$5-10/month for hobby projects
- **Vercel**: Free tier available, generous limits
- **Netlify**: Free tier available, generous limits

Total: **$0-10/month** for small to medium usage
