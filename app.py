import logging
import os
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler
import openai

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the Telegram token and OpenAI API key
TELEGRAM_TOKEN = "6258580641:AAFZU7_J_J2SR2govL-8EPEVKjt45gNmwdc"
OPENAI_API_KEY = "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"

# Set up the Telegram bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Set up the OpenAI API client
openai.api_key = OPENAI_API_KEY

# Define the inline query handler function
def inlinequery(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not query:
        return
    response = openai.Completion.create(
        engine="davinci",
        prompt=query,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    update.inline_query.answer(
        results=[telegram.InlineQueryResultArticle(
            id=query,
            title=message,
            input_message_content=telegram.InputTextMessageContent(message),
        )]
    )

# Set up the inline query handler
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))

# Start the bot
updater.start_polling()
updater.idle()
