import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

async def répondre(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message.text

    réponse = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Tu es BG-MARKET Assistant, assistant commercial officiel spécialisé dans les smartphones."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    await update.message.reply_text(
        réponse.choices[0].message.content
    )


app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, répondre)
)

app.run_polling()
