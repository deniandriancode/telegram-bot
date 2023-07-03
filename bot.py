import os
import logging
import threading
import server
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler

def web_server_thread():
    # return # TODO
    server.start_http_server()


### Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    message_thread_id = update.message.message_thread_id
    chat_id = update.effective_chat.id
    if message_text.lower() == "hi":
        await context.bot.send_message(chat_id=chat_id, text="Hello!", message_thread_id=message_thread_id)
    elif message_text.lower() == "hello":
        await context.bot.send_message(chat_id=chat_id, text="Hi!", message_thread_id=message_thread_id)
    elif message_text.lower() == "ping":
        await context.bot.send_message(chat_id=chat_id, text="PONG!", message_thread_id=message_thread_id)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_caps = ' '.join(context.args).upper()
    message_thread_id = update.message.message_thread_id
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=message_caps, message_thread_id=message_thread_id)

### Inline Handlers
async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


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
    logging.FileHandler(filename='telegram.log', encoding='utf-8', mode='w')

    web_thread = threading.Thread(target=web_server_thread)
    web_thread.start()

    ### Begin Bot
    TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    handlers = [
        CommandHandler('start', start),
        CommandHandler('caps', caps),
        MessageHandler(filters.TEXT & (~filters.COMMAND), echo),
        InlineQueryHandler(inline_caps),
        MessageHandler(filters.COMMAND, unknown) # unknown command handler
    ]

    application.add_handlers(handlers)

    application.run_polling()

if __name__ == "__main__":
    main()
