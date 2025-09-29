import requests
import time
import feedparser
from deep_translator import GoogleTranslator
# Importe für die neue asynchrone Struktur (Version 21.x)
from telegram.ext import ApplicationBuilder, ContextTypes, JobQueue

# ⚡ Ersetze mit deinem Bot-Token und deiner Chat-ID
TOKEN = "8108666415:AAGCZTSnsMS0iF17KGneWdRaz3CqlpH7iUo"
# Die CHAT_ID muss eine gültige Ziel-ID sein (z.B. ein Kanal, eine Gruppe oder deine private ID)
CHAT_ID = "462822296"

# Globale Variable für den letzten Titel
last_title = ""

def get_gold_news():
    """
    Ruft den RSS-Feed ab, übersetzt die neueste Nachricht und gibt sie zurück,
    falls es sich um eine neue Nachricht handelt.
    """
    global last_title
    url = "https://www.kitco.com/rss/gold.xml"
    feed = feedparser.parse(url)

    if feed.entries:
        latest = feed.entries[0]
        title = latest.title
        summary = latest.summary if "summary" in latest else ""
        link = latest.link

        # Nur senden, wenn die Nachricht neu ist
        if title != last_title:
            last_title = title
            original_text = f"{title}\n\n{summary}"
            
            # Übersetzen von Auto zu Persisch (fa)
            try:
                translated_text = GoogleTranslator(source='auto', target='fa').translate(original_text)
            except Exception as e:
                print(f"Fehler bei der Übersetzung: {e}")
                translated_text = original_text # Sende den Originaltext als Fallback

            return f"📢 خبر جدید بازار طلا:\n\n{translated_text}\n\n🔗 منبع: {link}"

    return None

# NEUE ASYNCHRONE FUNKTION für die Job Queue
async def check_for_news(context: ContextTypes.DEFAULT_TYPE):
    """
    Diese Funktion wird regelmäßig von der Job Queue aufgerufen, um nach Neuigkeiten zu suchen.
    """
    news = get_gold_news()
    if news:
        print(f"Neue Nachricht gefunden: {news[:50]}...")
        # Die Nachricht an die vordefinierte CHAT_ID senden
        await context.bot.send_message(
            chat_id=CHAT_ID, 
            text=news, 
            parse_mode="HTML"
        )
    else:
        print("Keine neuen Nachrichten.")


def main():
    """
    Startet den Bot und richtet die periodische Aufgabe ein.
    """
    print("Starte Gold News Bot...")
    
    # 1. Anwendung erstellen
    application = ApplicationBuilder().token(TOKEN).build()

    # 2. Job Queue für periodische Aufgaben einrichten
    job_queue: JobQueue = application.job_queue
    
    # 3. Den Job planen: check_for_news alle 600 Sekunden (10 Minuten) ausführen
    job_queue.run_repeating(
        check_for_news, 
        interval=600, 
        first=1 # Erste Ausführung nach 1 Sekunde
    )

    # 4. Den Bot starten (Der Bot läuft jetzt im Hintergrund, der Webserver bleibt aktiv)
    # Da es sich um einen Bot ohne Nutzerinteraktion handelt, ist der Startvorgang minimal.
    application.run_polling() # 'run_polling' hält das Skript am Laufen und die Jobs aktiv.


if __name__ == '__main__':
    main()
