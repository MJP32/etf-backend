@echo off
echo ========================================
echo Deploy to Railway via CLI
echo ========================================
echo.
echo This will:
echo 1. Install Railway CLI
echo 2. Login to Railway
echo 3. Deploy your backend
echo.
pause

echo.
echo Step 1: Installing Railway CLI...
echo ========================================
powershell -Command "iwr https://railway.app/install.ps1 -useb | iex"

echo.
echo Step 2: Login to Railway...
echo ========================================
echo This will open your browser to login
pause
railway login

echo.
echo Step 3: Initialize Railway Project...
echo ========================================
railway init

echo.
echo Step 4: Deploy to Railway...
echo ========================================
railway up

echo.
echo Step 5: Generate Public Domain...
echo ========================================
railway domain

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Your backend URL will be shown above.
echo Copy it and provide it to continue!
echo.
pause
