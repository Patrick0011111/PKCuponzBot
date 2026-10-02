import os
import time
import json
import hashlib
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SHOPEE_APP_ID = os.getenv("SHOPEE_APP_ID")
SHOPEE SECRET = os.getenv("SHOPEE_SECRET")
SHOPEE_API_URL = "https://open-api.affiliate.shopee.com.br/graphql"



def gerar_link_afiliado(url):
    query = """
    mutation generateShortLink($input: ShortLinkInput!) {
        generateShortLink(input: $input) {
            shortLink
        }
    }
    """

    body = {
        "query": query,
        "variables": {
            "input": {
                "originUrl": url
            }
        }
    }

    payload = json.dumps(body, separators=(",", ":"))
    timestamp = int(time.time())

    assinatura = hashlib.sha256(
        f"{SHOPEE_APP_ID}{timestamp}{payload}{SHOPEE_SECRET}".encode()
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "Authorization": (
            f"SHA256 Credential={SHOPEE_APP_ID}, "
            f"Timestamp={timestamp}, Signature={assinatura}"
        )
    }

    resposta = requests.post(
        SHOPEE_API_URL,
        data=payload,
        headers=headers,
        timeout=30
    )

    dados = resposta.json()

    if dados.get("errors"):
        raise Exception(dados["errors"][0]["message"])

    return dados["data"]["generateShortLink"]["shortLink"]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bem-vindo ao PK Cuponz!\n\n"
        "Envie o link de um produto da Shopee e eu vou gerar seu link de desconto."
    )


async def receber_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message.text.strip()

    try:
        link_afiliado = gerar_link_afiliado(mensagem)

        await update.message.reply_text(
            f"🔥 Seu link de afiliado:\n\n{link_afiliado}"
        )

    except Exception as erro:
        print(f"Erro ao gerar link: {erro}")

        await update.message.reply_text(
            "❌ Não consegui converter esse link. Confira se é um link válido da Shopee e tente novamente."
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
