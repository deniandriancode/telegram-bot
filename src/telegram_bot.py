import os
import logging
import threading
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, PrefixHandler, CallbackContext


### Prefix Handlers
async def test_pref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message_thread_id = update.message.message_thread_id
    await context.bot.send_message(chat_id=chat_id, text=f"TEST PASSED with message: {update.message.text} and args {context.args}", message_thread_id=message_thread_id)

async def reply_pref(update: Update, context: CallbackContext):
    print(update.message)
    
    
### Unknown Command Handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unknown command handler"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.", message_thread_id=update.message.message_thread_id)


def main():
    ### Preparation
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    # logging.FileHandler(filename='telegram.log', encoding='utf-8', mode='w')

    ### Begin Bot
    TELEGRAM_BOT_TOKEN = os.environ["QUIZ_FETCHER_TELEGRAM"]

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    command_prefix = "q"

    handlers = [
        PrefixHandler(command_prefix, "t", test_pref),
        PrefixHandler(command_prefix, "r", reply_pref),
        MessageHandler(filters.COMMAND, unknown) # unknown command handler
    ]

    application.add_handlers(handlers)

    application.run_polling(timeout=30)

if __name__ == "__main__":
    main()
