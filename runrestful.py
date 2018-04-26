from flask import Flask
from urls import register_api


app = Flask(__name__)
register_api(app)


if __name__ == '__main__':
    app.run(debug=True)