import telebot
import random
import string

TOKEN = "8850545430:AAFxrTVb_MZrIHk-PFqrY-VnJ94z49QkRgY"
CREATOR_ID = 8569900825  # Это твой ID, проверь
bot = telebot.TeleBot(TOKEN)

def generate_key(length):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != CREATOR_ID:
        bot.reply_to(message, "🛑🛑🛑 ВЫ НЕ СОЗДАТЕЛЬ БОТА 🛑🛑🛑")
        return
    bot.reply_to(message, "🤖 Бот готов! Используй /gen [срок]")

@bot.message_handler(commands=['gen'])
def gen(message):
    if message.from_user.id != CREATOR_ID:
        bot.reply_to(message, "🛑🛑🛑 ВЫ НЕ СОЗДАТЕЛЬ БОТА 🛑🛑🛑")
        return
    try:
        args = message.text.split()
        if len(args) != 2:
            bot.reply_to(message, "Формат: /gen [1день/7дней/30дней/365дней/бесконечно]")
            return
        t = args[1].lower()
        if t == "1день":
            key = generate_key(16)
            label = "1 день"
        elif t == "7дней":
            key = generate_key(17)
            label = "7 дней"
        elif t == "30дней":
            key = generate_key(18)
            label = "30 дней"
        elif t == "365дней":
            key = generate_key(19)
            label = "365 дней"
        elif t == "бесконечно":
            key = generate_key(20)
            label = "Бесконечно"
        else:
            bot.reply_to(message, "Неверный срок!")
            return
        bot.reply_to(message, f"✅ Готово!\nСрок: {label}\nКлюч: `{key}`")
    except:
        bot.reply_to(message, "Ошибка. Проверь команду.")

bot.polling(non_stop=True)
