"""
    This file hold the code for launching the webserver
    the webserver will allow our bot to persist to sleep signals 
    that are send by hosting services like heroku, replit ...

"""

from threading import Thread
from flask import Flask
app = Flask('')


@app.route('/')
def main():
    return "Your Bot Is Ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()
