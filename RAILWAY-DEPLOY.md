# Deploy Backend to Railway.app

## Quick Setup (5 minutes)

### Option 1: Deploy via GitHub (Recommended)

1. **Push backend to GitHub** (if not already):
   ```bash
   cd etf-backend
   git init
   git add .
   git commit -m "Prepare for Railway deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/etf-backend.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to https://railway.app/
   - Click **"Start a New Project"**
   - Click **"Deploy from GitHub repo"**
   - Select your `etf-backend` repository
   - Railway will auto-detect Python and deploy!

3. **Get your backend URL**:
   - Click on your project
   - Go to **Settings** → **Domains**
   - Click **"Generate Domain"**
   - Copy the URL (e.g., `https://your-app.railway.app`)

### Option 2: Deploy via Railway CLI

1. **Install Railway CLI**:
   ```bash
   # Windows (PowerShell)
   iwr https://railway.app/install.ps1 | iex

   # Mac/Linux
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **Login and deploy**:
   ```bash
   cd etf-backend
   railway login
   railway init
   railway up
   ```

3. **Get your URL**:
   ```bash
   railway domain
   ```

## Configuration

### Environment Variables (Optional)
If your backend needs environment variables:
1. Go to your Railway project
2. Click **Variables**
3. Add any needed variables from your `.env` file

### Custom Domain (Optional)
1. Go to **Settings** → **Domains**
2. Click **"Custom Domain"**
3. Add your domain and configure DNS

## Files Created for Railway

- `requirements.txt` - Lists all Python dependencies
- `Procfile` - Tells Railway how to start the app
- `railway.json` - Railway-specific configuration

## After Deployment

Your backend will be available at:
- **API**: `https://your-app.railway.app/api/etfs`
- **Docs**: `https://your-app.railway.app/docs`

**Next steps**:
1. Copy your Railway URL
2. Update `etf-frontend/.env.production`:
   ```env
   VITE_API_BASE_URL=https://your-app.railway.app/api
   ```
3. Rebuild frontend: `npm run build`
4. Upload to Hostinger via FTP

## Monitoring

- **View Logs**: Railway dashboard → Your project → **Deployments** → Click latest deployment
- **Check Health**: Visit `https://your-app.railway.app/docs` to see API docs
- **Restart**: Railway dashboard → **Deployments** → Click **Restart**

## Free Tier Limits

Railway free tier includes:
- $5 of usage per month
- Should be enough for moderate traffic
- Automatically sleeps after inactivity (wakes on request)

## Troubleshooting

### Build fails with "module not found"
- Check `requirements.txt` has all dependencies
- Make sure `setup.py` is included

### API returns 404
- Check the start command in `Procfile` or `railway.json`
- Verify the API is running on `$PORT` environment variable

### CORS errors
- Update `src/python_etf_db_service/api.py` CORS settings
- Add your Railway domain to `allow_origins`
- Redeploy: `railway up` or push to GitHub
