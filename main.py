from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
import json

app = Flask(__name__)

# TOKEN desde Railway
TOKEN = os.getenv("TELEGRAM_TOKEN")

# CARGAR JSON 
with open("temas_completos_formato2.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

# Crear aplicación Telegram
application = Application.builder().token(TOKEN).build()


# -

async def start(update, context):
    await update.message.reply_text(
        "Hola, soy tu Chatbot de Administracion de Proyectos.\n\n"
        "Escribe un número de tema (1–11) o una pregunta exacta."
    )


async def mensaje(update, context):
    texto = update.message.text.strip()

    # Si el usuario escribe un número de tema
    if texto in datos:
        preguntas = "\n".join([f"- {p}" for p in datos[texto].keys()])
        await update.message.reply_text(f"Preguntas del Tema {texto}:\n\n{preguntas}")
        return

    # Si el usuario escribe una pregunta
    for tema in datos.values():
        if texto in tema:
            await update.message.reply_text(tema[texto])
            return

    await update.message.reply_text("No encontré esa pregunta. Revisa que esté escrita igual.")


# Registrar comandos
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT, mensaje))


@app.post("/webhook")
def webhook():
    update_json = request.get_json(force=True)
    update = Update.de_json(update_json, application.bot)
    application.update_queue.put(update)
    return "ok", 200



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
