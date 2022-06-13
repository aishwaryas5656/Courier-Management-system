#imports
from flask import Flask
from database import mysql
from admin.admin import admin
from branch.branch import branch
from courier.courier import courier
from courier_boy.courier_boy import courier_boy
from customer.users import customer

#create app
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cms'
app.secret_key='itsMySecretKey'
mysql.init_app(app)

# blue_print registration
app.register_blueprint(admin)
app.register_blueprint(branch)
app.register_blueprint(courier)
app.register_blueprint(courier_boy)
app.register_blueprint(customer)

# starting the app
if __name__ == "__main__":
    app.run(port=2021, debug=True)

