import schedule, time, requests, json, os, random, sqlite3, subprocess
from instagrapi import Client
from datetime import datetime
from threading import Thread

# --- 👑 AUTOMATIC KEY LOADER (CRITICAL FIX) ---
def get_key(key_name):
    val = os.getenv(key_name)
    if not val:
        print(f"⚠️ Warning: {key_name} is missing in GitHub Secrets!")
    return val

KEYS = {
    "OPENROUTER": get_key("OPENROUTER"),
    "PEXELS": get_key("PEXELS_API_KEY"),
    "IG_USER": get_key("IG_USER"),
    "IG_PASS": get_key("IG_PASS"),
    "TELEGRAM_TOKEN": get_key("TELEGRAM_TOKEN"),
    "TELEGRAM_CHAT_ID": get_key("TELEGRAM_CHAT_ID"),
    "CASHFREE_ID": get_key("CASHFREE_ID"),
    "CASHFREE_SECRET": get_key("CASHFREE_SECRET")
}

# --- 📡 NOTIFICATION ENGINE ---
def notify(msg):
    print(f"📡 LOG: {msg}") # GitHub logs mein dikhega
    try:
        url = f"https://api.telegram.org/bot{KEYS['TELEGRAM_TOKEN']}/sendMessage"
        payload = {"chat_id": KEYS['TELEGRAM_CHAT_ID'], "text": f"🔱 CEO-LOG:\n{msg}"}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"❌ Telegram Failed: {e}")

# --- 🗄️ DATABASE SYSTEM ---
def init_db():
    try:
        conn = sqlite3.connect('agency_empire.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS memory 
                     (username TEXT PRIMARY KEY, history TEXT, sentiment INTEGER, total_spent REAL, last_interaction TEXT)''')
        conn.commit()
        conn.close()
        print("✅ Database Initialized.")
    except Exception as e:
        print(f"❌ DB Error: {e}")

# --- 💸 PAYMENT SYSTEM ---
def get_payment_link(username):
    headers = {
        "x-client-id": KEYS["CASHFREE_ID"],
        "x-client-secret": KEYS["CASHFREE_SECRET"],
        "x-api-version": "2023-08-01",
        "Content-Type": "application/json"
    }
    data = {
        "order_id": f"REV_{int(time.time())}",
        "order_amount": 4999.00,
        "order_currency": "INR",
        "customer_details": {"customer_id": username, "customer_phone": "9999999999"}
    }
    try:
        res = requests.post("https://api.cashfree.com/pg/orders", headers=headers, json=data).json()
        return f"https://www.cashfree.com/checkout/pay/{res['payment_session_id']}"
    except: return None

# --- 🧠 BRAIN & DECISION ---
def supreme_ai_decision(username, message):
    try:
        headers = {"Authorization": f"Bearer {KEYS['OPENROUTER']}"}
        prompt = f"Customer @{username} said: {message}. Goal: Sell ₹4999 AI Agency service in Hinglish."
        
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, 
                            json={"model": "google/gemini-pro", "messages": [{"role": "user", "content": prompt}]}, timeout=20).json()
        
        reply = res['choices'][0]['message']['content']
        score = 2 if any(x in message.lower() for x in ["price", "buy", "interested"]) else 0
        
        if score >= 2:
            link = get_payment_link(username)
            if link: reply += f"\n\n🔥 Payment Link: {link}"
            
        return reply, score
    except Exception as e:
        return f"Bhai thoda wait karo, system load ho raha hai. (Err: {e})", 0

# --- 🏰 THE EMPIRE ENGINE ---
def manage_empire(cl):
    now = datetime.now()
    print(f"🔄 Cycle Start: {now.strftime('%H:%M:%S')}")
    try:
        # DM Response Logic
        threads = cl.direct_threads()
        for thread in threads:
            if thread.unread_count > 0:
                user = thread.users[0].username
                msg = thread.messages[0].text
                print(f"📩 New Message from @{user}: {msg}")
                
                reply, _ = supreme_ai_decision(user, msg)
                cl.direct_answer(thread.id, reply)
                notify(f"✅ Replied to @{user}")

    except Exception as e:
        notify(f"⚠️ Cycle Warning: {e}")

# --- 🚀 MASTER IGNITION ---
def main():
    print("🚀 IGNITION SEQUENCE STARTED...")
    init_db()
    
    cl = Client()
    # Bypass settings
    cl.set_user_agent("Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
    
    try:
        print(f"🔐 Attempting Login for {KEYS['IG_USER']}...")
        cl.login(KEYS['IG_USER'], KEYS['IG_PASS'])
        notify("🔱 SYSTEM ARMORED & ONLINE. CEO is in the office.")
    except Exception as e:
        error_msg = f"❌ LOGIN FAILED: {str(e)}"
        print(error_msg)
        # Is message ko Telegram par bhejte hain bina notify function ke (for safety)
        requests.post(f"https://api.telegram.org/bot{KEYS['TELEGRAM_TOKEN']}/sendMessage", 
                      json={"chat_id": KEYS['TELEGRAM_CHAT_ID'], "text": error_msg})
        return

    # Automation Schedule
    schedule.every(2).minutes.do(lambda: manage_empire(cl))
    
    print("⚙️ Automation Engine: RUNNING")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as fatal:
        print(f"💀 FATAL SYSTEM CRASH: {fatal}")
    
