# Deployment Checklist

Quick checklist to deploy Valorant Store Checker with Telegram bot.

## ✅ Pre-Deployment

- [ ] Create Telegram bot via @BotFather
- [ ] Copy bot token
- [ ] Set bot description, about text, and commands
- [ ] Have Railway account ready

## 🚀 Deploy Steps

### 1. Initial Deploy

```bash
cd valorant-store-checker
railway login
railway init
railway up
```

### 2. Get Your Railway URL

After deployment completes:
```bash
railway domain
```

Copy the URL (e.g., `https://vstore-production-a665.up.railway.app`)

### 3. Set Environment Variables

In Railway dashboard → Variables:

```
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
WEBAPP_URL=https://your-app.railway.app
```

### 4. Configure Bot Menu Button

Send to @BotFather:
```
/setmenubutton
```
Select your bot → Edit menu button URL → Paste your Railway URL

### 5. Redeploy

```bash
railway up
```

Or click "Redeploy" in Railway dashboard.

## ✅ Post-Deployment

- [ ] Test bot: Send `/start` to your bot
- [ ] Verify Mini App opens
- [ ] Test login flow
- [ ] Check store loads correctly
- [ ] Verify balance shows
- [ ] Test region switching

## 🔍 Verification

### Check Logs

```bash
railway logs
```

Should see:
```
Starting Flask on port 8080
Starting Telegram bot
Bot starting... Mini App URL: https://...
```

### Test Endpoints

```bash
# Health check
curl https://your-app.railway.app/health

# Should return:
# {"status":"online","service":"valorant-store-checker"}
```

### Test Bot

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. Should see welcome message with buttons
5. Tap "Open Store Checker"
6. Should open the web app

## 🐛 Troubleshooting

### Bot not responding
```bash
# Check if bot is running
railway logs | grep "Bot starting"

# Verify token
railway variables | grep BOT_TOKEN
```

### Web app not loading
```bash
# Check Flask status
railway logs | grep "Starting Flask"

# Test health endpoint
curl https://your-app.railway.app/health
```

### Login fails
- Check browser console (F12)
- Verify redirect URL is correct
- Make sure popup isn't blocked

### Store shows errors
```bash
# Check API calls
railway logs | grep "store"

# Should see:
# [store] POST https://pd.ap.a.pvp.net/store/v3/storefront/...
# [store] status=200
```

## 📊 Monitoring

### Railway Dashboard

Monitor:
- CPU usage
- Memory usage
- Request count
- Error rate

### Bot Analytics

Check @BotFather → Bot Settings → Statistics

## 🔄 Updates

To deploy updates:

```bash
git add .
git commit -m "Update description"
railway up
```

Railway will:
1. Build new Docker image
2. Deploy with zero downtime
3. Keep environment variables

## 🎯 Next Steps

After successful deployment:

- [ ] Share bot with friends
- [ ] Monitor usage in Railway dashboard
- [ ] Set up custom domain (optional)
- [ ] Add more features (bundles, notifications, etc.)
- [ ] Configure auto-scaling if needed

## 💡 Tips

- **Use Railway's free tier** — Includes $5 credit/month
- **Monitor logs** — Check for errors regularly
- **Update regularly** — Keep dependencies up to date
- **Backup tokens** — Save BOT_TOKEN securely
- **Test before sharing** — Verify everything works

## 🆘 Need Help?

1. Check Railway logs: `railway logs`
2. Check bot logs in @BotFather
3. Review TELEGRAM_SETUP.md
4. Check GitHub issues
