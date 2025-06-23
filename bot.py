import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")
DOWNLOAD_DIR = "/tmp"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola 👋. Envíame el enlace del video público que quieres descargar.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    context.user_data['url'] = url
    keyboard = [
        [InlineKeyboardButton("📹 MP4 (video)", callback_data="mp4")],
        [InlineKeyboardButton("🎵 MP3 (audio)", callback_data="mp3")]
    ]
    await update.message.reply_text("¿En qué formato deseas descargar?", 
                                     reply_markup=InlineKeyboardMarkup(keyboard))

async def download_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    formato = query.data
    url = context.user_data.get('url')
    chat_id = query.message.chat_id

    if not url:
        await query.edit_message_text("No tengo el enlace guardado.")
        return

    params = {"outtmpl": os.path.join(DOWNLOAD_DIR, "%(title).50s.%(ext)s"),
              "format": "bestaudio+best",
              "noplaylist": True}
    if formato == "mp3":
        params["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]

    try:
        await query.edit_message_text("⏬ Descargando...")
        with yt_dlp.YoutubeDL(params) as ydl:
            info = ydl.extract_info(url, download=True)
            fname = ydl.prepare_filename(info)
            if formato == "mp3":
                fname = os.path.splitext(fname)[0] + ".mp3"

        with open(fname, "rb") as f:
            if formato == "mp3":
                await context.bot.send_audio(chat_id=chat_id, audio=f)
            else:
                await context.bot.send_video(chat_id=chat_id, video=f)
        os.remove(fname)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"❌ Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))
    app.add_handler(CallbackQueryHandler(download_and_send))
    app.run_polling()
