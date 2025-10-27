from flask import Flask, render_template, request, jsonify
import os
import sqlite3

app = Flask(__name__, template_folder="templates")

DB_PATH = "chatbot.db"

# --- Database setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT,
            reply TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB immediately (Flask 3.x compatible)
with app.app_context():
    init_db()

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user = data.get("user", "Guest")
    message = data.get("message", "")

    # Simple AI-like responses
    if "hello" in message.lower():
        reply = f"Hi {user}! How can I assist you today?"
    elif "book" in message.lower():
        reply = "Sure! Can you provide your email so we can confirm your schedule?"
    elif "price" in message.lower():
        reply = "Our pricing depends on your plan — would you like a free consultation?"
    else:
        reply = f"Thanks {user}, I received your message: '{message}'"

    # Save chat
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (user, message, reply) VALUES (?, ?, ?)", (user, message, reply))
    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
