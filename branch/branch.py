# imports--------------------------------------------------------------------------------------------------------
from flask import Blueprint,render_template,request,redirect,url_for,session
from courier.courier import courier
from flask.helpers import flash
from database import mysql
from flask_mysqldb import MySQLdb
import random

# creation of branch blueprint-----------------------------------------------------------------------------------
branch = Blueprint('branch', __name__, url_prefix='/branch', template_folder='templates',static_folder="static")

# branch index --------------------------------------------------------------------------------------------------
@branch.route('/')
def branch_index():
    return render_template('/branch/index.html')

# existing courier boys-------------------------------------------------------------------------------------------
@branch.route('branch/existing_courierboy')
@branch.route('/existing_courierboy')
def existing_courierboy():
    city = session['city']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM courierboydb where city="{}" AND status="accepted"'.format(city))
    data = cur.fetchall()
    cur.close()
    return render_template('branch/existing_courierboy.html',contacts = data)

# [delete courier boys]
@branch.route('branch/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('UPDATE courierboydb SET status="decline" WHERE id = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('branch.existing_courierboy'))

# branch login---------------------------------------------------------------------------------------------------
@branch.route('/branch/branch_login',methods=["GET","POST"])
@branch.route('/branch_login',methods=["GET","POST"])
def branch_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
 
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM branchdb WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
 
        if (user):
            if password == user["password"]:
                session['first_name'] = user['first_name']
                session['email'] = user['email']
                session['city'] = user['city']
                session['phone'] = user['phone']
                session['password'] = user['password']
                session['address'] = user['address']
                session['question'] = user['question']
                session['answer'] = user['answer']
                session['status'] = user['status']
                return render_template("branch/index.html")
            else:
                flash('email and password not match')
            return redirect(url_for('branch.branch_login'))
        else:
            flash('wrong email id')
            return redirect(url_for('branch.branch_login'))
    else:
        return render_template("branch/branch_login.html")

# courierboys------------------------------------------------------------------------------------------------------
@branch.route('/courierBoys')
def courierBoys():
    city = session['city']
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM courierboydb where city="{}" AND status=""'.format(city))
    data = cur.fetchall()
    cur.close()
    return render_template('branch/courierBoys.html',contacts = data)

# branch application----------------------------------------------------------------------------------------------
@branch.route('branch/branch_application',methods=["GET","POST"])
@branch.route('branch/branch/branch_application',methods=["GET","POST"])
def branch_application():
    try:
        if request.method == 'GET':
            return render_template("branch/branch_application.html")
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            address = request.form['address']
            city = request.form['city']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO branchDb (first_name,last_name,email,phone,password,address,city) VALUES (%s,%s,%s,%s,%s,%s,%s)",(first_name,last_name,email,phone,password,address,city))
            mysql.connection.commit()

            flash('register successful')
            return redirect(url_for('branch.branch_login'))
    except:
        flash("email or phone number already exists.. plz check it and try again...")
        return redirect(url_for('branch.branch_application'))

# decline of courier boys application----------------------------------------------------------------------------
@branch.route('branch/decline/<string:id>')
def decline_contact(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('UPDATE courierboydb SET status="decline" WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('branch.courierBoys'))

# accept of courier boys application----------------------------------------------------------------------------
@branch.route('branch/accept/<string:id>')
def accept(id):
    number = '1234567890'
    len= 10
    ran_num = "".join(random.sample(number,len))
    cur = mysql.connection.cursor()
    cur.execute('UPDATE courierboydb SET status="accepted",random="{}" WHERE id={}'.format(ran_num,id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('branch.courierBoys'))

# trancation---------------------------------------------------------------------------------------------------
@branch.route('/branch/transaction')
@branch.route('/transaction')
def transaction():
        city = session['city']
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute('SELECT * FROM courier where s_city="{}"'.format(city))
        user = curl.fetchall()
        curl.close()

        return render_template('branch/transaction.html',contacts=user)

# reset password-------------------------------------------------------------------------------------------
@branch.route('/branch/reset_request')
def reset_request():
    if request.method == 'GET' :
        return render_template("branch/reset_request.html")
    else:
        email = request.form['email']
        question = request.form['question']
        answer = request.form['answer']
        password = request.form['password']

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()


        if (user):
            if (question == user['question']):
                if answer == user['answer']:
                    curl = mysql.connection.cursor()
                    curl.execute('UPDATE branchdb SET password="{}" where email="{}"'.format(password,email))
                    mysql.connection.commit()
                    curl.close()
                    
                    flash('password updated')
                    return redirect(url_for('branch.branch_login'))
                else:
                    flash('invalid answer')
                    return redirect(url_for('branch.reset_request'))
            else:
                flash('invalid question')
                return redirect(url_for('branch.reset_request'))
        else:
            flash('email not found')
            return redirect(url_for('branch.reset_request'))


# end of code==================================================================================================