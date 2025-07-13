# 🎯 Metal Wings Tournament Bot

A comprehensive Discord bot for managing tournament systems with Google Sheets integration.

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended)
1. Fork this repository
2. Go to [Railway](https://railway.app/)
3. Connect your GitHub account
4. Create new project from GitHub repo
5. Add environment variables:
   - `DISCORD_TOKEN`: Your Discord bot token
6. Deploy!

### Option 2: Render
1. Fork this repository
2. Go to [Render](https://render.com/)
3. Create new Web Service
4. Connect your GitHub repo
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python app.py`
7. Add environment variables:
   - `DISCORD_TOKEN`: Your Discord bot token
8. Deploy!

### Option 3: Heroku
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Run these commands:
```bash
heroku create your-bot-name
heroku config:set DISCORD_TOKEN=your_token_here
git push heroku main
```

## 📋 Prerequisites

1. **Discord Bot Token**
   - Create a bot at [Discord Developer Portal](https://discord.com/developers/applications)
   - Copy the token

2. **Google Sheets Setup**
   - Create a Google Cloud Project
   - Enable Google Sheets API
   - Create service account and download JSON credentials
   - Share your sheets with the service account email

## 🔧 Environment Variables

Create a `.env` file or set these in your hosting platform:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

## 📁 File Structure

```
├── app.py              # Main bot file
├── sheet.py            # Google Sheets integration
├── requirements.txt    # Python dependencies
├── Procfile           # For Heroku/Railway
├── runtime.txt        # Python version
└── .env              # Environment variables (create this)
```

## 🛠️ Local Development

1. Install Python 3.11+
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create `.env` file with your Discord token
4. Run the bot:
```bash
python app.py
```

## 📊 Features

- **Tournament Management**: Complete tournament system with rounds
- **Role Management**: Automatic role assignment/removal
- **Google Sheets Integration**: Real-time data logging
- **Queue System**: Interactive player distribution
- **Check-in System**: Automated player check-ins
- **Team Balancing**: Mathematical team optimization
- **Support Tools**: Staff management commands

## 🔐 Security Notes

- Never commit your `.env` file or Google credentials
- Use environment variables for sensitive data
- Keep your bot token secure

## 📞 Support

For issues or questions, check the bot's help command: `/help`

---

**Made with ❤️ for Metal Wings Tournament System** 