import telebot
import random
import string
import threading
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8850545430:AAFxrTVb_MZrIHk-PFqrY-VnJ94z49QkRgY"
CREATOR_ID = 8569900825
bot = telebot.TeleBot(TOKEN)

# ================== ГЕНЕРАЦИЯ КЛЮЧА ==================
def generate_key(length):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

# ================== БАЗА ДАННЫХ (для защиты от повторов) ==================
import json
import os
DB_FILE = "keys_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

keys_db = load_db()

# ================== КНОПКИ ПРИ /START ==================
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

# ================== ГЕНЕРАЦИЯ ПО КНОПКЕ ==================
@bot.callback_query_handler(func=lambda call: call.data.startswith('gen|'))
def gen_callback(call):
    if call.from_user.id != CREATOR_ID:
        bot.answer_callback_query(call.id, text="🛑 Ты не создатель бота!")
        return

    duration = call.data.split('|')[1]
    if duration == "1день":
        key = generate_key(16)
        label = "1 день"
        duration_ms = 86400000
    elif duration == "7дней":
        key = generate_key(17)
        label = "7 дней"
        duration_ms = 604800000
    elif duration == "30дней":
        key = generate_key(18)
        label = "30 дней"
        duration_ms = 2592000000
    elif duration == "365дней":
        key = generate_key(19)
        label = "365 дней"
        duration_ms = 31536000000
    elif duration == "бесконечно":
        key = generate_key(20)
        label = "Бесконечно"
        duration_ms = 0
    else:
        bot.answer_callback_query(call.id, text="Ошибка!")
        return

    # Сохраняем в базу
    keys_db[key] = {"duration": duration_ms, "used": False}
    save_db(keys_db)

    # Отправляем ключ в формате с кликабельным текстом
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ Готово!\nСрок: {label}\n\n🔑 `{key}`",
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

# ================== ОБРАБОТКА ЗАПРОСОВ ОТ APK ==================
@bot.message_handler(commands=['check'])
def check_key(message):
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Используй: /check [ключ]")
            return
        key = args[1].strip()
        
        if key in keys_db and not keys_db[key]["used"]:
            # Помечаем как использованный
            keys_db[key]["used"] = True
            save_db(keys_db)
            duration_ms = keys_db[key]["duration"]
            bot.reply_to(message, f"✅|{duration_ms}")
        else:
            bot.reply_to(message, "❌ Неверный или уже использованный ключ!")
    except Exception:
        bot.reply_to(message, "❌ Ошибка проверки.")

# ================== ВЕЧНЫЙ БУДИЛЬНИК (Keep-Alive для Render) ==================
def keep_alive():
    while True:
        try:
            # Безопасный пинг, чтобы Render не усыпил бота
            bot.get_me()
        except Exception:
            pass
        time.sleep(45)  # 45 секунд — идеально, чтобы не нагружать API

threading.Thread(target=keep_alive, daemon=True).start()

# ================== ЗАПУСК ==================
if __name__ == "__main__":
    print("🤖 Бот запущен с вечным будильником!")
    bot.polling(non_stop=True)
