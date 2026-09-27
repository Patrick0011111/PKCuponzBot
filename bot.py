import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = "8959162571:AAHZjB_QgHfvno51-Qc30mclv5zmdN51qDY"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bem-vindo ao PK Cuponz!\n\n"
        "Envie o link de um produto da Shopee e eu vou gerar seu link de desconto."
    )


async def receber_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message.text

    await update.message.reply_text(
        f"🔎 Recebi seu link:\n\n{mensagem}\n\n"
        "Processando..."
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receber_link)
    )

    print("PK Cuponz Bot online!")

    app.run_polling()


if __name__ == "__main__":
    main()
