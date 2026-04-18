# 🎮 Valorant Store Checker

Check your VALORANT daily store, night market, and balance with a clean, modern web interface.

## ✨ Features

- 📦 **Daily Store** — View your 6 rotating skins with VP prices
- 🌙 **Night Market** — Track discounted offers when active
- 💎 **Balance Checker** — See your VP, Radianite, and Kingdom Credits
- 🌍 **Multi-Region** — Supports AP, NA, EU, KR, BR, LATAM
- 🔒 **Secure** — Official Riot OAuth, no passwords stored
- 🎨 **Dark Theme** — Sleek Vader-inspired design

## 🚀 Quick Start

### Deploy to Railway

1. **Clone the repo:**
   ```bash
   git clone <repo-url>
   cd valorant-store-checker
   ```

2. **Deploy to Railway:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Open your app:**
   ```bash
   railway open
   ```

### Run Locally

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```env
   PORT=5000
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
valorant-store-checker/
├── app.py                 # Flask web server
├── utils/
│   ├── auth.py           # Riot OAuth authentication
│   ├── valorant_api.py   # Valorant API client
│   └── helpers.py        # Utility functions
├── static/
│   ├── css/style.css     # Dark Vader theme
│   └── js/main.js        # Frontend logic
├── templates/
│   └── index.html        # Main web interface
└── config/
    └── constants.py      # API constants
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Flask server port | `5000` |

## 🛠️ API Endpoints

- `GET /` — Main interface
- `GET /health` — Health check
- `POST /auth/finalize` — Complete Riot OAuth
- `POST /store` — Fetch daily store
- `POST /nightmarket` — Fetch night market
- `POST /balance` — Fetch balance

## 🎨 Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** Vanilla JS + CSS
- **API:** Riot Games API + valorant-api.com
- **Deployment:** Railway

## 📝 How It Works

1. User clicks "Login with Riot"
2. Popup opens to Riot OAuth page
3. User logs in with Riot credentials
4. Redirect URL is captured
5. Tokens are extracted and validated
6. Store data is fetched from Riot API
7. Skin metadata is fetched from valorant-api.com
8. Everything is displayed in the UI

## 🔒 Security

- No passwords stored (OAuth only)
- Tokens stored in browser localStorage
- All API calls use HTTPS
- Official Riot authentication flow

## 🐛 Troubleshooting

### Store not loading
- Check if your session expired (re-login)
- Verify region is correct in settings
- Check browser console for errors

### Login popup blocked
- Allow popups for this site
- Or use the manual URL paste method

### API errors
- Tokens expire after ~1 hour
- Re-login to get fresh tokens
- Check Railway logs if deployed

## 📜 License

MIT License — feel free to use and modify!

## 🙏 Credits

- [Riot Games](https://www.riotgames.com/) for VALORANT
- [valorant-api.com](https://valorant-api.com/) for asset data
- [VShop](https://github.com/vshopapp/mobile) for API reference

---

**Made with ⚡ by the community**
