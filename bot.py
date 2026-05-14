import telebot
import os
from telebot import types

# 🛡️ UJASUSI WA TOKEN
# Token itasomwa kutoka Vercel Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 799203820 
NAMBA_MALIPO = "255799203820"
LINK_CONNECTION = "https://t.me/zumaudaku18"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
        f"Dvary Teach Bot Ipo Hewani! ✅\n\n"
        f"Ili kupata link ya kujiunga, lipia TSh 2,000.\n"
        f"Namba: {NAMBA_MALIPO}\n"
        f"Jina: Elia\n\n"
        f"Baada ya kulipa, tuma namba ya muamala hivi:\n"
        f"/muamala [NAMBA_YA_MUAMALA]"
    )

@bot.message_handler(commands=['muamala'])
def handle_muamala(message):
    bot.reply_to(message, "Muamala wako umepokelewa na Bosi Elia. Subiri uthibitisho kitalaamu.")
    bot.send_message(ADMIN_ID, f"🔔 MUAMALA MPYA!\nKutoka: {message.from_user.first_name}\nID: {message.from_user.id}\nText: {message.text}")

# Hii ni muhimu kwa Vercel kuitambua kodi
def handler(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.get_json(force=True))
        bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    bot.infinity_polling()

