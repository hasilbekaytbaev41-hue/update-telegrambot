import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8732925466:AAFCckRwQ_6HZgPFEe6Cg-R33acgQ3pRHc8"
ADMIN_ID = 123456789  # o'zingni ID yoz
ADMIN_USERNAME = "Az1zbekoo99"  # @siz yoziladi

bot = telebot.TeleBot(TOKEN)

# Userlar bazasi (oddiy)
users = {}  # {user_id: {"orders": 0, "balance": 0}}

# 🔘 Asosiy menyu
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Bot narxlari")
    markup.add("🤖 Bot yaratish")
    markup.add("ℹ️ Bot haqida")
    markup.add("👤 Profil")
    markup.add("📞 Admin bilan bog'lanish")
    return markup

# 🔘 Profil menyu
def profile_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💳 Hisob to'ldirish")
    markup.add("⬅️ Orqaga")
    return markup

# 🚀 START
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {"orders": 0, "balance": 0}

    bot.send_message(message.chat.id, "Xush kelibsiz!", reply_markup=main_menu())

# 💰 Narxlar
@bot.message_handler(func=lambda msg: msg.text and "narx" in msg.text.lower())
def prices(message):
    bot.send_message(message.chat.id, "Bot narxlari:\n- Oddiy bot: 50k\n- Premium bot: 150k")

# 🤖 Bot yaratish
@bot.message_handler(func=lambda msg: msg.text == "🤖 Bot yaratish")
def create_bot(message):
    msg = bot.send_message(message.chat.id, "Hohlagan fikringizni yozing:")
    bot.register_next_step_handler(msg, send_to_admin)

# ℹ️ Bot haqida
@bot.message_handler(func=lambda msg: msg.text and "haqida" in msg.text.lower())
def about(message):
    bot.send_message(message.chat.id, "BU JOYNI O'ZING TO'LDIRASAN")

# 👤 Profil
@bot.message_handler(func=lambda msg: msg.text == "👤 Profil")
def profile(message):
    user_id = message.from_user.id
    user = users.get(user_id, {"orders": 0, "balance": 0})

    bot.send_message(
        message.chat.id,
        f"Zakazlar soni: {user['orders']}\nBalans: {user['balance']} so'm",
        reply_markup=profile_menu()
    )

# 💳 Hisob to‘ldirish
@bot.message_handler(func=lambda msg: msg.text == "💳 Hisob to'ldirish")
def payment(message):
    msg = bot.send_message(
        message.chat.id,
        "Karta: 9860 1901 0382 1087\n\nTo'lov qilgandan keyin chek (rasm) yuboring:"
    )
    bot.register_next_step_handler(msg, check_payment)

# 📸 Chek qabul qilish
def check_payment(message):
    if message.photo:
        bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=f"To'lov cheki\nUser ID: {message.from_user.id}"
        )
        bot.send_message(message.chat.id, "To'lov yuborildi ✅ Admin tekshiradi.")
    else:
        bot.send_message(message.chat.id, "Iltimos rasm yuboring!")

# ⬅️ Orqaga
@bot.message_handler(func=lambda msg: msg.text == "⬅️ Orqaga")
def back(message):
    bot.send_message(message.chat.id, "Asosiy menyu", reply_markup=main_menu())

# 📞 Admin bilan bog‘lanish
@bot.message_handler(func=lambda msg: msg.text == "📞 Admin bilan bog'lanish")
def contact_admin(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Admin profiliga o'tish", url=f"https://t.me/{ADMIN_USERNAME}"))

    bot.send_message(message.chat.id, "Admin bilan bog'lanish:", reply_markup=markup)

# 📩 Adminga yuborish (faqat bot yaratishdan keyin ishlaydi)
def send_to_admin(message):
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {"orders": 0, "balance": 0}

    users[user_id]["orders"] += 1

    bot.send_message(
        ADMIN_ID,
        f"Yangi zakaz!\n\nUser: {message.from_user.first_name}\nID: {user_id}\n\n{message.text}"
    )

    bot.send_message(
        message.chat.id,
        "Adminga yuborildi ✅\n1 soat ichida javob beriladi."
    )

# 💰 Admin balans qo‘shadi
@bot.message_handler(commands=['addbalance'])
def add_balance(message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, user_id, amount = message.text.split()
        user_id = int(user_id)
        amount = int(amount)

        if user_id not in users:
            users[user_id] = {"orders": 0, "balance": 0}

        users[user_id]["balance"] += amount

        bot.send_message(user_id, f"Balansingiz {amount} so'mga to'ldirildi ✅")
        bot.send_message(message.chat.id, "Qo‘shildi ✅")

    except:
        bot.send_message(message.chat.id, "Format xato!\nMisol: /addbalance 123456789 50000")

# 🔁 24/7 ishlash
import time

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(e)
        time.sleep(5)