import schedule, time, requests, json, os, random, sqlite3, subprocess
from instagrapi import Client
from datetime import datetime

# --- 👑 ALL-IN-ONE CONFIGURATION ---
def get_key(key_name):
    return os.getenv(key_name)

KEYS = {
    "OPENROUTER": get_key("OPENROUTER"),
    "PEXELS": get_key("PEXELS_API_KEY"),
    "IG_USER": "uzumakilabs",
    "IG_PASS": "13643211097013",
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
    c.execute('''CREATE TABLE IF NOT EXISTS memory (username TEXT PRIMARY KEY, history TEXT)''')
    conn.commit()
    conn.close()

# --- 🧠 BRAIN LOGIC ---
def supreme_ai_decision(username, message):
    try:
        headers = {"Authorization": f"Bearer {KEYS['OPENROUTER']}"}
        prompt = f"Client @{username}: {message}. Close ₹4999 deal in Hinglish."
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, 
                            json={"model": "google/gemini-pro", "messages": [{"role": "user", "content": prompt}]}).json()
        return res['choices'][0]['message']['content']
    except: return "Bhai, thoda system load ho raha hai. Line pe raho!"

# --- 🏰 EMPIRE CYCLE ---
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

# --- 🚀 MASTER IGNITION (IP & PASSWORD FIX) ---
def main():
    print("🚀 IGNITION SEQUENCE STARTED...")
    init_db()
    cl = Client()
    
    # Naya Agent taaki IP blacklisting ka asar kam ho
    cl.set_user_agent("Instagram 282.0.0.22.119 Android (13/33; 440dpi; 1080x2340; samsung; SM-S901B; qcom; en_GB; 468305018)")

    try:
        session_file = "session.json"
        if os.path.exists(session_file):
            print("🔄 Loading existing session...")
            cl.load_settings(session_file)
            cl.login(KEYS['IG_USER'], KEYS['IG_PASS'])
        else:
            print(f"🔐 New Login attempt for {KEYS['IG_USER']}...")
            cl.login(KEYS['IG_USER'], KEYS['IG_PASS'])
            cl.dump_settings(session_file)
        
        notify("🔱 SYSTEM ONLINE. CEO is in the office!")
        
    except Exception as e:
        error_msg = str(e)
        if "password" in error_msg.lower():
            notify("❌ PASSWORD INCORRECT: Bhai, ek baar manual login karke password reset ya check karo.")
        elif "blacklist" in error_msg.lower() or "proxy" in error_msg.lower():
            notify("⚠️ IP BLACKLISTED: GitHub ka IP block hai. 30 min ruko ya manual check karo.")
        else:
            notify(f"❌ LOGIN FAILED: {error_msg}")
        return

    schedule.every(2).minutes.do(lambda: manage_empire(cl))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
    
