from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_pyfile('config.py') #chama arquivo de config

db = SQLAlchemy(app) #instanciando o orm
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


from views_game import * #importa a view
from views_user import *

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080) para rodar em outra porta
    app.run(debug=True) #com debug
    # app.run()


