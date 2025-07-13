import json
import uuid
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied, PeerIdInvalid
from db.db import SessionLocal
from db.models import Whispers, Users
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ==== INLINE HANDLER ====
def register_inline(client):
    @client.on_inline_query()
    async def answer(client: Client, query):
        sender = query.from_user.id
        query_list = query.query.strip().split(" ")
        db = SessionLocal()

        try:
            message = query.query.strip()

            if message == "":
                results = [
                    InlineQueryResultArticle(
                        title="NajvaBot",
                        input_message_content=InputTextMessageContent(
                            "پیام خود را بنویسید سپس در آخر @یوزرنیم شخص یاآیدی عددی شخص"),
                        url="https://t.me/",
                        description="پیام خود را بنویسید سپس در آخر @یوزرنیم شخص یاآیدی عددی شخص",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("اطلاعات بیشتر", url="https://t.me/")],
                                [InlineKeyboardButton("🔒 ارسال نجوا 🔒", switch_inline_query="")],
                            ]
                        ),
                    )
                ]
                await query.answer(results, cache_time=0)
                return

            if len(query_list) < 2 or not (
                query_list[-1].startswith("@") or (query_list[-1].isdigit() and len(query_list[-1]) >= 7)
            ):
                await query.answer([], cache_time=0)
                return

            message_text = " ".join(query_list[:-1])
            target = query_list[-1]
            if target.isdigit():
                target = int(target)

            to_user = await client.get_users(target)
            receiver_id = to_user.id

            to_user_json = json.dumps({
                "id": to_user.id,
                "first_name": to_user.first_name or "",
                "last_name": to_user.last_name or "",
                "username": to_user.username or ""
            })

            whisper_id = str(uuid.uuid4())
            whisper = Whispers(
                inline_message_id=whisper_id,
                message=message_text,
                sender_id=sender,
                receiver_id=receiver_id
            )
            db.add(whisper)
            db.commit()

            q = db.query(Users).filter(Users.user_id == sender).first()
            if q:
                q.target_user = to_user_json
            else:
                db.add(Users(user_id=sender, target_user=to_user_json))
            db.commit()

            data_string = f"{sender}|{receiver_id}|{whisper_id}"
            name = (to_user.first_name or "") + " " + (to_user.last_name or "")
            name = name.strip() or "کاربر"
            #mention = to_user.mention
            mention = f"<a href='tg://user?id={receiver_id}'>{name}</a>" 
            text = f"نجوا ارسال شد برای: {mention}\nفقط او می‌تواند پیام را ببیند."

            await query.answer(
                results=[
                    InlineQueryResultArticle(
                        title=f"نجوا به {name}",
                        input_message_content=InputTextMessageContent(
                            text,
                            parse_mode= ParseMode.HTML
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton(
                                    "🔐 دیدن نجوا 🔐",
                                    callback_data=data_string
                                )
                            ]]
                        )
                    )
                ],
                cache_time=0
            )
        except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid, Exception) as e:
            print(f"[InlineQuery Error] {e}")
            db.rollback()
            await query.answer([], cache_time=0)
        finally:
            db.close()