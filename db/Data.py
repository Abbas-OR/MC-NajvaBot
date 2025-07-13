from pyrogram.types import InlineKeyboardButton

class Data:
    START = (
    " {} سلام! 👋\n"
    "من @{} ربات نجوا هستم\n"
    "با من میتونی به دوستات داخل گروه نجوا بدی"
)

    home_buttons = [
        [InlineKeyboardButton("🔒 ارسال نجوا 🔒", switch_inline_query="")],
        [InlineKeyboardButton(text="🏠 برگشت 🏠", callback_data="home")],
    ]
    buttons = [
        [
            InlineKeyboardButton("🔒 ارسال نجوا 🔒", switch_inline_query="")
        ],
        [
            InlineKeyboardButton("راهنمای استفاده ❔", callback_data="help"),
            InlineKeyboardButton("🎪 درباره ما 🎪", callback_data="about")
        ],
        [InlineKeyboardButton("♥ خدمات و اطلاعات بیشتر ♥", url="https://t.me/")],
        [InlineKeyboardButton("🎨 گروه پشتیبانی 🎨", url="https://t.me/")],
    ]
    HELP = """
فقست کافیه داخل گروه آیدی ربات رو بزنی 
سپس متنن پیام نجوا و سپس آیدی عددی یا یوزرنیم شخصی که بهش میخوای نجوا بدی

مثال :
`@bot your_message friend_username/id`
    """
    ABOUT = """
**درباره ربات** 

ساخت شده توسط : @Boss_Eric

Github : [Click Here](https://github.com/AbbasOR/)

Framework : [Pyrogram](docs.pyrogram.org)

Language : [Python](www.python.org)

Developer : @Boss_Eric
    """