import telebot
import os
from flask import Flask, request

# 🛡️ UJASUSI WA TOKEN
# Token inasomwa kutoka Vercel Environment Variables uliyoweka kitalaamu
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 799203820 
NAMBA_MALIPO = "255799203820"
JINA_MALIPO = "Elia"
LINK_CONNECTION = "https://t.me/zumaudaku18"

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        f"Habari {message.from_user.first_name}!\n\n"
        f"🛡️ Karibu kwenye Dvary Connection Bot.\n"
        f"Ili kupata link ya Zuma Udaku, lipia TSH 2,000 pekee kitalaamu.\n\n"
        f"💰 **Maelekezo ya Malipo**:\n"
        f"Namba: {NAMBA_MALIPO}\n"
        f"Jina: {JINA_MALIPO}\n\n"
        f"Baada ya kulipa, tuma namba ya muamala hivi:\n"
        f"** /muamala [NAMBA_YA_MUAMALA] **"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['muamala'])
def handle_muamala(message):
    bot.reply_to(message, "Muamala wako umepokelewa na Mwalimu Elia. Subiri uthibitisho kitalaamu.")
    bot.send_message(ADMIN_ID, f"🔔 MUAMALA MPYA!\nKutoka: {message.from_user.first_name}\nID: {message.from_user.id}\nText: {message.text}")

# Hii ni njia ya Vercel kupokea ujumbe (Webhook)
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Invalid Request', 403

@app.route('/')
def index():
    return "Dvary Bot is Online kitalaamu!"
