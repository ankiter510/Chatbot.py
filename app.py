from flask import Flask, request, jsonify, render_template
from chatbot import get_chatbot_response

app = Flask(__name__)

# Add this route to handle requests to the root URL
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = get_chatbot_response(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
