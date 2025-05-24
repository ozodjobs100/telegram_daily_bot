from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import db
import os
from dotenv import load_dotenv

load_dotenv()  # .env fayldan TOKEN ni yuklaydi
TOKEN = os.getenv("TOKEN")


ADMIN_ID = 6875167708  # <-- Bu yerga o'z Telegram user_id'ingizni yozing

db.setup()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db.add_user(user_id)
    await update.message.reply_text("Botga xush kelibsiz! Siz ro'yxatga olindingiz.")

async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Sizda bu buyruqni ishlatishga ruxsat yo'q.")
        return
    text = ' '.join(context.args)
    if not text:
        await update.message.reply_text("Xabar matni bo‘sh bo‘lmasligi kerak.")
        return
    db.set_message(text)
    await update.message.reply_text("Xabar muvaffaqiyatli yangilandi!")

async def send_daily_messages(app):
    while True:
        try:
            message = db.get_message()
            users = db.get_users()
            for user_id in users:
                try:
                    await app.bot.send_message(chat_id=user_id, text=message)
                except Exception as e:
                    print(f"Xatolik foydalanuvchi {user_id} ga yuborishda: {e}")
            await asyncio.sleep(86400)  # Har 24 soatda yuboradi
        except asyncio.CancelledError:
            print("✅ Xabar yuboruvchi task to‘xtatildi.")
            break

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setmessage", set_message))

    # Yuboruvchi task
    message_task = asyncio.create_task(send_daily_messages(app))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        # Bu yerda biz shunchaki to‘xtashni kutamiz
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        print("🔴 To‘xtatilmoqda...")
    finally:
        message_task.cancel()
        await app.stop()
        await app.shutdown()
        print("✅ Bot to‘xtatildi.")

if __name__ == '__main__':
    asyncio.run(main())
