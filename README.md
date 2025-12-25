# LifeBrain Bot

LifeBrain is a **Telegram productivity assistant** built using **python-telegram-bot**.
It helps users with calculations, weather updates, news, task reminders, and simple natural chat — **without paid AI APIs**.

This project is designed to be:

*  Free & offline-friendly
*  Easy to run locally
*  Suitable for academic projects
*  Safe for public GitHub sharing

---

##  Features

*  Solve math expressions
*  Get weather by city
*  Fetch latest news
*  Add, view, and delete tasks
*  Task reminders
*  Daily summary
*  Simple natural replies (rule-based, no OpenAI)

---

##  Project Structure

```
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

* Python **3.10 or 3.11** ( Python 3.12 may cause dependency issues)
* Telegram account

---

##  Setup Instructions

### 1️ Clone the repository

```bash
git clone https://github.com/ramkumar27072006/bot.git
cd bot
```

---

### 2️ Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

---

### 3️ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️ Create Telegram Bot Token

1. Open Telegram
2. Search **@BotFather**
3. Run:

   ```
   /start
   /newbot
   ```
4. Copy the **BOT TOKEN**

---

### 5️ Create `.env` file

Create a file named `.env` in the project root.

```env
TELEGRAM_BOT_TOKEN=PASTE_YOUR_BOT_TOKEN_HERE
```

 **Never upload `.env` to GitHub**

---

### 6️ Run the bot

```bash
python main.py
```

You should see:

```
 LifeBrain Bot running (free version)...
```

---

##  Telegram Commands

| Command                      | Description           |
| ---------------------------- | --------------------- |
| `/start`                     | Start the bot         |
| `/help`                      | Show help menu        |
| `/solve 25*(4/3)`            | Solve math expression |
| `/weather chennai`           | Get weather           |
| `/news ai`                   | Get news              |
| `/addtask drink water 14:00` | Add task              |
| `/showtasks`                 | View tasks            |
| `/deletetask <id>`           | Delete a task         |
| `/daily 07:00`               | Daily summary         |

You can also **type normal messages** for simple chat replies.

---

##  Task Deletion

Tasks can be deleted manually using:

```text
/deletetask <task_id>
```

(Task IDs are shown in `/showtasks`)

---

##  Notes & Limitations

* No OpenAI / paid APIs used
* Bot must be running locally or on a server
* Stopping the terminal will stop the bot
* Best tested on Python **3.10 / 3.11**

---

##  Deployment (Optional)

You can deploy this bot on:

* Railway
* Render
* AWS EC2
* DigitalOcean
* Raspberry Pi.

(Local PC works fine for college projects.)

---

##  Author

**Ramkumar R**
B.Tech AI & Data Science
Academic / Learning Project

---

##  License

This project is open-source and intended for **educational use**.


