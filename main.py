import schedule, time, requests, json, os, random, sqlite3, subprocess
from instagrapi import Client
from datetime import datetime
from threading import Thread

# --- 👑 AUTOMATIC KEY LOADER ---
def get_key(key_name):
    val = os.getenv(key_name)
    if not val: print(f"⚠️ Warning: {key_name} is missing!")
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
    print(f"📡 LOG: {msg}")
    try:
        url = f"https://api.telegram.org/bot{KEYS['TELEGRAM_TOKEN']}/sendMessage"
        requests.post(url, json={"chat_id": KEYS['TELEGRAM_CHAT_ID'], "text": f"🔱 CEO-LOG:\n{msg}"}, timeout=10)
    except: pass

# --- 🗄️ DATABASE SYSTEM ---
def init_db():
    conn = sqlite3.connect('agency_empire.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory 
                 (username TEXT PRIMARY KEY, history TEXT, sentiment INTEGER, total_spent REAL, last_interaction TEXT)''')
    conn.commit()
    conn.close()

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
        return reply
    except: return "Bhai thoda wait karo, system load ho raha hai."

# --- 🏰 THE EMPIRE ENGINE ---
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
    except Exception as e: print(f"Cycle Err: {e}")

# --- 🚀 MASTER IGNITION (CSRF BYPASS ENABLED) ---
def main():
    print("🚀 IGNITION SEQUENCE STARTED...")
    init_db()
    cl = Client()
    cl.set_user_agent("Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
    
    try:
        print("⏳ Fetching CSRF tokens...")
        cl.get_timeline_feed() 
        time.sleep(random.randint(5, 10)) 
        
        print(f"🔐 Login attempt for {KEYS['IG_USER']}...")
        cl.login(KEYS['IG_USER'], KEYS['IG_PASS'])
        cl.dump_settings("session.json")
        notify("🔱 SYSTEM ARMORED & ONLINE. CEO is in the office.")
        
    except Exception as e:
        error_msg = str(e)
        if "CSRF" in error_msg:
            notify("⚠️ CSRF Detected. Sleeping 30s for Bypass...")
            time.sleep(30)
            try:
                cl.login(KEYS['IG_USER'], KEYS['IG_PASS'], relogin=True)
                notify("🔱 SYSTEM ONLINE (CSRF Bypassed)!")
            except:
                notify(f"❌ LOGIN FAILED: {error_msg}\nTip: Mobile app par 'This was me' confirm karo.")
        else:
            notify(f"❌ LOGIN FAILED: {error_msg}")
        return

    schedule.every(2).minutes.do(lambda: manage_empire(cl))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
    
