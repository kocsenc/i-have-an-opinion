# create our little application :)
from flask import Flask
import praw

app = Flask(__name__)


@app.route("/opinion")
def opinionate():
    message = "I am an anonymous person, and I have an opinion"
    post_reddit(message[:40], message)


def post_reddit(title, content):
    subreddit = "SubredditSimulator"

    r = praw.Reddit(user_agent='Opiniot github.com/kocsenc/i-have-an-opinion')
    r.login('opiniot', 'password', disable_warning=True)



if __name__ == "__main__":
    app.debug = True
    app.run()
