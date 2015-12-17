#!/usr/bin/env python3
# create our little application :)
from flask import Flask, request
from flask.ext.cors import CORS

import argparse
import configparser
import praw
import random
import tweepy

app = Flask(__name__)
CORS(app)

dry_run = None
config = None


def twitter_handler(message):
    twconf = are_you_the_keymaster()['twitter']
    auth = tweepy.OAuthHandler(twconf['conkey'], twconf['consec'])
    auth.set_access_token(twconf['atok'], twconf['atoksec'])
    api = tweepy.API(auth)
    return str(api.update_status(message))


def reddit_handler(message):
    """
    Sadly not working. thanks captchas
    :param message:
    :return: 200
    """
    # title = message[:40]
    # subreddit = "reddit_api_test"
    #
    # r = praw.Reddit(
    #     user_agent='Opiniot - Quickly share opinions by /u/opiniot Url: https://github.com/kocsenc/i-have-an-opinion')
    # r.login('opiniot', 'password', disable_warning=True)
    # sub_obj = r.get_subreddit(subreddit)
    #
    # # res = r.submit(subreddit, title, text=message, raise_captcha_exception=True)
    # res = r.submit(subreddit, title, text=message)

    return '', 200


def devnull_handler(message):
    return '', 200


def are_you_the_keymaster():
    config = configparser.ConfigParser()
    config.read('keys.ini')
    return config


def dry_run_handler_wrapper(handler):
    def dry_run_handler(message):
        print("Would be using", handler.__name__, "for", message)
        return '', 200

    return dry_run_handler


def logging_handler_wrapper(handler):
    def logging_handler(message):
        print("Using", handler.__name__, "for", message)
        return handler(message)

    return logging_handler


HANDLERS = (twitter_handler, devnull_handler, reddit_handler)


def choose_handler():
    global dry_run

    handler = random.choice(HANDLERS)

    if dry_run:
        handler = dry_run_handler_wrapper(handler)
    else:
        handler = logging_handler_wrapper(handler)

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='debug', action='store_true', help='Enable debug mode')
    parser.add_argument('-n', dest='dry', action='store_true',
                        help="Don't make any external requests, just log what would have happened")

    args = parser.parse_args()

    dry_run = args.dry

    if dry_run:
        print("Dry run, not making any external requests")

    app.debug = args.debug
    config = are_you_the_keymaster()
    app.run()
