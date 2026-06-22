import telebot
import random
import string
import threading
import time
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8850545430:AAFxrTVb_MZrIHk-PFqrY-VnJ94z49QkRgY"
CREATOR_ID = 8569900825
bot = telebot.TeleBot(TOKEN)

# ================== БАЗА ДАННЫХ ==================
DB_FILE = "keys_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

# Загружаем базу
keys_db = load_db()

# ================== ГЕНЕРАЦИЯ ==================
def generate_key(length):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

# ================== КНОПКИ ==================
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != CREATOR_ID:
        bot.reply_to(message, "🛑🛑🛑 ВЫ НЕ СОЗДАТЕЛЬ БОТА 🛑🛑🛑")
        return

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🔑 1 день", callback_data="gen|1день"),
        InlineKeyboardButton("🔑 7 дней", callback_data="gen|7дней"),
        InlineKeyboardButton("🔑 30 дней", callback_data="gen|30дней"),
        InlineKeyboardButton("🔑 365 дней", callback_data="gen|365дней"),
        InlineKeyboardButton("♾️ Навсегда", callback_data="gen|бесконечно")
    )
    bot.reply_to(message, "🤖 Выбери срок:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('gen|'))
def gen_callback(call):
    if call.from_user.id != CREATOR_ID:
        bot.answer_callback_query(call.id, text="🛑 Ты не создатель бота!")
        return

    duration = call.data.split('|')[1]
    if duration == "1день":
        key = generate_key(16)
        label = "1 день"
    elif duration == "7дней":
        key = generate_key(17)
        label = "7 дней"
    elif duration == "30дней":
        key = generate_key(18)
        label = "30 дней"
    elif duration == "365дней":
        key = generate_key(19)
        label = "365 дней"
    elif duration == "бесконечно":
        key = generate_key(20)
        label = "Бесконечно"
    else:
        bot.answer_callback_query(call.id, text="Ошибка!")
        return

    # Сохраняем ключ в базу
    keys_db[key] = {"duration": label, "used": False}
    save_db(keys_db)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ Готово!\nСрок: {label}\n\n🔑 `{key}`",
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ================== ПРОВЕРКА КЛЮЧА ДЛЯ APK ==================
@bot.message_handler(commands=['check'])
def check_key(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Используй: /check [ключ]")
            return
        key = args[1].strip()
        if key in keys_db and not keys_db[key]["used"]:
            # Помечаем ключ как использованный
            keys_db[key]["used"] = True
            save_db(keys_db)
            bot.reply_to(message, "✅ Ключ валиден! Активация разрешена.")
        else:
            bot.reply_to(message, "❌ Неверный или уже использованный ключ!")
    except:
        bot.reply_to(message, "❌ Ошибка проверки.")

# ================== KEEP-ALIVE ==================
def keep_alive():
    while True:
        try:
            bot.get_me()
        except:
            pass
        time.sleep(3)

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    print("🤖 Бот запущен с базой данных!")
    bot.polling(non_stop=True)
