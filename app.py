from flask import Flask, render_template, request, jsonify
import os
import sqlite3

app = Flask(__name__, template_folder="templates")

DB_PATH = "chatbot.db"

# --- DB setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT,
            reply TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB on start (Flask 3.x safe)
with app.app_context():
    init_db()

# --- Routes ---
@app.route("/")
def home():
    # homepage -> renders the UI
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user = (data.get("user") or "Guest").strip()
    message = (data.get("message") or "").strip()

    # simple AI-like rules
    text = message.lower()
    if "hello" in text or "hi" in text:
        reply = f"Hi {user}! How can I assist you today?"
    elif "book" in text or "schedule" in text:
        reply = "Sure! Can you provide your email so we can confirm your schedule?"
    elif "price" in text or "pricing" in text:
        reply = "Our pricing depends on your plan — want a free consultation?"
    else:
        reply = f"Thanks {user}, I received your message: '{message}'."

    # save conversation
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (user, message, reply) VALUES (?, ?, ?)",
        (user, message, reply),
    )
    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Render sets $PORT — fall back to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
