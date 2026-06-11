# LifeBrain Bot Public Deployment Guide

To make your bot available to everyone 24/7, you cannot use Render's free tier for web services anymore. Render automatically puts free services to sleep after 15 minutes of inactivity, which will cause your Telegram bot to stop responding entirely until someone wakes it up.

Since you need a completely free, zero-downtime hosting solution so anyone can message your bot at any time, the absolute best platform for a Python Telegram bot is PythonAnywhere. It keeps your script running 24 hours a day without sleeping.

Here is the exact setup to make your bot public and permanent.

---

## Step 1: Prepare Your Code for Production

Before pushing your final code to GitHub, make sure your Telegram bot doesn't crash if it hits an unexpected error or an invalid user input. Wrap your main polling handler in a `while True` loop with error handling inside your local `main.py` file:

```python
import time
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    while True:
        try:
            print("LifeBrain Bot is starting...")
        except Exception as e:
            logging.error(f"Bot crashed with error: {e}. Restarting in 15 seconds...")
            time.sleep(15)

if __name__ == '__main__':
    main()
```

Commit and push this updated code to your GitHub repository.

---

## Step 2: Deploy to PythonAnywhere (24/7 Hosting)

1. Go to PythonAnywhere and create a free account.
2. Log in and go to the Consoles tab. Click on Bash to launch a cloud terminal.
3. Clone your public GitHub repository directly onto their server:

```bash
git clone https://github.com/ramkumar27072006/LifeBrain-tele-bot.git
```

4. Move into your project folder and install your code dependencies:

```bash
cd LifeBrain-tele-bot
pip install --user python-telegram-bot
```

---

## Step 3: Run the Bot Permanently in the Background

If you just run `python main.py`, the bot will stop working the moment you close your browser tab. To prevent this, use the `nohup` command.

```bash
nohup python main.py &
```

What this does:

- The `&` pushes the process to the background.
- `nohup` keeps it alive even when you log out.

How to check if it's running:

```bash
ps ux
```

How to view logs:

```bash
cat nohup.out
```

---

## Step 4: Share Your Bot

Your backend infrastructure is now decoupled from your laptop. The cloud server will keep the bot running.

Give users your Telegram link:

```text
https://t.me/YourBotUsername
```

Anyone can open the bot, tap Start, and receive a response from your application.
