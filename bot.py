import os
import random
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
WELCOME_PHOTO = "welcome.jpg"

logging.basicConfig(level=logging.INFO)


def mention(user):
    name = user.first_name or "Friend"
    return f'<a href="tg://user?id={user.id}">{name}</a>'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌸 Hello! I'm Siya Bot ❤️\n\n"
        "Welcome to Chill Corner Malayalam Chat!"
    )


# 👋 NEW MEMBER WELCOME
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    for user in update.message.new_chat_members:

        if user.is_bot:
            continue

        user_mention = mention(user)

        text = (
            f"👋 <b>Welcome {user_mention}!</b> ❤️\n\n"
            "🌸 <b>Welcome to Chill Corner</b> 🌸\n\n"
            "💬 Malayalam Chat • Share • Make Friends\n\n"
            "😊 Have fun and enjoy the group!\n\n"
            "📜 Please check our group rules."
        )

        keyboard = [[
            InlineKeyboardButton(
                "📜 Group Rules",
                callback_data="rules"
            )
        ]]

        markup = InlineKeyboardMarkup(keyboard)

        try:
            with open(WELCOME_PHOTO, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=text,
                    parse_mode="HTML",
                    reply_markup=markup
                )

        except FileNotFoundError:
            await update.message.reply_text(
                text,
                parse_mode="HTML",
                reply_markup=markup
            )


# 📜 RULES
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    rules_text = (
        "📜 <b>CHILL CORNER RULES</b>\n\n"
        "1️⃣ എല്ലാവരെയും respect ചെയ്യുക ❤️\n\n"
        "2️⃣ Spam / Flood ഒഴിവാക്കുക 🚫\n\n"
        "3️⃣ Unwanted links / Ads ഒഴിവാക്കുക 🔗\n\n"
        "4️⃣ Abuse / Bad words ഒഴിവാക്കുക ❌\n\n"
        "5️⃣ Personal fights ഒഴിവാക്കുക 🤝\n\n"
        "6️⃣ എല്ലാവരോടും friendly ആയി പെരുമാറുക 😊\n\n"
        "🌸 <b>Let's keep Chill Corner peaceful!</b> ❤️"
    )

    await query.message.reply_text(
        rules_text,
        parse_mode="HTML"
    )


# 💬 AUTO REPLY
async def chat_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()

    if text.startswith("/"):
        return

    user = update.effective_user

    if not user:
        return

    user_mention = mention(user)

    # 👋 HI / HELLO
    if any(x in text for x in [
        "hi", "hello", "hey", "hai",
        "ഹായ്", "ഹലോ"
    ]):
        replies = [
            f"👋 Hi {user_mention}! ❤️",
            f"😊 Hello {user_mention}! Welcome to Chill Corner!",
            f"🌸 Hey {user_mention}! എന്തൊക്കെയുണ്ട്?"
        ]

        await update.message.reply_text(
            random.choice(replies),
            parse_mode="HTML"
        )
        return

    # 😊 HOW ARE YOU
    if any(x in text for x in [
        "how are you",
        "സുഖമാണോ",
        "എങ്ങനെയുണ്ട്",
        "എന്തൊക്കെയുണ്ട്"
    ]):
        await update.message.reply_text(
            f"😊 എനിക്ക് സുഖമാണ് {user_mention}! "
            "നിങ്ങൾക്ക് എങ്ങനെയുണ്ട്? ❤️",
            parse_mode="HTML"
        )
        return

    # ❤️ THANKS
    if any(x in text for x in [
        "thanks",
        "thank you",
        "നന്ദി"
    ]):
        await update.message.reply_text(
            f"❤️ Welcome {user_mention}!",
            parse_mode="HTML"
        )
        return

    # 🌞 GOOD MORNING
    if any(x in text for x in [
        "good morning",
        "gm",
        "ഗുഡ് മോണിംഗ്"
    ]):
        await update.message.reply_text(
            f"🌞 Good Morning {user_mention}! ❤️",
            parse_mode="HTML"
        )
        return

    # 🌙 GOOD NIGHT
    if any(x in text for x in [
        "good night",
        "gn",
        "ഗുഡ് നൈറ്റ്"
    ]):
        await update.message.reply_text(
            f"🌙 Good Night {user_mention}! ❤️",
            parse_mode="HTML"
        )
        return

    # 💬 OTHER MESSAGES
    replies = [
        f"😊 {user_mention}, Ziya അല്ല... Siya ഇവിടെയുണ്ട്! ❤️",
        f"🌸 {user_mention}, പറഞ്ഞോളൂ...",
        f"😄 {user_mention}, എന്താ വിശേഷം?",
        f"💬 {user_mention}, Chat തുടരൂ ❤️",
        f"🤖 {user_mention}, Siya Bot കേൾക്കുന്നുണ്ട്!"
    ]

    await update.message.reply_text(
        random.choice(replies),
        parse_mode="HTML"
    )


async def error_handler(update, context):
    logging.error("Error: %s", context.error)


def main():

    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            rules,
            pattern="^rules$"
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            chat_reply
        )
    )

    app.add_error_handler(error_handler)

    print("🌸 Siya Bot is running...")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
