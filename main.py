import schedule, time, requests, json, os, random, sqlite3
from instagrapi import Client
from datetime import datetime

# --- 👑 ALL-IN-ONE CONFIGURATION ---
def get_key(key_name, default=""):
    return os.getenv(key_name, default)

KEYS = {
    "OPENROUTER": get_key("OPENROUTER"),
    "PEXELS": get_key("PEXELS_API_KEY"),
    "IG_USER": "uzumakilabs",
    "IG_PASS": "adarsh848210",
    "TELEGRAM_TOKEN": get_key("TELEGRAM_TOKEN"),
    "TELEGRAM_CHAT_ID": get_key("TELEGRAM_CHAT_ID"),
    "CASHFREE_ID": get_key("CASHFREE_ID"),
    "CASHFREE_SECRET": get_key("CASHFREE_SECRET")
}

def notify(msg):
    print(f"📡 LOG: {msg}")
    try:
        url = f"https://api.telegram.org/bot{KEYS['TELEGRAM_TOKEN']}/sendMessage"
        requests.post(url, json={"chat_id": KEYS['TELEGRAM_CHAT_ID'], "text": f"🔱 CEO-LOG:\n{msg}"}, timeout=10)
    except: pass

def init_db():
    conn = sqlite3.connect('agency_empire.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory 
                 (username TEXT PRIMARY KEY, history TEXT, sentiment INTEGER, total_spent REAL, last_interaction TEXT)''')
    conn.commit()
    conn.close()

# --- 🧠 AI BRAIN ---
def supreme_ai_decision(username, message):
    try:
        headers = {"Authorization": f"Bearer {KEYS['OPENROUTER']}"}
        prompt = f"Customer @{username} said: {message}. Goal: Sell ₹4999 AI Agency service in Hinglish."
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, 
                            json={"model": "google/gemini-pro", "messages": [{"role": "user", "content": prompt}]}, timeout=20).json()
        return res['choices'][0]['message']['content']
    except: return "Bhai thoda wait karo, details bhej raha hoon. 🔱"

# --- 🏰 EMPIRE ENGINE ---
def manage_empire(cl):
    try:
        threads = cl.direct_threads()
        for thread in threads:
            if thread.unread_count > 0:
                user = thread.users[0].username
                msg = thread.messages[0].text
                reply = supreme_ai_decision(user, msg)
                cl.direct_answer(thread.id, reply)
                notify(f"✅ Replied to @{user}")
    except Exception as e: 
        print(f"Cycle Error: {e}")

# --- 🚀 MASTER IGNITION (FIXED FOR PHONE/GITHUB) ---
def main():
    print("🚀 IGNITION SEQUENCE STARTED...")
    init_db()
    cl = Client()
    
    # Naya Agent taaki block na ho
    cl.set_user_agent("Instagram 282.0.0.22.119 Android (13/33; 440dpi; 1080x2340; samsung; SM-S901B; qcom; en_GB; 468305018)")

    try:
        # Step 1: Check for Session
        if os.path.exists("session.json"):
            print("💾 Loading Session...")
            cl.load_settings("session.json")
        
        # Step 2: Login
        print(f"🔐 Attempting Login for {KEYS['IG_USER']}...")
        cl.login(KEYS['IG_USER'], KEYS['IG_PASS'])
        cl.dump_settings("session.json")
        notify("🔱 SYSTEM ONLINE. Empire is LIVE!")
        
    except Exception as e:
        error_msg = str(e)
        if "challenge" in error_msg.lower():
            notify("⚠️ CHALLENGE DETECTED: Phone par IG kholo aur 'It was me' confirm karo.")
        elif "password" in error_msg.lower():
            notify("❌ LOGIN FAIL: Password check karo ya IG App se login karke confirm karo.")
        else:
            notify(f"❌ ERROR: {error_msg}")
        return

    # Automation Loop
    schedule.every(2).minutes.do(lambda: manage_empire(cl))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
    
