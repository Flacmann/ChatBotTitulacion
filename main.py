from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
import json

app = Flask(__name__)

# TOKEN desde Railway
TOKEN = os.getenv("TELEGRAM_TOKEN")

# CARGAR JSON
with open("temas_completos_formato2.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

# Crear aplicación Telegram
application = ApplicationBuilder().token(TOKEN).build()


# ---------------- HANDLERS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola, soy tu Chatbot de Administración de Proyectos.\n\n"
        "Escribe un número de tema (1–11) o una pregunta exacta."
    )


async def mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()

    # Tema número
    if texto in datos:
        preguntas = "\n".join([f"- {p}" for p in datos[texto].keys()])
        await update.message.reply_text(f"Preguntas del Tema {texto}:\n\n{preguntas}")
        return

    # Pregunta literal
    for tema in datos.values():
        if texto in tema:
            await update.message.reply_text(tema[texto])
            return

    await update.message.reply_text("No encontré esa pregunta. Revisa que esté escrita igual.")


# Registrar handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT, mensaje))



@app.post("/webhook")
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok", 200



if __name__ == "__main__":
    # Run Flask (Railway)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
