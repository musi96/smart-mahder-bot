# Smart Mahder Bot

An educational Telegram bot for sharing academic materials and course content, specifically designed for HUESA (Hawassa University Economics Students Association).

## Features

- 📚 Course material sharing system
- 🎓 Multi-field support (Economics, Psychology, Accounting, etc.)
- 📖 Year and semester-based organization
- 🔒 Channel membership verification
- 🌐 Web server for hosting platform compatibility

## Recent Updates (January 2025)

✅ **Security Improvements:**
- Moved sensitive data to environment variables
- Added .env support for configuration
- Secured bot token and channel information

✅ **Dependency Updates:**
- Updated python-telegram-bot to v22.2 (latest)
- Updated Flask to v3.1.1 (includes security fixes)
- Added version specifications for all dependencies
- Added python-dotenv for environment management

## Prerequisites

- Python 3.9 or higher
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A Telegram channel for user verification

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd smart-mahder-bot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit the `.env` file with your actual values:

```env
# Bot Configuration
BOT_TOKEN=your_actual_bot_token_here

# Channel Configuration  
CHANNEL_USERNAME=your_channel_username_without_@
CHANNEL_ID=your_channel_id_here

# Server Configuration (for hosting platforms like Render)
PORT=10000
```

### 5. Getting Required Values

**Bot Token:**
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the provided token to `BOT_TOKEN`

**Channel Information:**
1. Create a Telegram channel
2. Add your bot as an administrator
3. For Channel ID: Forward a message from the channel to [@userinfobot](https://t.me/userinfobot)
4. Use the channel username (without @) for `CHANNEL_USERNAME`

### 6. Run the Bot

For development:
```bash
python bot.py
```

For production (with proper logging):
```bash
python -u bot.py
```

## File Structure

```
smart-mahder-bot/
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
├── .env.example       # Environment template
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── UPDATE_FINDINGS.md # Update documentation
```

## Configuration

The bot uses the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token from BotFather | `123456:ABC-DEF...` |
| `CHANNEL_USERNAME` | Channel username without @ | `mychannel` |
| `CHANNEL_ID` | Telegram channel ID | `-1001234567890` |
| `PORT` | Web server port (for hosting) | `10000` |

## Deployment

### Render.com
1. Connect your GitHub repository
2. Add environment variables in Render dashboard
3. The bot includes a Flask health check server for Render compatibility

### Heroku
1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Set environment variables: `heroku config:set BOT_TOKEN=your_token`
4. Deploy: `git push heroku main`

### VPS/Server
1. Clone repository on server
2. Create `.env` file with production values
3. Set up systemd service or process manager
4. Ensure Python 3.9+ is installed

## Dependencies

- **python-telegram-bot 22.2**: Telegram Bot API wrapper
- **Flask 3.1.1**: Web server for hosting platforms
- **aiohttp 3.10.11**: HTTP client library
- **python-dotenv 1.0.0**: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Security Notes

- Never commit `.env` files to version control
- Rotate bot tokens if accidentally exposed
- Use environment variables for all sensitive data
- Keep dependencies updated regularly

## Support

For issues or questions:
1. Check the UPDATE_FINDINGS.md for recent changes
2. Create an issue in the repository
3. Contact the development team

## License

This project is created for educational purposes for HUESA students.