# LifeBrain Bot

LifeBrain is a Telegram productivity assistant built using python-telegram-bot.

It helps users with calculations, weather updates, news, task reminders, and simple natural chat without paid AI APIs.

This project is designed to be:

* Free and offline-friendly
* Easy to run locally
* Suitable for academic projects
* Safe for public GitHub sharing

---

## Features

* Solve math expressions
* Get weather by city
* Fetch latest news
* Add, view, and delete tasks
* Task reminders
* Daily summary
* Simple natural replies (rule-based, no OpenAI)

---

## Project Structure

```text
bot/
├── main.py
├── requirements.txt
├── .env.example
├── utils/
│   ├── solver.py
│   ├── translator.py
│   ├── weather.py
│   ├── news.py
│   ├── db.py
│   ├── memory.py
│   └── daily_summary.py
```

---

## Prerequisites

* Python 3.10 or 3.11
* Telegram account

---

## Local Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/ramkumar27072006/LifeBrain-tele-bot.git
cd LifeBrain-tele-bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a Telegram Bot

1. Open Telegram
2. Search for @BotFather
3. Run:

```text
/start
/newbot
```

4. Copy your bot token.

### 5. Create a .env file

```env
TELEGRAM_BOT_TOKEN=PASTE_YOUR_BOT_TOKEN_HERE
```

Never upload your .env file to GitHub.

### 6. Run the bot

```bash
python main.py
```

---

## Telegram Commands

| Command | Description |
|----------|-------------|
| /start | Start the bot |
| /help | Show help menu |
| /solve 25*(4/3) | Solve math expression |
| /weather chennai | Get weather |
| /news ai | Get news |
| /addtask drink water 14:00 | Add task |
| /showtasks | View tasks |
| /deletetask <id> | Delete a task |
| /daily 07:00 | Daily summary |

You can also type normal messages for simple chat replies.

---

## Public 24/7 Deployment Guide

### Why Not Render Free Tier?

Render free services automatically sleep after inactivity, causing Telegram bots to stop responding.

For a free always-on solution, PythonAnywhere is recommended.

### Step 1: Add Restart Protection

Wrap your polling logic in a restart loop:

```python
import time
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    while True:
        try:
            print('LifeBrain Bot is starting...')
        except Exception as e:
            logging.error(f'Bot crashed with error: {e}. Restarting in 15 seconds...')
            time.sleep(15)

if __name__ == '__main__':
    main()
```

### Step 2: Deploy on PythonAnywhere

```bash
git clone https://github.com/ramkumar27072006/LifeBrain-tele-bot.git
cd LifeBrain-tele-bot
pip install --user python-telegram-bot
```

### Step 3: Run in Background

```bash
nohup python main.py &
```

Check running processes:

```bash
ps ux
```

View logs:

```bash
cat nohup.out
```

### Step 4: Share Your Bot

```text
https://t.me/YourBotUsername
```

---

## Notes & Limitations

* No OpenAI or paid APIs used
* Bot must run locally or on a server
* Best tested on Python 3.10 and 3.11

---

## Author

Ramkumar R

B.Tech AI & Data Science

---

## License

This project is open-source and intended for educational use.
