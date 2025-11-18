from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import requests

BOT_TOKEN = "8539755972:AAHyVupXMbJFtquIhpvehxjnX-gkVdgjErc"
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbyJpl0psuS1FRETtwVJSDKCJ4G0enBq4jvgyjDHBDxmfudMSskGhRfiRskosiNbbxBIvQ/exec"


# -------------------------
# /start
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Halo! 👋\n"
        "Kirim laporan keuangan dengan format:\n\n"
        "<b>Nama;Jenis Transaksi;Kategori;Jumlah;Metode Pembayaran;Catatan</b>\n\n"
        "Contoh:\n"
        "<i>Budi;Pengeluaran;Makan Siang;30000;Cash;Makan di luar</i>"
    )
    await update.message.reply_text(text, parse_mode="HTML")


# -------------------------
# Handler pesan masuk
# -------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()

        parts = [p.strip() for p in text.split(";")]  # Hilangkan spasi berlebih

        if len(parts) != 6:
            await update.message.reply_text(
                "❌ *Format salah!*\nGunakan:\n"
                "`Nama;Jenis Transaksi;Kategori;Jumlah;Metode Pembayaran;Catatan`",
                parse_mode="Markdown"
            )
            return

        data = {
            "pelapor": parts[0],
            "jenisTransaksi": parts[1],
            "kategori": parts[2],
            "jumlah": parts[3],
            "metodePembayaran": parts[4],
            "catatan": parts[5]
        }

        response = requests.post(WEBAPP_URL, json=data, timeout=10)

        if response.status_code == 200 and "Success" in response.text:
            await update.message.reply_text("Data berhasil dikirim ke Google Sheet ✅")
        else:
            await update.message.reply_text(
                "❌ Gagal mengirim ke Google Sheet.\n"
                "Pastikan WebApp sudah dideploy & akses publik."
            )

    except Exception as e:
        await update.message.reply_text(f"⚠ Error: {e}")


# -------------------------
# Main Program
# -------------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot sudah aktif...")
    app.run_polling()
