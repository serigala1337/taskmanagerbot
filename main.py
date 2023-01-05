# use python python-telegram-bot 13.7
import os
import re
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    JobQueue,
    Job,
)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Selamat datang di bot jadwal harian! ketik /help untuk melihat daftar perintah yang tersedia",
    )


def help(update, context):
    update.message.reply_text(
        "Daftar perintah yang tersedia:\n\n"
        "/start - memulai bot\n"
        "/help - menampilkan daftar perintah\n"
        "/tambah - menambah tugas baru\n"
        "/lihat - melihat daftar tugas yang ada\n"
        "/hapus - menghapus tugas yang ada"
    )


def tambah(update, context):
    # Extract the task and due date from the user's message
    task_pattern = re.compile(r"/tambah (.*) pada (\d{2}/\d{2}/\d{4})")
    match = task_pattern.match(update.message.text)
    if match:
        task = match.group(1)
        due_date = match.group(2)

        # Add the task to the user's list
        user_id = update.message.from_user.id
        if user_id in tasks:
            tasks[user_id].append((task, due_date))
        else:
            tasks[user_id] = [(task, due_date)]

        update.message.reply_text(
            f"Tugas '{task}' dengan batas waktu {due_date} telah ditambahkan ke daftar tugas Anda"
        )
    else:
        update.message.reply_text(
            "Format perintah salah. Gunakan format: /tambah [tugas] pada [tanggal]"
        )


def lihat(update, context):
    user_id = update.message.from_user.id
    if user_id in tasks:
        # Build the message to send to the user
        message = "Daftar tugas:\n\n"
        for i, (task, due_date) in enumerate(tasks[user_id]):
            message += f"{i+1}. {task} (batas waktu: {due_date})\n"
        update.message.reply_text(message)
    else:
        update.message.reply_text("Tidak ada tugas yang tersimpan.")


def hapus(update, context):
    user_id = update.message.from_user.id
    if user_id in tasks:
        # Extract the task index from the user's message
        task_index = int(context.args[0]) - 1

        # Remove the task from the user's list
        try:
            del tasks[user_id][task_index]
            update.message.reply_text("Tugas berhasil dihapus dari daftar tugas.")
        except IndexError:
            update.message.reply_text("Tugas tidak ditemukan.")
    else:
        update.message.reply_text("Tidak ada tugas yang tersimpan.")


def main():
    # Create the Updater and pass it the bot's token.
    updater = Updater(
        "GANTI_TOKEN_BOT", use_context=True
    )

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("tambah", tambah))
    dp.add_handler(CommandHandler("lihat", lihat))
    dp.add_handler(CommandHandler("hapus", hapus))

    # Start the bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


# Global variable to store the user's tasks
tasks = {}

if __name__ == "__main__":
    main()
