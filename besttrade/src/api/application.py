from flask import Flask
from besttrade.src.api.blueprints.investorbp import investor_blueprint

application = app = Flask(__name__)

app.register_blueprint(investor_blueprint)

if __name__ == '__main__':
    application.run()