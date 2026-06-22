import telebot
import random
import string
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8850545430:AAFxrTVb_MZrIHk-PFqrY-VnJ94z49QkRgY"
CREATOR_ID = 8569900825
bot = telebot.TeleBot(TOKEN)

def generate_key(length):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

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

    # Ключ отправляется ВНУТРИ ТЕКСТА с дополнительными кавычками
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ Готово!\nСрок: {label}\n\n🔑 `{key}`",
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id)

bot.polling(non_stop=True)
