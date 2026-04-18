# 🚀 Push to GitHub

Your repository is ready to push! Follow these steps:

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Repository name: `valorant-store-checker`
3. Description: `Check your VALORANT daily store, night market, and balance`
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

## Step 2: Add GitHub Remote

Copy the repository URL from GitHub (looks like `https://github.com/yourusername/valorant-store-checker.git`)

Then run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/valorant-store-checker.git
```

## Step 3: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
gh repo create valorant-store-checker --public --source=. --remote=origin
git push -u origin main
```

## Verify

After pushing, visit your repository on GitHub:
```
https://github.com/YOUR_USERNAME/valorant-store-checker
```

You should see:
- ✅ Clean README.md with project description
- ✅ All source files
- ✅ .gitignore (no .env or database files)
- ✅ Deployment guides

## What's Included

```
valorant-store-checker/
├── README.md              ← Main documentation
├── .gitignore             ← Excludes .env, .db files
├── app.py                 ← Flask server
├── requirements.txt       ← Python dependencies
├── Dockerfile             ← Railway deployment
├── deploy.sh / .bat       ← Deployment scripts
├── utils/                 ← Auth & API logic
├── static/                ← CSS & JS
├── templates/             ← HTML
└── config/                ← Constants
```

## Next Steps

After pushing to GitHub:

1. **Deploy to Railway:**
   ```bash
   railway login
   railway init
   railway up
   ```

2. **Share your project:**
   - Add topics: `valorant`, `riot-games`, `flask`, `python`
   - Add a nice banner image
   - Star your own repo 😄

3. **Optional: Add GitHub Actions**
   - Auto-deploy on push
   - Run tests
   - Check code quality

## Troubleshooting

### Authentication Error
If you get authentication errors:
- Use a Personal Access Token instead of password
- Or use SSH: `git remote set-url origin git@github.com:YOUR_USERNAME/valorant-store-checker.git`

### Large Files
If you accidentally committed large files:
```bash
git rm --cached large-file.db
git commit -m "Remove large file"
```

---

**Ready to push!** 🎉
