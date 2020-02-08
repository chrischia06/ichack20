from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
	return app

app = create_app()
db = SQLAlchemy(app)

from app import routes



if __name__=="__main__":	
	app.run(debug=True)
    # app.run(host='0.0.0.0',port=8000)