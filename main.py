import schedule
import time
import requests
import json
import os
import random
from instagrapi import Client
from datetime import datetime
from flask import Flask
from threading import Thread

# --- 👑 CONFIGURATION FROM GITHUB SECRETS ---
KEYS = {
    "OPENROUTER": os.getenv("OPENROUTER"),
    "CASHFREE_ID": os.getenv("CASHFREE_ID"),
    "CASHFREE_SECRET": os.getenv("CASHFREE_SECRET"),
    "IG_USER": os.getenv("IG_USER"),
    "IG_PASS": os.getenv("IG_PASS"),
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID")
}

# --- 🌐 KEEP-ALIVE SERVER ---
app = Flask('')
@app.route('/')
def home(): return "AI-CEO is Running 24/7"
def run_flask(): app.run(host='0.0.0.0', port=8080)

# --- 🧠 AI SALES BRAIN ---
def get_ai_response(msg):
    headers = {"Authorization": f"Bearer {KEYS['OPENROUTER']}"}
    prompt = f"User said: '{msg}'. Respond in Hinglish. Sell our SaaS (₹499) or Custom App (₹4999). Tell them to check Bio link and DM screenshot."
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, 
                            data=json.dumps({"model": "openai/gpt-4o", "messages": [{"role": "user", "content": prompt}]}))
        return res.json()['choices'][0]['message']['content']
    except: return "Bhai, bio link check karo aur payment ke baad screenshot bhejo! 🔥"

# --- 🏰 OMNI-REVENUE CYCLE ---
def run_cycle(cl):
    try:
        # Handle DMs
        for thread in cl.direct_threads():
            if thread.unread_count > 0:
                last_msg = thread.messages[0]
                if last_msg.item_type == 'text':
                    cl.direct_answer(thread.id, get_ai_response(last_msg.text))
                elif last_msg.item_type == 'media':
                    requests.post(f"https://api.telegram.org/bot{KEYS['TELEGRAM_TOKEN']}/sendMessage", 
                                  json={"chat_id": KEYS['TELEGRAM_CHAT_ID'], "text": f"💰 Payment Proof from @{thread.users[0].username}!"})
        
        # Human-like Interaction (Growth)
        tag = random.choice(["startupindia", "coding", "business"])
        medias = cl.hashtag_medias_recent(tag, amount=2)
        for m in medias:
            cl.user_stories(m.user.pk) # Watch stories
            time.sleep(random.randint(5, 10))
            
    except Exception as e: print(f"Error: {e}")

def main():
    cl = Client()
    cl.set_user_agent("Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
    try:
        cl.login(KEYS['IG_USER'], KEYS['IG_PASS'])
        requests.post(f"https://api.telegram.org/bot{KEYS['TELEGRAM_TOKEN']}/sendMessage", 
                      json={"chat_id": KEYS['TELEGRAM_CHAT_ID'], "text": "🔱 AI-CEO LIVE ON CLOUD 24/7"})
    except: return

    schedule.every(3).minutes.do(lambda: run_cycle(cl))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    main()
  
