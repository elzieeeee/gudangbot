
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import sqlite3
import os

DB_PATH = "inventory.db"

def get_product_info(keyword):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT nama_produk, stok, lokasi_rak, expired_date FROM products WHERE nama_produk LIKE ?", ('%' + keyword + '%',))
    result = c.fetchone()
    conn.close()
    return result

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya GudangBot.\nKetik: \n`stok [nama barang]`\n`lokasi [nama barang]`\nUntuk bantuan cepat.", parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text.startswith("stok"):
        keyword = text.replace("stok", "").strip()
        info = get_product_info(keyword)
        if info:
            nama, stok, lokasi, exp = info
            await update.message.reply_text(f"✅ *{nama}*\n🔢 Stok: {stok} pcs\n📍 Lokasi: {lokasi}\n🗓️ Exp: {exp}", parse_mode='Markdown')
        else:
            await update.message.reply_text("Barang tidak ditemukan.")
    elif text.startswith("lokasi"):
        keyword = text.replace("lokasi", "").strip()
        info = get_product_info(keyword)
        if info:
            nama, _, lokasi, _ = info
            await update.message.reply_text(f"📍 *{nama}* ada di rak: {lokasi}", parse_mode='Markdown')
        else:
            await update.message.reply_text("Barang tidak ditemukan.")
    else:
        await update.message.reply_text("Perintah tidak dikenali. Coba ketik `stok [nama]` atau `lokasi [nama]`.")

if __name__ == '__main__':
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
