# create our little application :)
from flask import Flask

app = Flask(__name__)


@app.route('/opinion')
def opinionate():
    return 'Hello World!'


if __name__ == '__main__':
    app.debug = True
    app.run()
