#!/bin/bash

# Valorant Store Checker - Quick Deploy Script
# This script helps you deploy to Railway with all necessary environment variables

echo "🎮 Valorant Store Checker - Railway Deployment"
echo "=============================================="
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo "📦 Install it with: npm i -g @railway/cli"
    echo "   Or visit: https://docs.railway.app/develop/cli"
    exit 1
fi

echo "✅ Railway CLI found"
echo ""

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Not logged in to Railway"
    echo "📝 Running: railway login"
    railway login
fi

echo "✅ Logged in to Railway"
echo ""

# Check if project exists
if ! railway status &> /dev/null; then
    echo "📦 No Railway project found"
    echo "🆕 Creating new project..."
    railway init
fi

echo "✅ Railway project ready"
echo ""

# Check environment variables
echo "🔍 Checking environment variables..."
echo ""

BOT_TOKEN=$(railway variables get BOT_TOKEN 2>/dev/null)
WEBAPP_URL=$(railway variables get WEBAPP_URL 2>/dev/null)

if [ -z "$BOT_TOKEN" ]; then
    echo "⚠️  BOT_TOKEN not set"
    echo "📝 Get your bot token from @BotFather on Telegram"
    echo ""
    read -p "Enter BOT_TOKEN: " BOT_TOKEN
    railway variables set BOT_TOKEN="$BOT_TOKEN"
    echo "✅ BOT_TOKEN set"
else
    echo "✅ BOT_TOKEN already set"
fi

if [ -z "$WEBAPP_URL" ]; then
    echo "⚠️  WEBAPP_URL not set"
    echo "📝 This will be your Railway app URL"
    echo "   Example: https://vstore-production-a665.up.railway.app"
    echo ""
    read -p "Enter WEBAPP_URL: " WEBAPP_URL
    railway variables set WEBAPP_URL="$WEBAPP_URL"
    echo "✅ WEBAPP_URL set"
else
    echo "✅ WEBAPP_URL already set: $WEBAPP_URL"
fi

# Set CHECK_INTERVAL if not set
CHECK_INTERVAL=$(railway variables get CHECK_INTERVAL 2>/dev/null)
if [ -z "$CHECK_INTERVAL" ]; then
    echo "⚠️  CHECK_INTERVAL not set, using default: 3600 (1 hour)"
    railway variables set CHECK_INTERVAL="3600"
    echo "✅ CHECK_INTERVAL set to 3600"
else
    echo "✅ CHECK_INTERVAL already set: $CHECK_INTERVAL"
fi

echo ""
echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Check logs: railway logs"
echo "   2. Open your bot in Telegram"
echo "   3. Send /start to test"
echo ""
echo "🔗 Useful commands:"
echo "   railway logs          - View logs"
echo "   railway open          - Open Railway dashboard"
echo "   railway status        - Check deployment status"
echo "   railway variables     - View all variables"
echo ""
echo "🎉 Happy gaming!"
