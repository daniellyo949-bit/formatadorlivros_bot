import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8639228499:AAEs5cBNaD6OhcHRVC9n81QpzWJfFCFTYec"

EXCECOES = {'de', 'do', 'da', 'dos', 'das', 'e', 'o', 'a', 'os', 'as', 'em', 'no', 'na', 'com', 'por', 'para', 'to'}

def title_case_br(texto):
    palavras = texto.lower().split()
    resultado = []
    for i, palavra in enumerate(palavras):
        if i == 0 or palavra not in EXCECOES:
            resultado.append(palavra.capitalize())
        else:
            resultado.append(palavra)
    return ' '.join(resultado)

def formatar(texto):
    texto = texto.strip()
    url_match = re.search(r'https?://\S+', texto)
    url = url_match.group(0) if url_match else ''
    sem_url = texto.replace(url, '').strip()
    match = re.match(r'^(.+?)\s+([\d,\.]+)', sem_url)
    if match:
        titulo = match.group(1).strip()
        preco = match.group(2).strip()
        resto = sem_url[match.end():].strip()
    else:
        titulo = sem_url.split('\n')[0].strip()
        preco = ''
        resto = sem_url[len(titulo):].strip()
    tropes = [t.strip() for t in re.split(r'[•\n]+', resto) if t.strip()]
    preco_str = f" - R$ {preco}" if preco else ''
    resultado = f"📖 {title_case_br(titulo)}{preco_str}\n"
    for t in tropes:
        resultado += f"{title_case_br(t)}\n"
    if url:
        resultado += f"🔗 {url}"
    return resultado.strip()

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    resposta = formatar(texto)
    await update.message.reply_text(resposta)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
print("Bot rodando...")
app.run_polling()
