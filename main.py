import schedule
import time
import requests
import json
import os
import random
import subprocess
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
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
    "NETLIFY": os.getenv("NETLIFY"),
    "AFFILIATE_LINK": os.getenv("AFFILIATE_LINK")
}

# --- 🌐 KEEP-ALIVE SERVER ---
app = Flask('')
@app.route('/')
def home(): return "AI-CEO Multi-Revenue System is Online 24/7"
def run_flask(): app.run(host='0.0.0.0', port=8080)

# --- 🧠 OMNI-BRAIN (Sales, SEO & Affiliate Logic) ---
def get_ai_response(msg, task="sales"):
    headers = {"Authorization": f"Bearer {KEYS['OPENROUTER']}"}
    
    if task == "sales":
        prompt = (f"User: '{msg}'. You are an All-Rounder Digital Entrepreneur. "
                  f"1. Sell ₹499 SaaS. 2. Negotiate Custom Apps for ₹4999. "
                  f"3. Pitch affiliate link if relevant: {KEYS['AFFILIATE_LINK']}. "
                  "Use Hinglish, be a master closer. Tell them link in bio.")
    elif task == "seo":
        prompt = "Create a viral 'Make Money Online' landing page HTML/CSS. ONLY CODE."

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, 
                            data=json.dumps({"model": "openai/gpt-4o", "messages": [{"role": "user", "content": prompt}]}))
        return res.json()['choices'][0]['message']['content']
    except: return "Bhai, bio check karo sab details wahan hain! 🔥"

# --- 🛰️ TELEGRAM LOGGING ---
def log_tele(msg):
    try: requests.post(f"https://api.telegram.org/bot{KEYS['TELEGRAM_TOKEN']}/sendMessage", 
                      json={"chat_id": KEYS['TELEGRAM_CHAT_ID'], "text": f"🔱 OMNI-EMPIRE: {msg}"})
    except: pass

# --- 🛠️ PASSIVE REVENUE: NETLIFY DEPLOYER ---
def deploy_to_netlify():
    try:
        blog_code = get_ai_response("", task="seo")
        with open("index.html", "w") as f: f.write(blog_code)
        os.environ["NETLIFY_AUTH_TOKEN"] = KEYS['NETLIFY']
        # Note: Requires netlify-cli to be installed via requirements or workflow
        subprocess.run(["npx", "netlify-cli", "deploy", "--prod", "--dir=."], input='y', text=True)
        log_tele("🌐 New SEO Landing Page Deployed to Netlify.")
    except Exception as e: print(f"Netlify Error: {e}")

# --- 🏰 OMNI-REVENUE CYCLE ---
def run_omni_cycle(cl):
    try:
        # 1. Direct Message & Sales
        for thread in cl.direct_threads():
            if thread.unread_count > 0:
                last_msg = thread.messages[0]
                if last_msg.item_type == 'text':
                    reply = get_ai_response(last_msg.text, task="sales")
                    cl.direct_answer(thread.id, reply)
                elif last_msg.item_type == 'media':
                    log_tele(f"💰 New Payment Proof from @{thread.users[0].username}!")
                time.sleep(random.randint(5, 10))

        # 2. Competitor Mining & Growth
        target_tags = ["startupindia", "coding", "entrepreneur"]
        tag = random.choice(target_tags)
        medias = cl.hashtag_medias_recent(tag, amount=3)
        for m in medias:
            cl.user_stories(m.user.pk) # Story views for traffic
            if random.random() > 0.8: cl.user_follow(m.user.pk) # Targeted follow
            time.sleep(random.randint(10, 20))
            
    except Exception as e: print(f"Cycle Error: {e}")

def main():
    cl = Client()
    cl.set_user_agent("Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
    try:
        cl.login(KEYS['IG_USER'], KEYS['IG_PASS'])
        log_tele("🔱 ALL-ROUNDER AI-CEO LIVE ON CLOUD.\nSaaS, Affiliate, & SEO Engines Active.")
    except: return

    # Scheduling
    schedule.every(3).minutes.do(lambda: run_omni_cycle(cl))
    schedule.every().day.at("12:00").do(deploy_to_netlify) # Roz ek SEO site
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    main()
                
