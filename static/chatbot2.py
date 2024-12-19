from flask import Flask, request, jsonify, render_template
from chatbot import fetch_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({"response": "Please send a POST request with your query."})

    user_query = request.json.get('query')
    response = fetch_response(user_query)
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)


#//Chatbot.py//


import sqlite3

# Create database and tables
conn = sqlite3.connect('faq.db')
cursor = conn.cursor()

# Create FAQs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS FAQs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    keywords TEXT,
    answer TEXT
)
''')

# Create Logs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    response TEXT,
    timestamp TEXT
)
''')

conn.commit()
conn.close()
def populate_faq():
    faqs = [
        ("What is the return policy?", "return,refund", "Our return policy lasts for 30 days."),
        ("How can I reset my password?", "reset,password", "Click on 'Forgot Password' on the login page."),
        ("Where is my order?", "order,status", "You can track your order in the 'My Orders' section."),
        ("What payment methods do you accept?", "payment,methods", "We accept credit cards, PayPal, and bank transfers."),
        ("How do I contact customer support?", "contact,support", "You can contact customer support via email or our 24/7 chat service."),
        ("Do you ship internationally?", "ship,international", "Yes, we ship to over 100 countries worldwide."),
        ("How can I cancel my order?", "cancel,order", "You can cancel your order within 24 hours from the 'My Orders' section."),
        ("Are my personal details secure?", "secure,privacy", "Yes, we use advanced encryption to protect your personal information."),
        ("How do I update my account details?", "update,account", "You can update your details in the 'Account Settings' section."),
        ("What are your delivery times?", "delivery,shipping", "Delivery times vary by location, typically 5-7 business days."),
        ("How can I apply a discount code?", "discount,code", "Enter the discount code at checkout to apply it."),
        ("What happens if I receive a damaged item?", "damaged,item", "Contact customer support within 48 hours to arrange a replacement."),
        ("Do you offer gift wrapping?", "gift,wrapping", "Yes, you can select gift wrapping at checkout."),
        ("Can I change my delivery address after placing an order?", "change,address", "You can change your address within 12 hours from 'My Orders'.")
    ]
    conn = sqlite3.connect('faq.db')
    cursor = conn.cursor()

    for question, keywords, answer in faqs:
        cursor.execute("INSERT INTO FAQs (question, keywords, answer) VALUES (?, ?, ?)",
                       (question, keywords, answer))

    conn.commit()
    conn.close()

populate_faq()

import sqlite3
import datetime

def fetch_response(user_query):
    conn = sqlite3.connect('faq.db')
    cursor = conn.cursor()

    if any(keyword.lower() in user_query.lower() for keyword in keyword_list):
            log_interaction(user_query, answer)
            return answer
 # Fetch FAQs
    cursor.execute("SELECT question, keywords, answer FROM FAQs")
    faqs = cursor.fetchall()

    for question, keywords, answer in faqs:
        keyword_list = keywords.split(',')
    
    # Default response for unsupported queries
    fallback_response = "I'm sorry, I couldn't understand your query. Please contact support."
    log_interaction(user_query, fallback_response)
    return fallback_response

def log_interaction(query, response):
    conn = sqlite3.connect('faq.db')
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO Logs (query, response, timestamp) VALUES (?, ?, ?)",
                   (query, response, timestamp))
    conn.commit()
    conn.close()


### index.html ###

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot UI</title>
    <link rel="stylesheet" href="/static/styles.css"> <!-- Optional -->
</head>
<body>
    <h1>Chat with our Bot</h1>
    <div id="chatbox">
        <div id="chat-log"></div>
        <input type="text" id="user-input" placeholder="Type your message here..." />
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        function sendMessage() {
            const userInput = document.getElementById('user-input').value;
            const chatLog = document.getElementById('chat-log');

            if (!userInput.trim()) return;

            // Display user message
            chatLog.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

            // Send message to backend
            fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: userInput })
            })
            .then(response => response.json())
            .then(data => {
                // Display bot response
                chatLog.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
                document.getElementById('user-input').value = ''; // Clear input
            })
            .catch(error => {
                chatLog.innerHTML += `<p><strong>Bot:</strong> Sorry, an error occurred.</p>`;
                console.error('Error:', error);
            });
        }
    </script>
</body>
</html>


#### styles.css ###

body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f4f4f9;
}

h1 {
    text-align: center;
}

#chatbox {
    max-width: 600px;
    margin: 20px auto;
    background: white;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

#chat-log {
    height: 300px;
    overflow-y: auto;
    margin-bottom: 10px;
    padding: 10px;
    border: 1px solid #ddd;
    background: #f9f9f9;
    border-radius: 4px;
}

#user-input {
    width: calc(100% - 90px);
    padding: 10px;
    margin-right: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    padding: 10px 20px;
    border: none;
    background: #007BFF;
    color: white;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background: #0056b3;
}
