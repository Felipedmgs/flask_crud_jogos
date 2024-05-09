from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_pyfile('config.py') #chama arquivo de config

db = SQLAlchemy(app) #instanciando o orm
csrf = CSRFProtect(app)


from views import * #importa a view

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080) para rodar em outra porta
    app.run(debug=True) #com debug
    # app.run()


