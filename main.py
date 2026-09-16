import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
SESSION = os.environ.get('SESSION', '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hola! Comandos:\n/grupos - Lista tus grupos\n/descargar ID CANTIDAD')

async def grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Buscando grupos...')
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    msg = ''
    async for dialog in client.iter_dialogs():
        msg += f'{dialog.id} | {dialog.name}\n'
        if len(msg) > 3000:
            await update.message.reply_text(msg)
            msg = ''
    if msg:
        await update.message.reply_text(msg)
    await client.disconnect()

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text('Uso: /descargar ID_GRUPO CANTIDAD')
        return
    grupo_id = int(context.args[0])
    limite = int(context.args[1])
    await update.message.reply_text(f'Descargando {limite} archivos...')
    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    await client.connect()
    count = 0
    async for msg in client.iter_messages(grupo_id, limit=limite):
        if msg.media:
            file = await client.download_media(msg, bytes)
            await update.message.reply_document(file)
            count += 1
    await client.disconnect()
    await update.message.reply_text(f'Listo! {count} archivos.')

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('grupos', grupos))
app.add_handler(CommandHandler('descargar', descargar))
app.run_polling()
