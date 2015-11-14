#!/usr/bin/env python

import telegram
from flask import Flask, request
from functions import Response

app = Flask(__name__)

apiKey = ''

with open ('apikey.txt', 'r') as apiKeyFile:
    apiKey = apiKeyFile.read().replace('\n', '')

bot = telegram.Bot(token=apiKey)

responseGenerator = Response.ResponseGenerator()


@app.route('/' + apiKey.split(':')[1] + '/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))
        chat_id = update.message.chat.id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text

        response = responseGenerator.generate_response(text)

	if response is not None:
        	response = response.encode('utf-8')
        	bot.sendMessage(chat_id=chat_id, text=response)

    return 'ok'


@app.route('/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8888)
