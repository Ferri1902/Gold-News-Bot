import requests
import imghdr
from telegram import Bot
import time
import feedparser
from deep_translator import GoogleTranslator

# ⚡ جایگزین با توکن ربات و چت‌آیدی خودت
TOKEN = "8108666415:AAGCZTSnsMS0iF17KGneWdRaz3CqlpH7iUo"
CHAT_ID = "462822296"

bot = Bot(token=TOKEN)

last_title = ""  # برای جلوگیری از ارسال تکراری

def get_gold_news():
    global last_title
    url = "https://www.kitco.com/rss/gold.xml"
    feed = feedparser.parse(url)

    if feed.entries:
        latest = feed.entries[0]
        title = latest.title
        summary = latest.summary if "summary" in latest else ""
        link = latest.link

        # فقط وقتی خبر جدید باشه
        if title != last_title:
            last_title = title
            original_text = f"{title}\n\n{summary}"
            translated_text = GoogleTranslator(source='auto', target='fa').translate(original_text)
            return f"📢 خبر جدید بازار طلا:\n\n{translated_text}\n\n🔗 منبع: {link}"

    return None

while True:
    news = get_gold_news()
    if news:
        bot.send_message(chat_id=CHAT_ID, text=news, parse_mode="HTML")
    time.sleep(600)  # هر 10 دقیقه یک بار بررسی
