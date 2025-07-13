import ast
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db.Data import Data
from db.db import SessionLocal
from db.models import Whispers, Users

def register_callback(client):
    @client.on_callback_query()
    async def _callbacks(client: Client, callback_query: CallbackQuery):
        db = SessionLocal()
        try:
            data = callback_query.data.strip()

            if "|" in data:
                parts = data.split("|")
                if len(parts) != 3:
                    await callback_query.answer("داده نامعتبر است.", show_alert=True)
                    return

                sender_id, receiver_id, whisper_inline_id = parts
                sender_id = int(sender_id)
                receiver_id = int(receiver_id)

                # چک کن کاربر اجازه دیدن دارد یا نه
                if callback_query.from_user.id not in [sender_id, receiver_id]:
                    await callback_query.answer("شما اجازه مشاهده این پیام را ندارید.", show_alert=True)
                    return

                whisper = db.query(Whispers).filter(
                    Whispers.inline_message_id == whisper_inline_id
                ).first()

                if whisper and whisper.message.strip():
                    # اگر گیرنده است و هنوز نخونده → بروزرسانی کن
                    if callback_query.from_user.id == receiver_id and not whisper.is_read:
                        whisper.is_read = True
                        db.commit()

                        # فقط در صورت خواندن توسط گیرنده، پیام اصلی ادیت شود
                        text = f"✅ نجوا توسط {callback_query.from_user.mention} خوانده شد."

                        reply_markup = InlineKeyboardMarkup(
                            [[
                                InlineKeyboardButton("🔐 دیدن نجوا 🔐", callback_data=data),
                                InlineKeyboardButton("پاسخ", switch_inline_query_current_chat=f"{sender_id}"),
                            ]]
                        )

                        if callback_query.message:
                            await client.edit_message_text(
                                chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.id,
                                text=text,
                                disable_web_page_preview=True,
                                reply_markup=reply_markup,
                            )
                        elif callback_query.inline_message_id:
                            await client.edit_inline_text(
                                inline_message_id=callback_query.inline_message_id,
                                text=text,
                                disable_web_page_preview=True,
                                reply_markup=reply_markup,
                            )

                    # نمایش پیام فقط برای مشاهده، حتی اگر فرستنده باشد
                    await callback_query.answer(whisper.message, show_alert=True)
                    print(f"[Callback] Whisper shown to user_id {callback_query.from_user.id}")

                else:
                    await callback_query.answer("نجوا یافت نشد.", show_alert=True)
            else:
                await callback_query.answer("دکمه نامعتبر است.", show_alert=True)
        except Exception as e:
            print(f"[Callback Error]: {e}")
            await callback_query.answer("خطایی رخ داده است.", show_alert=True)
        finally:
            db.close()
