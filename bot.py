from PIL import Image
from google import genai
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from config import (
    TELEGRAM_TOKEN,
    GEMINI_API_KEY,
    CHANNEL_ID
)


# Gemini Setup

client = genai.Client(
    api_key=GEMINI_API_KEY
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🤖 MH Trader AI Active\n\n"
        "📸 BTC / XAUUSD / Forex Chart পাঠান।"
    )



async def analyze_chart(update, context):

    try:

        # Message থেকে ছবি নেওয়া

        photo = update.message.photo[-1]

        file = await photo.get_file()

        image_path = "chart.png"

        await file.download_to_drive(image_path)



        img = Image.open(image_path)

        img.thumbnail((1200,1200))



        prompt = """

You are MH Trader AI.

You are a professional crypto and forex scalping analyst.


Analyze this chart image.


Focus:
M1
M5
M15


Use:

EMA 9/21
RSI
Support Resistance
Candlestick
Price Action
Market Structure


Give:


🔥 MH Trader Signal


📊 Market:

⏱ Timeframe:


📈 Trend:


🌐 Market Condition:


🎯 Signal:
BUY / SELL / WAIT


💯 Confidence:


📍 Entry Zone:


🛑 Stop Loss:


✅ Take Profit 1:


✅ Take Profit 2:


⚖️ Risk Reward:


📌 Support:


📌 Resistance:


🧠 Reason:

EMA:

RSI:

Price Action:


If WAIT:

BUY confirmation:

SELL confirmation:


⚠️ Risk Warning:

Not financial advice.


"""


        response = client.models.generate_content(

            model="gemini-3.1-flash-lite",

            contents=[
                prompt,
                img
            ]

        )


        result = response.text



        message = (
            "🔥 MH Trader Signal\n\n"
            + result
        )


        # User কে Reply

        await update.message.reply_text(
            message[:4000]
        )


        # Channel এ Auto Post

        await context.bot.send_message(

            chat_id=CHANNEL_ID,

            text=message[:4000]

        )



        if os.path.exists(image_path):

            os.remove(image_path)



    except Exception as e:

        await update.message.reply_text(

            "❌ Error:\n\n"
            + str(e)

        )





async def photo_handler(update, context):

    await update.message.reply_text(
        "📊 Chart Received...\n🤖 AI Analysis চলছে..."
    )

    await analyze_chart(
        update,
        context
    )





def main():

    app = Application.builder()\
        .token(TELEGRAM_TOKEN)\
        .build()



    # Start command

    app.add_handler(

        CommandHandler(
            "start",
            start
        )

    )



    # ব্যক্তিগত chat ছবি

    app.add_handler(

        MessageHandler(
            filters.PHOTO,
            photo_handler
        )

    )



    print(
        "🚀 MH Trader AI Bot Running..."
    )



    app.run_polling()





if __name__ == "__main__":

    main()MH-Trader-Bot