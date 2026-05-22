import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from core.config import Config
from utils.logger import logger

class TelegramManager:
    def __init__(self, token):
        self.app = ApplicationBuilder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("status", self.status_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("IQ Option AI Bot is active! Use /status to check.")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Bot is running. Connected: True")

    def run(self):
        logger.info("Starting Telegram Bot...")
        self.app.run_polling()

    async def send_message(self, text):
        if Config.TELEGRAM_CHAT_ID:
            bot = Bot(token=Config.TELEGRAM_TOKEN)
            await bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text=text)
