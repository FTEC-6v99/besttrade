import logging
import datetime
import pytz
from flask import Flask
from besttrade.src.api.blueprints.investorbp import investor_blueprint

application = app = Flask(__name__)

@app.route('/')
def health_check():
    date_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
    application.logger.info("The application is healthy. call received at: " + str(date_time))
    # print(f'The date time now is: {str(date_time)}')
    return f'OK: {str(date_time)}'

app.register_blueprint(investor_blueprint)

if __name__ == '__main__':
    application.run(debug=True)