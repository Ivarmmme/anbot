from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters


AUTHORIZED_USERS = [6369933143]  # Replace with actual user IDs
echo_users = set()

async def start_echo(update: Update, context: CallbackContext) -> None:
    # Check if the command is issued in reply to a message
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        echo_users.add(user_id)
        await update.message.reply_text(f"Echoing messages from user {user_id}.")
    else:
        # Existing functionality to manually add a user by ID
        args = update.message.text.split()
        if len(args) >= 2 and update.message.from_user.id in AUTHORIZED_USERS:
            user_id = int(args[1])
            echo_users.add(user_id)
            await update.message.reply_text(f"Echoing messages from user {user_id}.")


async def echo(update: Update, context: CallbackContext) -> None:
    if update.message and update.message.from_user.id in echo_users:
        # Check if 'ivar' is mentioned in the message text
        if 'ivar' in update.message.text.lower():
            # Send the custom response as a reply to the original message
            await update.message.reply_text("Ivar is dope")
        else:
            # Echo the original message as a reply
            await update.message.reply_text(update.message.text)
