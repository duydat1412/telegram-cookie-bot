# 🍪 Telegram Cookie Bot

A powerful Telegram bot that automatically receives and stores browser cookies from a Chrome extension, making cookie management effortless and secure.

## ✨ Features

- 🔄 **Automatic Cookie Collection** - Extension automatically sends cookies when visiting websites
- 💾 **Smart Storage** - Stores cookies with timestamps, IP addresses, and user agent info
- 📋 **Easy Management** - Simple commands to list, view, and manage stored cookies
- 🕐 **Time Tracking** - Records when each cookie was captured
- 📊 **Statistics** - View statistics about your collected cookies
- 🔒 **Private & Secure** - All data stored in bot memory, no database needed

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Chrome Browser

### Installation

1. Clone this repository:
```bash
git clone https://github.com/duydat1412/telegram-cookie-bot.git
cd telegram-cookie-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your bot token:
```bash
export TELEGRAM_BOT_TOKEN='your_bot_token_here'
```

4. Run the bot:
```bash
python bot.py
```

## 📱 Bot Commands

- `/start` or `/help` - Show welcome message and available commands
- `/list` - List all stored cookies with timestamps
- `/get <number>` - View detailed information and download cookies as JSON file
- `/stats` - View statistics (total sites, total cookies, etc.)
- `/clear` - Delete all stored cookies

## 🔧 Chrome Extension Setup

1. Load the extension in Chrome (Developer Mode)
2. The extension will automatically send cookies to your bot
3. Visit any website and cookies will be captured

## 📊 Usage Example

```
User visits: https://example.com

Bot receives and stores:
- URL: example.com
- IP Address: 1.2.3.4
- User Agent: Mozilla/5.0...
- Cookies: [array of cookie objects]
- Timestamp: 2024-12-04 15:30:45

User types: /list

Bot responds:
📋 Danh sách Cookies (1)

1. example.com
   🕐 2024-12-04 15:30:45
   🍪 15 cookies

💡 Dùng /get 1 để xem chi tiết
```

## 🌐 Deploy to Cloud

### Render.com (Recommended - Free)

1. Fork this repository
2. Sign up at [Render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Add environment variable: `TELEGRAM_BOT_TOKEN`
6. Deploy!

### Other Platforms

- **Railway.app** - $5 free credit monthly
- **Replit** - Code directly in browser
- **Heroku** - Free tier available

## 🛡️ Security Notes

⚠️ **Important:**
- This tool is for educational and personal use only
- Only use on your own devices and accounts
- Respect privacy laws and terms of service
- Keep your bot token secure and never share it

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📧 Contact

For questions or support, contact via fb:(https://www.facebook.com/duydat141207)

---

Made with ❤️ by duydat1412

## 🎯 Project Structure

```
telegram-cookie-bot/
│
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── README.md          # This file
│
└── extension/         # Chrome extension files (separate repo)
    ├── background.js
    ├── content.js
    └── manifest.json
```

## 🔄 How It Works

1. **Extension captures cookies** when you visit websites
2. **Sends data to Telegram** via bot API
3. **Bot stores in memory** with metadata
4. **You retrieve anytime** using simple commands

## 💡 Tips

- Use `/clear` regularly to manage storage
- Download important cookies using `/get` command
- Check `/stats` to see your collection overview

---

⭐ If you find this project useful, please give it a star!
