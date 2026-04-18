# ⚠️ Important Deployment Note

## Current Configuration

The app is configured to run **Web App Only** mode by default. This is the recommended setup for Railway's free tier.

## What Works

✅ **Web Interface** - Full store checker at your Railway URL
✅ **Telegram Mini App** - Opens web interface inside Telegram
✅ **Favorite Skins** - Star button works when opened via Telegram
✅ **Automatic Notifications** - Background scheduler sends alerts
✅ **Login & Sessions** - Riot OAuth and session persistence

## What Doesn't Work (By Design)

❌ **Bot Commands** - `/store`, `/balance`, `/favorites` won't respond
❌ **Inline Buttons** - Buttons in bot messages won't work

**Why?** The bot process isn't running to save resources and avoid threading issues.

## How Users Should Use It

1. **Open Telegram** and find your bot
2. **Send `/start`** to the bot
3. **Tap "Open Store Checker"** button
4. **Login** with Riot account
5. **Star favorite skins** using ⭐ button
6. **Receive notifications** automatically when favorites appear

The Mini App provides the full experience - bot commands are optional.

## If You Want Bot Commands

See `RAILWAY_DEPLOYMENT.md` for three options:
1. **Web Only** (current, recommended)
2. **Web + Bot** (requires Railway Pro)
3. **Web on Railway + Bot locally**

## Quick Deploy

```bash
cd valorant-store-checker
railway up
```

Set these variables in Railway dashboard:
```
BOT_TOKEN=your_bot_token
WEBAPP_URL=https://your-app.railway.app
CHECK_INTERVAL=3600
```

## Verify It's Working

```bash
railway logs
```

Should see:
```
Starting Flask on port 8080
Notification scheduler started (interval: 3600s)
```

## Test It

1. Open your Railway URL in browser ✅
2. Login and view store ✅
3. Open Telegram bot ✅
4. Send `/start` ✅
5. Tap "Open Store Checker" ✅
6. Star some skins ✅
7. Wait for notifications ✅

## Need Help?

- Full docs: `README.md`
- Notification guide: `NOTIFICATIONS_GUIDE.md`
- Railway guide: `RAILWAY_DEPLOYMENT.md`
- Quick start: `QUICK_START.md`

---

**TL;DR:** The app works great without bot commands. Users interact via the Mini App, which provides the full experience.
