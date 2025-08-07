from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8492876490:AAHeabg0tSKRe_X0TOYGnzEQhA22sxmBGUU"

main_menu = ["Software", "App", "Coin", "Contact Us"]

products = {
    "Software": [
        {
            "name": "$70 per week",
            "payment_url": "https://nowpayments.io/payment/?iid=5957752765"
        },
        {
            "name": "$200 per month",
            "payment_url": "https://nowpayments.io/payment/?iid=5000925423"
        }
    ],
    "App": [
        {
            "name": "$70 per week",
            "payment_url": "https://nowpayments.io/payment/?iid=5957752765"
        },
        {
            "name": "$200 per month",
            "payment_url": "https://nowpayments.io/payment/?iid=5000925423"
        }
    ],
    "Coin": [
        {
            "name": "$30 = 20,000 FLASH USDT\nFully TRADABLE\nSecure & TRANSFERABLE\nInstant P2P Transactions\n45 DAYS STABLE VALUE",
            "payment_url": "https://nowpayments.io/payment/?iid=5849342108"
        },
        {
            "name": "$50 = 30,000 FLASH USDT\nFully TRADABLE\nSecure & TRANSFERABLE\nInstant P2P Transactions\n30 DAYS STABLE VALUE",
            "payment_url": "https://nowpayments.io/payment/?iid=5452220895"
        },
        {
            "name": "$100 = 50,000 FLASH USDT\nFully TRADABLE\nSecure & TRANSFERABLE\nInstant P2P Transactions\n90 DAYS STABLE VALUE",
            "payment_url": "https://nowpayments.io/payment/?iid=4895158191"
        },
        {
            "name": "$150 = 75,000 FLASH USDT\n5 FLASH BNB GIFT\nSPECIAL FOR BINANCE\nFully TRADABLE\nSecure & TRANSFERABLE\nInstant P2P Transactions\n180 DAYS STABLE VALUE\nCASH BACK GUARANTEE",
            "payment_url": "https://nowpayments.io/payment/?iid=5767788225"
        },
        {
            "name": "$500 = 750,000 FLASH USDT\n30 FLASH BNB GIFT\n2 FLASH BTC GIFT\n1 WEEK FREE SUPER APP\nSPECIAL FOR BINANCE\nFully TRADABLE\nSecure & TRANSFERABLE\nInstant P2P Transactions\n365 DAYS STABLE VALUE\nCASH BACK GUARANTEE",
            "payment_url": "https://nowpayments.io/payment/?iid=6182034333"
        }
    ]
}

contact_info = [
    "🌐 WEBSITE: https://cryptoflash.shop",
    "📱 WHATSAPP: +18603166184"
]

user_state = {}

def main_menu_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton(item)] for item in main_menu], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_state[chat_id] = "MAIN_MENU"
    await update.message.reply_text("👋 Welcome! Please select a category:", reply_markup=main_menu_keyboard())

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    state = user_state.get(chat_id, "MAIN_MENU")

    if state == "MAIN_MENU":
        if text in main_menu:
            if text == "Contact Us":
                message = "📞 Contact Information:\n\n" + "\n".join(contact_info)
                keyboard = ReplyKeyboardMarkup([[KeyboardButton("Back")]], resize_keyboard=True)
                user_state[chat_id] = "CONTACT_INFO"
                await update.message.reply_text(message, reply_markup=keyboard)

            else:
                user_state[chat_id] = text

                # اگر دسته App یا Software هست پیام لینک دانلود بده
                if text in ["App", "Software"]:
                    await update.message.reply_text(
                        "📲FOR DOWNLOAD PLEASE GO TO:\nhttps://cryptoflash.shop/app/"
                    )

                product_list = products[text]
                message = f"📂 {text} Products:\n\n"
                keyboard_buttons = []
                for idx, product in enumerate(product_list, 1):
                    message += f"{idx}. {product['name']}\n\n"
                    keyboard_buttons.append([KeyboardButton(str(idx))])
                keyboard_buttons.append([KeyboardButton("Back")])
                reply_markup = ReplyKeyboardMarkup(keyboard_buttons, resize_keyboard=True)
                await update.message.reply_text(message, reply_markup=reply_markup)
        else:
            await update.message.reply_text("❗ Please select a valid category from the menu.", reply_markup=main_menu_keyboard())

    elif state in main_menu:
        if text == "Back":
            user_state[chat_id] = "MAIN_MENU"
            await update.message.reply_text("👋 Back to main menu. Please select a category:", reply_markup=main_menu_keyboard())

        elif text.isdigit():
            product_list = products[state]
            idx = int(text)
            if 1 <= idx <= len(product_list):
                product = product_list[idx - 1]
                pay_button = InlineKeyboardButton("💳 Pay Now", url=product['payment_url'])
                markup = InlineKeyboardMarkup([[pay_button]])
                await update.message.reply_text(f"ℹ️ {product['name']}\n\nClick the button below to pay:", reply_markup=markup)

                keyboard = ReplyKeyboardMarkup([[KeyboardButton("Back")]], resize_keyboard=True)
                await update.message.reply_text("📩 After payment, please send your phone number starting with + for order confirmation.", reply_markup=keyboard)
                user_state[chat_id] = "AWAITING_PHONE"
            else:
                keyboard = ReplyKeyboardMarkup([[KeyboardButton("Back")]], resize_keyboard=True)
                await update.message.reply_text("❗ Please select a valid product number or press Back.", reply_markup=keyboard)

        else:
            keyboard = ReplyKeyboardMarkup([[KeyboardButton("Back")]], resize_keyboard=True)
            await update.message.reply_text("❗ Please send your phone number starting with + to order, or press Back.", reply_markup=keyboard)

    elif state == "CONTACT_INFO":
        if text == "Back":
            user_state[chat_id] = "MAIN_MENU"
            await update.message.reply_text("👋 Back to main menu. Please select a category:", reply_markup=main_menu_keyboard())
        else:
            keyboard = ReplyKeyboardMarkup([[KeyboardButton("Back")]], resize_keyboard=True)
            await update.message.reply_text("❗ Press Back to return to the main menu.", reply_markup=keyboard)

    elif state == "AWAITING_PHONE":
        if text == "Back":
            user_state[chat_id] = "MAIN_MENU"
            await update.message.reply_text("👋 Back to main menu. Please select a category:", reply_markup=main_menu_keyboard())
        elif text.startswith("+") and text[1:].isdigit():
            await update.message.reply_text("✅ Thank you! We will contact you shortly to confirm your order.")
            user_state[chat_id] = "MAIN_MENU"
            await update.message.reply_text("👋 Please select a category:", reply_markup=main_menu_keyboard())
        else:
            keyboard = ReplyKeyboardMarkup([[KeyboardButton("Back")]], resize_keyboard=True)
            await update.message.reply_text("❗ Please send your phone number starting with + or press Back.", reply_markup=keyboard)

    else:
        await update.message.reply_text("❗ Please select a valid option from the menu or send your phone number.", reply_markup=main_menu_keyboard())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
