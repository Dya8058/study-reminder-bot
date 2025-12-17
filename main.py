from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from apscheduler.schedulers.background import BackgroundScheduler
import datetime, os

TOKEN = os.environ.get("BOT_TOKEN")

scheduler = BackgroundScheduler()
scheduler.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to StudyReminderBot 📚\n\n"
        "Reminder set karne ke liye:\n"
        "/remind 18:30 Maths Revision"
    )

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        time = context.args[0]
        text = " ".join(context.args[1:])

        hour, minute = map(int, time.split(":"))
        now = datetime.datetime.now()
        run_time = now.replace(hour=hour, minute=minute, second=0)

        scheduler.add_job(
            send_reminder,
            "date",
            run_date=run_time,
            args=[update.effective_chat.id, text]
        )

        await update.message.reply_text(
            f"✅ Reminder set!\n⏰ {time}\n📘 {text}"
        )
    except:
        await update.message.reply_text(
            "❌ Galat format\nUse:\n/remind 18:30 Maths"
        )

async def send_reminder(chat_id, text):
    await app.bot.send_message(
        chat_id=chat_id,
        text=f"⏰ Reminder!\n📚 {text}"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("remind", remind))

app.run_polling()
