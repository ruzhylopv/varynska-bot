from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
from os import getenv
from dotenv import load_dotenv
from flask import Flask
import threading

# ----------------- CONFIG -----------------
USERNAMES = ["ruzhylopv", "varynskat", "yanakilchinskaa"]
TEMPLATE = "gift-card-online.png"
FONT_PATH = "cormorant.ttf"
FONT_SIZE = 60

# Load environment variables
load_dotenv()
KEY = getenv("TELEGRAM_TOKEN")

# Initialize Flask
app = Flask(__name__)

# ----------------- BOT FUNCTIONS -----------------
FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username not in USERNAMES:
        return await update.message.reply_text("Access denied")
    text = update.message.text
    try:
        for_who, from_who, amount = list(map(lambda s: s.strip(), text.split(",")))
    except ValueError:
        return await update.message.reply_text(
            "Неправильний формат. Використай: Для кого, від кого, сума"
        )

    # Open template and draw text
    img = Image.open(TEMPLATE).convert("RGBA")
    draw = ImageDraw.Draw(img)
    # Coordinates
    xto, yto = 140, 645
    xfrom, yfrom = 781, yto
    xamount, yamount = 140, 860
    # Draw text
    draw.text((xto, yto), for_who, font=FONT, fill="white")
    draw.text((xfrom, yfrom), from_who, font=FONT, fill="white")
    draw.text((xamount, yamount), amount, font=FONT, fill="white")
    # Save and send
    img.save("output.png")
    await update.message.reply_document(document=open("output.png", "rb"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Напиши текст у форматі: Для кого, від кого, сума. "
        "Наприклад: петренка івана, василенка дмитра, 2100грн"
    )

def run_bot():
    """Run the Telegram bot in a separate thread."""
    telegram_app = Application.builder().token(KEY).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    telegram_app.run_polling()

# ----------------- FLASK ROUTE -----------------
@app.route("/")
def index():
    return "Bot is running!"

# ----------------- MAIN -----------------
if __name__ == "__main__":
    # Start bot in a separate thread
    threading.Thread(target=run_bot).start()
    # Start Flask server (Render free tier requires this)
    port = int(getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
