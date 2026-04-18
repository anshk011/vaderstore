@echo off
REM Valorant Store Checker - Quick Deploy Script for Windows
REM This script helps you deploy to Railway with all necessary environment variables

echo.
echo 🎮 Valorant Store Checker - Railway Deployment
echo ==============================================
echo.

REM Check if railway CLI is installed
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Railway CLI not found!
    echo 📦 Install it with: npm i -g @railway/cli
    echo    Or visit: https://docs.railway.app/develop/cli
    pause
    exit /b 1
)

echo ✅ Railway CLI found
echo.

REM Check if logged in
railway whoami >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 🔐 Not logged in to Railway
    echo 📝 Running: railway login
    railway login
)

echo ✅ Logged in to Railway
echo.

REM Check if project exists
railway status >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 📦 No Railway project found
    echo 🆕 Creating new project...
    railway init
)

echo ✅ Railway project ready
echo.

REM Check environment variables
echo 🔍 Checking environment variables...
echo.

REM Check BOT_TOKEN
railway variables get BOT_TOKEN >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  BOT_TOKEN not set
    echo 📝 Get your bot token from @BotFather on Telegram
    echo.
    set /p BOT_TOKEN="Enter BOT_TOKEN: "
    railway variables set BOT_TOKEN="%BOT_TOKEN%"
    echo ✅ BOT_TOKEN set
) else (
    echo ✅ BOT_TOKEN already set
)

REM Check WEBAPP_URL
railway variables get WEBAPP_URL >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  WEBAPP_URL not set
    echo 📝 This will be your Railway app URL
    echo    Example: https://vstore-production-a665.up.railway.app
    echo.
    set /p WEBAPP_URL="Enter WEBAPP_URL: "
    railway variables set WEBAPP_URL="%WEBAPP_URL%"
    echo ✅ WEBAPP_URL set
) else (
    echo ✅ WEBAPP_URL already set
)

REM Set CHECK_INTERVAL if not set
railway variables get CHECK_INTERVAL >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  CHECK_INTERVAL not set, using default: 3600 (1 hour)
    railway variables set CHECK_INTERVAL="3600"
    echo ✅ CHECK_INTERVAL set to 3600
) else (
    echo ✅ CHECK_INTERVAL already set
)

echo.
echo 🚀 Deploying to Railway...
railway up

echo.
echo ✅ Deployment complete!
echo.
echo 📋 Next steps:
echo    1. Check logs: railway logs
echo    2. Open your bot in Telegram
echo    3. Send /start to test
echo.
echo 🔗 Useful commands:
echo    railway logs          - View logs
echo    railway open          - Open Railway dashboard
echo    railway status        - Check deployment status
echo    railway variables     - View all variables
echo.
echo 🎉 Happy gaming!
echo.
pause
