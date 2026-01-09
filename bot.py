# Telegram Quiz Bot (stable, python-telegram-bot v20+)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ======= CONFIG =======
TOKEN = "8445360818:AAFlyQw258Sv7sfo-mBJ8wvDPO0mx2rKekc"   # <-- yahan BotFather ka token paste karo
CHANNEL = "@ALLRESULTS"               # <-- yahan apne channel ka @username
# ======================

QUIZ = [
    {
        "q": "भारत की राजधानी क्या है?",
        "options": ["दिल्ली", "मुंबई", "कोलकाता", "चेन्नई"],
        "ans": "दिल्ली",
    },
    {
        "q": "2 + 2 = ?",
        "options": ["1", "2", "3", "4"],
        "ans": "4",
    },
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Channel membership check
    try:
        member = await context.bot.get_chat_member(CHANNEL, user_id)
        if member.status not in ("member", "administrator", "creator"):
            raise Exception
    except Exception:
        join_btn = [[
            InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL.lstrip('@')}")
        ]]
        await update.message.reply_text(
            "❌ Quiz ke liye pehle channel join karo",
            reply_markup=InlineKeyboardMarkup(join_btn),
        )
        return

    context.user_data["i"] = 0
    context.user_data["score"] = 0
    await send_question(update, context)

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    i = context.user_data.get("i", 0)

    if i >= len(QUIZ):
        await update.effective_message.reply_text(
            f"🎉 Quiz Finished\nScore: {context.user_data.get('score', 0)}/{len(QUIZ)}"
        )
        return

    q = QUIZ[i]
    keyboard = [[InlineKeyboardButton(opt, callback_data=opt)] for opt in q["options"]]
    await update.effective_message.reply_text(
        f"Q{i+1}. {q['q']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    i = context.user_data.get("i", 0)
    correct = QUIZ[i]["ans"]

    if query.data == correct:
        context.user_data["score"] = context.user_data.get("score", 0) + 1
        await query.message.reply_text("✅ सही")
    else:
        await query.message.reply_text(f"❌ गलत | सही: {correct}")

    context.user_data["i"] = i + 1
    await send_question(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_answer))
    app.run_polling()

if __name__ == "__main__":
    main()
