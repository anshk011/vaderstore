# 🚂 Railway Deployment Guide

Complete guide for deploying to Railway with proper bot configuration.

## Issue: Bot Threading Error

You may see this error when running the bot in a thread:
```
RuntimeError: set_wakeup_fd only works in main thread of the main interpreter
```

This happens because asyncio signal handlers only work in the main thread.

## Solution: Two Deployment Options

### Option 1: Web App Only (Recommended for Railway Free Tier)

Run only the Flask web app with notification scheduler. The Telegram Mini App will work perfectly without the bot commands.

**What works:**
- ✅ Web interface
- ✅ Telegram Mini App
- ✅ Login and store viewing
- ✅ Favorite skins
- ✅ Automatic notifications

**What doesn't work:**
- ❌ Bot commands (`/store`, `/balance`, `/favorites`)
- ❌ Inline keyboard buttons

**How to deploy:**
```bash
railway up
```

The default `Procfile` will run:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
```

This includes the notification scheduler automatically.

### Option 2: Web App + Bot (Requires Railway Pro)

Run both the web app and bot as separate Railway services.

**Step 1: Deploy Web App**
```bash
railway up
```

**Step 2: Create Bot Service**

1. In Railway dashboard, click "New Service"
2. Select "Empty Service"
3. Connect to same GitHub repo
4. Set custom start command: `python bot.py`
5. Copy environment variables from web service

**Environment variables for bot service:**
```
BOT_TOKEN=your_bot_token
WEBAPP_URL=https://your-web-app.railway.app
```

**Note:** This requires Railway Pro plan ($5/month) for multiple services.

### Option 3: Run Bot Locally

Run the web app on Railway and the bot on your local machine or a separate server.

**Railway (Web App):**
```bash
railway up
```

**Local (Bot):**
```bash
cd valorant-store-checker
python bot.py
```

Make sure your `.env` file has:
```env
BOT_TOKEN=your_bot_token
WEBAPP_URL=https://your-railway-app.railway.app
```

## Recommended Setup

For most users, **Option 1** (Web App Only) is recommended because:

1. **Free tier friendly** - Uses only one Railway service
2. **Core features work** - Mini App, notifications, favorites all work
3. **Simpler deployment** - One command to deploy
4. **More reliable** - No threading issues

The bot commands are nice-to-have but not essential. Users can:
- Open the Mini App to view their store
- Star favorites in the web UI
- Receive notifications automatically

## Current Configuration

The project is configured for **Option 1** by default:

**`run.py`** - Runs Flask only (no bot thread)
```python
if __name__ == "__main__":
    from app import app
    # Notification scheduler starts automatically
    app.run(host="0.0.0.0", port=port)
```

**`app.py`** - Includes notification scheduler
```python
if os.getenv("BOT_TOKEN"):
    from notifications import start_notification_scheduler
    start_notification_scheduler()
```

**`Procfile`** - Defines both processes (Railway runs only `web` by default)
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
bot: python bot.py
```

## Deployment Steps (Option 1)

### 1. Set Environment Variables

In Railway dashboard or via CLI:
```bash
railway variables set BOT_TOKEN="your_bot_token"
railway variables set WEBAPP_URL="https://your-app.railway.app"
railway variables set CHECK_INTERVAL="3600"
```

### 2. Deploy

```bash
cd valorant-store-checker
railway up
```

### 3. Verify

Check logs:
```bash
railway logs
```

Look for:
```
Starting Flask on port 8080
Notification scheduler started (interval: 3600s)
```

### 4. Test

1. Open your Railway URL in browser
2. Login with Riot account
3. Verify store loads
4. Open Telegram bot
5. Send `/start`
6. Tap "Open Store Checker"
7. Should open your Railway URL

## Troubleshooting

### Bot commands don't work

**Expected behavior with Option 1:**
- `/start` works (shows Mini App button)
- `/help` works (shows help text)
- `/store`, `/balance`, `/favorites` don't work (bot not running)

**Solution:** Use the Mini App instead of bot commands.

### Notifications not working

**Check 1: Is scheduler running?**
```bash
railway logs | grep "Notification scheduler"
```

**Check 2: Is BOT_TOKEN set?**
```bash
railway variables | grep BOT_TOKEN
```

**Check 3: Are there users with favorites?**
```bash
railway logs | grep "Checking stores"
```

### Mini App doesn't open

**Check 1: Is WEBAPP_URL correct?**
```bash
railway variables | grep WEBAPP_URL
```

**Check 2: Did you set menu button in BotFather?**
1. Message @BotFather
2. Send `/setmenubutton`
3. Select your bot
4. Send your Railway URL

### Database not persisting

Railway's ephemeral filesystem means the database resets on each deploy.

**Solution:** Use Railway's persistent volumes:

1. In Railway dashboard, go to your service
2. Click "Variables" tab
3. Add volume mount: `/app/data`
4. Update code to use `/app/data/vstore.db`

Or use Railway's PostgreSQL addon for production.

## Performance Optimization

### Gunicorn Workers

Default: 2 workers
```
web: gunicorn app:app --workers 2
```

For more traffic:
```
web: gunicorn app:app --workers 4
```

### Notification Interval

Default: 1 hour (3600 seconds)

For testing:
```bash
railway variables set CHECK_INTERVAL="300"  # 5 minutes
```

For production:
```bash
railway variables set CHECK_INTERVAL="3600"  # 1 hour
```

### Database Optimization

For SQLite:
- Add indexes on frequently queried columns
- Clean up old notifications periodically
- Consider PostgreSQL for >1000 users

## Cost Estimate

**Option 1 (Web Only):**
- Free tier: $5 credit/month
- Usage: ~$3-4/month
- Supports: 100+ users

**Option 2 (Web + Bot):**
- Requires: Railway Pro ($5/month)
- Usage: ~$5-7/month
- Supports: 1000+ users

**Option 3 (Web on Railway, Bot Local):**
- Railway: Free tier
- Local: Free (your electricity)
- Supports: 100+ users

## Monitoring

### View Logs
```bash
railway logs
railway logs --follow  # Live logs
```

### Check Status
```bash
railway status
```

### View Metrics
```bash
railway open  # Opens dashboard
```

## Rollback

If something goes wrong:
```bash
railway rollback
```

Or in dashboard:
1. Go to "Deployments"
2. Click on previous deployment
3. Click "Redeploy"

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | No | 8080 | Railway sets automatically |
| `BOT_TOKEN` | Yes | - | From @BotFather |
| `WEBAPP_URL` | Yes | - | Your Railway URL |
| `CHECK_INTERVAL` | No | 3600 | Notification check interval (seconds) |

## Next Steps

1. Deploy with Option 1
2. Test Mini App functionality
3. Add some favorite skins
4. Wait for notifications
5. If you need bot commands, upgrade to Option 2

## Support

- Check logs: `railway logs`
- View docs: `README.md`, `NOTIFICATIONS_GUIDE.md`
- Railway docs: https://docs.railway.app

---

**Recommended:** Start with Option 1, upgrade to Option 2 only if you really need bot commands.
