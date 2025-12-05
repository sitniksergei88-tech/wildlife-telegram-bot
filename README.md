# 🦁 Wildlife Telegram Bot

> Automated Telegram bot that posts daily wildlife videos from Reddit to your Telegram channel using GitHub Actions

[![GitHub](https://img.shields.io/badge/GitHub-sitniksergei88--tech-blue)](https://github.com/sitniksergei88-tech)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## ✨ Features

- 📺 **Automatic Updates**: Runs daily at 09:00 UTC (12:00 MSK) via GitHub Actions
- 🎬 **High-Quality Videos**: Fetches short wildlife videos (15-90 sec) from Reddit
- 🦓 **Multiple Sources**: Aggregates from r/wildlife, r/AnimalsBeingBros, r/NatureIsFuckingLit
- 🚀 **Easy Setup**: No server required, runs on GitHub Actions for free
- 🔧 **Fully Configurable**: Customize sources, posting schedule, and behavior
- 💾 **No Dependencies**: Pure Python with minimal requirements

## 📋 Requirements

- GitHub Account (for Actions)
- Telegram Bot Token (from @BotFather)
- Telegram Channel ID (where to post videos)
- Python 3.9+ (for local testing)

## 🚀 Quick Start

### Step 1: Create Telegram Bot

1. Write to [@BotFather](https://t.me/BotFather) on Telegram
2. Send command `/newbot`
3. Follow the instructions
4. **Copy the bot token** (format: `123456789:ABCdefGHIjklMnoPqrsTUVwxYZ`)

### Step 2: Get Chat ID

1. Add your bot to a Telegram channel
2. Send any message in the channel
3. Navigate to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Find `"chat": {"id": YOUR_ID}` in the response

### Step 3: Clone Repository

```bash
git clone https://github.com/sitniksergei88-tech/wildlife-telegram-bot.git
cd wildlife-telegram-bot
```

### Step 4: Add GitHub Secrets

1. Go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Add two secrets:
   - `TELEGRAM_BOT_TOKEN` = Your bot token
   - `TELEGRAM_CHAT_ID` = Your channel ID

### Step 5: Enable GitHub Actions

1. Go to **Actions** tab
2. Click **I understand my workflows, go ahead and enable them**
3. Done! ✅

## 📅 Schedule

The bot runs **daily at 09:00 UTC** (12:00 MSK). To change:

1. Edit `.github/workflows/wildlife-reddit.yml`
2. Change the cron schedule:
   ```yaml
   - cron: '0 9 * * *'  # Change these numbers
   ```

Common examples:
- `0 */6 * * *` = Every 6 hours
- `0 12,18 * * *` = At 12:00 and 18:00 UTC
- `0 0 * * *` = Daily at midnight UTC

## 🔌 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_id"

# Run script
python scripts/post_wildlife.py
```

## 📂 Project Structure

```
wildlife-telegram-bot/
├── .github/
│   └── workflows/
│       └── wildlife-reddit.yml      # GitHub Actions workflow
├── scripts/
│   └── post_wildlife.py             # Main script
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## 🎯 Customization

### Change Subreddits

Edit `scripts/post_wildlife.py`:

```python
SUBREDDITS = ['wildlife', 'AnimalsBeingBros', 'NatureIsFuckingLit']
```

### Modify Number of Videos

```python
VIDEO_LIMIT = 5  # Get top 5 videos per subreddit
```

### Post More Videos Per Run

```python
for video in videos[:3]:  # Change 3 to desired number
```

## 🛠️ Troubleshooting

### GitHub Actions Not Running

- Check **Actions** tab for errors
- Verify secrets are correctly set
- Ensure workflow file syntax is correct

### No Videos Posted

- Check if Reddit is accessible
- Verify subreddits have recent videos
- Increase `VIDEO_LIMIT` or lower engagement threshold

### Telegram Error

- Verify bot token is correct
- Check chat ID is valid
- Ensure bot has permission to post in channel

## 📊 How It Works

1. **GitHub Actions** triggers workflow at scheduled time
2. **Python script** fetches data from Reddit API
3. **Videos** are filtered by engagement (upvotes > 50)
4. **Top 3 videos** are sent to Telegram channel
5. **Logs** are available in Actions tab

## 📝 License

MIT License - feel free to use and modify!

## 💬 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## ⭐ Support

If this project helped you, please star it! ⭐

---

**Made with ❤️ by [@sitniksergei88-tech](https://github.com/sitniksergei88-tech)**
