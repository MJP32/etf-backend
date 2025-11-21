@echo off
echo ========================================
echo Pushing ETF Backend to GitHub
echo ========================================
echo.
echo Repository: https://github.com/MJP32/etf-backend
echo.
echo You will be prompted for credentials:
echo   Username: MJP32
echo   Password: Use your GitHub Personal Access Token
echo.
echo Don't have a token? Get one at:
echo https://github.com/settings/tokens
echo.
pause

git push -u origin master

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS! Code pushed to GitHub
    echo ========================================
    echo.
    echo Next step: Deploy to Railway
    echo 1. Go to: https://railway.app/
    echo 2. Login with GitHub
    echo 3. New Project ^> Deploy from GitHub repo
    echo 4. Select: MJP32/etf-backend
    echo 5. Generate Domain and copy the URL
    echo.
) else (
    echo ========================================
    echo FAILED! Authentication error
    echo ========================================
    echo.
    echo Get a Personal Access Token:
    echo 1. Go to: https://github.com/settings/tokens
    echo 2. Generate new token (classic)
    echo 3. Check "repo" scope
    echo 4. Copy the token
    echo 5. Use it as your password when pushing
    echo.
)

pause
