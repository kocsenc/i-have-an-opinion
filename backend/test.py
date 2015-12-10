# create our little application :)
import praw


def opinionate():
    message = "I am an anonymous person, and I have an opinion"
    post_reddit(message[:40], message)


def post_reddit(title, content):
    r = praw.Reddit(user_agent='Opiniot - Quickly share opinions by /u/kocsen'
                               'Url: https://github.com/kocsenc/i-have-an-opinion')
    r.login('opiniot', 'password', disable_warning=True)
    subreddit = "reddit_api_test"
    sub_obj = r.get_subreddit(subreddit)

    res = r.submit(subreddit, title, text=content, raise_captcha_exception=True)
    print(res)


def get_title_from_message(message):
    limit = 40
    if len(message) < limit:
        limit = len(message)

    split = message.split('/\s+/')
    res = ''

    while len(res) < limit:
        res = split.pop(0) + ' '

    return res + '...'


if __name__ == "__main__":
    opinionate()
