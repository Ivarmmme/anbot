import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from echo import echo, start_echo, stop
# Retrieve the bot token from an environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_USERS = [6369933143]  # Replace with actual user IDs

gif_users = set()

async def start_gif_reply(update: Update, context: CallbackContext) -> None:
    # Check if the command is issued in reply to a message
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        gif_users.add(user_id)
        await update.message.reply_text(f"Replying with GIFs to messages from user {user_id}.")
    else:
        # Functionality to manually add a user by ID
        args = update.message.text.split()
        if len(args) >= 2 and update.message.from_user.id in AUTHORIZED_USERS:
            user_id = int(args[1])
            gif_users.add(user_id)
            await update.message.reply_text(f"Replying with GIFs to messages from user {user_id}.")

GIF_URL = 'https://graph.org/file/6805acd7f5e08d1266dfa.mp4'  # Replace with your actual GIF URL
gif_users = set()
async def gif_reply(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.from_user.id in gif_users:
        # Reply with a GIF using the URL
        await update.message.reply_animation(animation=GIF_URL)
gif_users = set()
async def stop_echo(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id in AUTHORIZED_USERS:
        gif_users.clear()# Clear the set of users being replied with GIFs
        await update.message.reply_text("Mission accomplished, Niggesh is dead .")

def main() -> None:
    if TOKEN is None:
        print("The TELEGRAM_BOT_TOKEN environment variable is not set.")
        return
    application = Application.builder().token(TOKEN).build()

    # Command handler
    application.add_handler(CommandHandler('echo', start_echo, filters.ChatType.GROUPS))
    application.add_handler(CommandHandler('mathi', stop_echo, filters.ChatType.GROUPS))
    application.add_handler(CommandHandler('end', stop, filters.ChatType.GROUPS))
    application.add_handler(CommandHandler('surah', start_gif_reply, filters.ChatType.GROUPS))

    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, echo))
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, gif_reply))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
