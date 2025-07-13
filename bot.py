import logging
import signal
import sys
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import register_handlers

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Init bot
bot = Client(
    name="NajvaBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

register_handlers(bot)

# Graceful shutdown
def shutdown(signum, frame):
    logger.info("Received shutdown signal, stopping bot...")
    bot.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

logger.info("🤖 MC NajvaBot is running...")
bot.run()
