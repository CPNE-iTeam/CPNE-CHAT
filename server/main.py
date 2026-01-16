import html
from flask import Flask, jsonify, request
from flask_cors import CORS
import time

from message import Message
from db import Database

SERVER_PORT = 80
MESSAGES_TIME_LIMIT = 1  # seconds

app = Flask(__name__)
CORS(app)

db = Database()
db.init_db()


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the CPNEchat API !"

@app.route('/new_message', methods = ['GET', 'POST'])
def new_message():
    if request.method == 'POST':
        args = request.get_json()
    elif request.method == 'GET':
        args = request.args
    else:
        return jsonify({"status": "error", "message": "Invalid request method."}), 400

    content = args.get('content')
    if not content:
        return jsonify({"status": "error", "message": "Message content is required."}), 400
    escaped_content = html.escape(content)

    author = html.escape(args.get('author', 'Anonymous'))
    

    authorIP = request.remote_addr
    if not authorIP:
        return jsonify({"error": "Could not determine author IP."}), 400
    authorIpHash = hash(authorIP)

    authorNameTag = str(abs(authorIpHash))[3:6]

    nowTime = int(time.time())

    message = Message(content=escaped_content, author=author, authorIP=str(authorIpHash), authorNameTag=authorNameTag, time=nowTime)

    author_messages = db.get_messages_from_authorIP(str(authorIpHash))
    if len(author_messages) > 0 and author_messages[-1].time + MESSAGES_TIME_LIMIT > nowTime:
        return jsonify({"status": "error", "message": "You are sending messages too quickly. Please wait a moment before sending another message."}), 429

    try:
        db.new_message(message)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success"}), 200


@app.route("/messages", methods=["GET", "POST"])
def get_messages():
    try:
        messages = db.get_messages()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    messages_dict = [message.to_dict(includes=["content", "author", "authorNameTag", "time"]) for message in messages]
    return jsonify({"status": "success", "messages": messages_dict}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVER_PORT)