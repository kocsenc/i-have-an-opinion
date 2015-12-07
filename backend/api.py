# create our little application :)
import configparser
from flask import Flask, request
import tweepy

app = Flask(__name__)

def are_you_the_keymaster():
    config = configparser.ConfigParser()
    config.read('keys.ini')
    return config


def twitter_handler(message):
    twconf = are_you_the_keymaster()['twitter']
    auth = tweepy.OAuthHandler(twconf['conkey'], twconf['consec'])
    auth.set_access_token(twconf['atok'], twconf['atoksec'])
    api = tweepy.API(auth)
    return str(api.update_status(message))
    #return str(api.verify_credentials())


def choose_handler():
    # TODO: add other handlers
    def handler(message):
        print("Sending message", str(message))
        return twitter_handler
    return handler


def validate_message(message):
    print("Testing message", message)
    return message != ''


def handle_message(message):
    if not validate_message(message):
        return 'Bad message!', 400

    handler = choose_handler()

    return handler(message)


@app.route('/opinion', methods=['GET', 'POST', 'HEYLISTEN'])
def opinionate():
    if request.method == 'GET':
        return 'Hey! POST me an opinion to have it put somewhere.'
    elif request.method in ('POST', 'HEYLISTEN'):
        message = request.data
        return handle_message(message)


if __name__ == '__main__':
    app.debug = True
    app.run()
