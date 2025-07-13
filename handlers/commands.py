from pyrogram import Client, filters
from pyrogram.types import Message
from db.Data import Data
from pyrogram.types import InlineKeyboardMarkup
from db.db import SessionLocal
from db.models import BotUsers

def register(client):
    @client.on_message(filters.command("start") & filters.incoming & filters.private)
    async def start(client: Client, message: Message):
        user = message.from_user
        db = SessionLocal()

        first_name = user.first_name or ""
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()

        try:
            existing_user = db.query(BotUsers).filter(BotUsers.user_id == user.id).first()
            if not existing_user:
                new_user = BotUsers(
                    user_id=user.id,
                    name=full_name,
                    username=user.username
                )
                db.add(new_user)
                db.commit()
        except Exception as e:
            print(f"[Start Command Error] {e}")
        finally:
            db.close()

        bot_user = await client.get_me()
        mention = bot_user.username
        await client.send_message(
            message.chat.id,
            Data.START.format(message.from_user.mention, mention),
            reply_markup=InlineKeyboardMarkup(Data.buttons),
        )