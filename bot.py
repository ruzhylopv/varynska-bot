from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
from os import getenv
from dotenv import load_dotenv, dotenv_values 

USERNAMES = ["ruzhylopv", "varynskat", "yanakilchinskaa"]
# шлях до твоєї картинки
TEMPLATE = "gift-card-online.png"

load_dotenv()
KEY = getenv("TELEGRAM_TOKEN")

# шрифт (може бути будь-який)
FONT = ImageFont.truetype("cormorant.ttf", 60)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username not in USERNAMES:
        return await update.message.reply_text("Access denied")
    text = update.message.text
    for_who, from_who, amount = list(map(lambda s: s.strip(), text.split(",")))

    # відкриваємо шаблон
    img = Image.open(TEMPLATE).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # координа́ти для тексту
    xto, yto = 140, 645
    xfrom, yfrom = 781, yto
    xamount, yamount = 140, 860

    # наносимо текст
    draw.text((xto, yto), for_who, font=FONT, fill="white")
    draw.text((xfrom, yfrom), from_who, font=FONT, fill="white")
    draw.text((xfrom, yfrom), from_who, font=FONT, fill="white")
    draw.text((xamount, yamount), amount, font=FONT, fill="white")

    # зберігаємо готове зображення
    img.save("output.png")

    # відправляємо назад
    await update.message.reply_document(document=open("output.png", "rb"))

# handle_text()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши текст у форматі: Для кого, від кого, сума. наприклад: петренка івана, василенка дмитра, 2100грн")

def main():
    app = Application.builder().token(KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
