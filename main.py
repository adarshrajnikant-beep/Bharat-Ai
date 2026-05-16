import schedule, time, requests, json, os, random, sqlite3, subprocess
from instagrapi import Client
from datetime import datetime
from threading import Thread

# --- 👑 ALL-IN-ONE CONFIGURATION ---
KEYS = {
    "OPENROUTER": os.getenv("OPENROUTER"),
    "PEXELS": os.getenv("PEXELS_API_KEY"),
    "IG_USER": "uzumakilabs",
    "IG_PASS": "13643211097013",
    "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
    "CASHFREE_ID": os.getenv("CASHFREE_ID"),
    "CASHFREE_SECRET": os.getenv("CASHFREE_SECRET")
}

# --- 📡 NOTIFICATION ENGINE ---
def notify(msg):
    print(f"📡 LOG: {msg}")
    try:
        url = f"https://api.telegram.org/bot{KEYS['TELEGRAM_TOKEN']}/sendMessage"
        requests.post(url, json={"chat_id": KEYS['TELEGRAM_CHAT_ID'], "text": f"🔱 CEO-LOG:\n{msg}"}, timeout=10)
    except: pass

# --- 🗄️ INFINITE MEMORY & ML DATA ---
def init_db():
    conn = sqlite3.connect('agency_empire.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory 
                 (username TEXT PRIMARY KEY, history TEXT, sentiment INTEGER, total_spent REAL, last_interaction TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS neural_weights (key TEXT PRIMARY KEY, value REAL)''')
    c.execute("INSERT OR IGNORE INTO neural_weights VALUES ('scarcity', 0.5), ('politeness', 0.5)")
    conn.commit()
    conn.close()

# --- 💸 REVENUE & PAYMENT (Cashfree) ---
def get_payment_link(username):
    headers = {
        "x-client-id": KEYS["CASHFREE_ID"],
        "x-client-secret": KEYS["CASHFREE_SECRET"],
        "x-api-version": "2023-08-01",
        "Content-Type": "application/json"
    }
    try:
        data = {
            "order_id": f"REV_{int(time.time())}", 
            "order_amount": 4999.00, "order_currency": "INR",
            "customer_details": {"customer_id": username, "customer_phone": "9999999999"}
        }
        res = requests.post("https://api.cashfree.com/pg/orders", headers=headers, json=data).json()
        return f"https://www.cashfree.com/checkout/pay/{res['payment_session_id']}"
    except: return None

# --- 🧠 THE BRAIN (AI Reasoning) ---
def supreme_ai_decision(username, message):
    try:
        score = 2 if any(x in message.lower() for x in ["buy", "price", "how", "interested", "kitna", "paisa"]) else 0
        prompt = f"User @{username}. Msg: {message}. Goal: Sell ₹4999 AI Agency service in Hinglish."
        
        headers = {"Authorization": f"Bearer {KEYS['OPENROUTER']}"}
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, 
                            json={"model": "google/gemini-pro", "messages": [{"role": "user", "content": prompt}]}, timeout=20).json()
        reply = res['choices'][0]['message']['content']
        
        if score >= 2:
            link = get_payment_link(username)
            if link: reply += f"\n\n🔥 Order Link: {link}"
        return reply
    except: return "Bhai thoda wait karo, system load ho raha hai! 🔱"

# --- 🏰 THE UNSTOPPABLE CYCLE ---
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
    except Exception as e: print(f"Cycle Error: {e}")

# --- 🚀 MASTER IGNITION (FIXED LOGIN) ---
def main():
    print("🚀 IGNITION SEQUENCE STARTED...")
    init_db()
    cl = Client()
    cl.set_user_agent("Instagram 282.0.0.22.119 Android (13/33; 440dpi; 1080x2340; samsung; SM-S901B; qcom; en_GB; 468305018)")

    try:
        # Step 1: Session Check
        if os.path.exists("session.json"):
            cl.load_settings("session.json")
        
        # Step 2: Safe Login
        print(f"🔐 Attempting Login for {KEYS['IG_USER']}...")
        cl.login(KEYS['IG_USER'], KEYS['IG_PASS'])
        cl.dump_settings("session.json")
        notify("🔱 SYSTEM ARMORED & ONLINE. CEO is in the office.")
        
    except Exception as e:
        error_msg = str(e)
        if "password" in error_msg.lower():
            notify("⚠️ IG Security Triggered! Phone mein 'Settings > Login Activity' jaakar 'This was me' confirm karo.")
        else:
            notify(f"❌ LOGIN FAILED: {error_msg}")
        
        # Don't crash, stay alive to retry
        time.sleep(600)
        return

    # Automation Loop
    schedule.every(2).minutes.do(lambda: manage_empire(cl))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
        
