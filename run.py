from flask import Flask
from app.controllers.payment_controller import payment_bp
from app.config import Config
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.join('app', 'views'), static_folder='app/static')
    app.config.from_object(Config)
    app.register_blueprint(payment_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)