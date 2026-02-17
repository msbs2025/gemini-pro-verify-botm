"""Telegram bot command handlers with Bahasa Indonesia messages"""
import asyncio
import logging

from telegram import Update
from telegram.ext import ContextTypes

from verifier.sheerid import SheerIDVerifier
from database import Database

logger = logging.getLogger(__name__)

# Module-level database instance (set by bot.py)
db = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - welcome message in Bahasa Indonesia"""
    welcome_msg = (
        "🤖 Selamat datang di Bot Verifikasi Gemini!\n\n"
        "Bot ini membantu Anda memverifikasi akun Gemini One Pro menggunakan SheerID.\n\n"
        "Gunakan /help untuk melihat cara penggunaan."
    )
    await update.message.reply_text(welcome_msg)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command - usage instructions in Bahasa Indonesia"""
    help_msg = (
        "📖 Cara Penggunaan:\n\n"
        "/verify <link_sheerid> - Verifikasi akun Gemini One Pro\n\n"
        "Contoh:\n"
        "/verify https://services.sheerid.com/verify/...\n\n"
        "📝 Link SheerID harus mengandung parameter 'verificationId'\n"
        "⏳ Proses verifikasi membutuhkan waktu 1-2 menit\n"
        "✅ Dokumen akan disubmit ke SheerID untuk ditinjau"
    )
    await update.message.reply_text(help_msg)


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /verify command - main verification flow in Bahasa Indonesia"""
    # Parse arguments
    if not context.args:
        await update.message.reply_text(
            "❌ Format salah!\n\n"
            "Cara penggunaan: /verify <link_sheerid>\n\n"
            "Contoh:\n"
            "/verify https://services.sheerid.com/verify/..."
        )
        return
    
    url = context.args[0]
    
    # Parse verification ID from URL
    verification_id = SheerIDVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text(
            "❌ Link SheerID tidak valid.\n\n"
            "Pastikan link mengandung parameter 'verificationId'.\n\n"
            "Contoh link yang benar:\n"
            "https://services.sheerid.com/verify/...?verificationId=abc123"
        )
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text(
        f"⏳ Memproses verifikasi Gemini One Pro...\n\n"
        f"Verification ID: {verification_id}\n\n"
        "📝 Sedang menghasilkan data mahasiswa...\n"
        "🎨 Sedang membuat kartu mahasiswa PNG...\n"
        "📤 Sedang mengirim dokumen...\n\n"
        "Harap tunggu, proses ini membutuhkan 1-2 menit..."
    )
    
    # Run verification in background thread (httpx.Client is sync)
    try:
        verifier = SheerIDVerifier(verification_id)
        result = await asyncio.to_thread(verifier.verify)
        
        # Build result message based on verification outcome
        if result["success"]:
            result_msg = "✅ Verifikasi berhasil!\n\n"
            if result.get("pending"):
                result_msg += "✨ Dokumen telah disubmit ke SheerID\n"
                result_msg += "⏳ Menunggu peninjauan manual\n"
                result_msg += "⏱️ Estimasi waktu: beberapa menit\n\n"
            if result.get("redirect_url"):
                result_msg += f"🔗 Link redirect:\n{result['redirect_url']}"
            
            # Log success to database
            if db:
                db.add_verification(url, verification_id, "success", result["message"])
            
            await processing_msg.edit_text(result_msg)
        else:
            result_msg = (
                f"❌ Verifikasi gagal:\n\n"
                f"{result.get('message', 'Kesalahan tidak diketahui')}"
            )
            
            # Log failure to database
            if db:
                db.add_verification(url, verification_id, "failed", result["message"])
            
            await processing_msg.edit_text(result_msg)
    
    except Exception as e:
        logger.error(f"Verification error: {e}")
        error_msg = (
            f"❌ Terjadi kesalahan saat memproses verifikasi:\n\n"
            f"{str(e)}\n\n"
            "Silakan coba lagi nanti atau hubungi admin."
        )
        
        # Log error to database
        if db:
            db.add_verification(url, verification_id or "unknown", "error", str(e))
        
        await processing_msg.edit_text(error_msg)
