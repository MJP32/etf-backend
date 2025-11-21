# Deploy Backend via GitHub to Railway

## Step 1: Create New GitHub Repository

1. Go to https://github.com/new
2. **Repository name**: `etf-backend` (or whatever you prefer)
3. **Description**: "ETF Portfolio Analyzer Backend API"
4. **Visibility**: Public or Private (your choice - both work with Railway)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 2: Update Git Remote

After creating the repo, GitHub will show you the repository URL. It will look like:
```
https://github.com/YOUR_USERNAME/etf-backend.git
```

Copy that URL, then run these commands in your terminal:

```bash
# Remove old remote
git remote remove origin

# Add your new remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/etf-backend.git

# Verify it's correct
git remote -v
```

## Step 3: Push to Your GitHub Repository

```bash
# Push to your new repository
git push -u origin master
```

If you get an authentication error, you may need to use a Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name like "Railway Deployment"
4. Check the "repo" scope
5. Click "Generate token"
6. Copy the token and use it as your password when pushing

## Step 4: Deploy to Railway

1. **Go to Railway**: https://railway.app/
2. **Sign in** with your GitHub account
3. Click **"New Project"**
4. Click **"Deploy from GitHub repo"**
5. **Authorize Railway** to access your GitHub repositories
6. **Select** your `etf-backend` repository
7. Railway will automatically detect it's a Python project and start deploying!

## Step 5: Generate Public Domain

After deployment completes (takes 2-3 minutes):

1. Click on your project in Railway dashboard
2. Go to **Settings** tab
3. Scroll to **Domains** section
4. Click **"Generate Domain"**
5. Copy the generated URL (e.g., `https://etf-backend-production-abc123.up.railway.app`)

## Step 6: Test Your Backend

Visit these URLs to verify it's working:
- `https://your-railway-url.railway.app/docs` - API documentation
- `https://your-railway-url.railway.app/api/etfs` - List of ETFs

## Step 7: Update CORS Settings

If needed, update the backend CORS to allow your frontend domain:

Edit `src/python_etf_db_service/api.py` and add your Railway URL:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://etfvaluepro.com",
        "https://www.etfvaluepro.com",
        "https://your-backend-url.railway.app",  # Add this
    ],
    # ...
)
```

Then commit and push:
```bash
git add src/python_etf_db_service/api.py
git commit -m "Update CORS for Railway deployment"
git push
```

Railway will automatically redeploy when you push!

## Troubleshooting

### Push rejected
- Make sure you removed the old remote and added your new one
- Check you have write access to the repository

### Railway build fails
- Check the build logs in Railway dashboard
- Ensure `requirements.txt` and `railway.json` are in the repository
- Verify all dependencies are listed in `requirements.txt`

### API returns 404
- Check the deployment logs in Railway
- Verify the start command in `railway.json`
- Make sure the app is listening on `$PORT` environment variable

## Auto-Deploy on Push

Railway automatically deploys when you push to GitHub! Just:
```bash
git add .
git commit -m "Your changes"
git push
```

Railway will rebuild and redeploy automatically.
