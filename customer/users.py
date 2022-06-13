#imports-------------------------------------------------------------------------------------------------------
from flask import Blueprint,render_template, request, redirect, url_for, session,flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from database import mysql
from flask_mysqldb import MySQLdb

#create blueprint of customer------------------------------------------------------------------------------------
customer = Blueprint('customer', __name__, url_prefix='/', template_folder='templates',static_folder="static")

#main page index-------------------------------------------------------------------------------------------------
@customer.route('/')
@customer.route('/index')
def customer_index():
    return render_template('customer/index.html')

@customer.route('/profile', methods=["GET", "POST"])
def profile():
    try:
        if request.method == 'POST':
            uid=session['email']
            
            nm = request.form['name']
            em = request.form['email']
            nu = request.form['phone']
            qs = request.form['question']
            aw = request.form['answer']

            cur = mysql.connection.cursor()
            cur.execute('UPDATE users SET name="{}",email="{}",phone="{}",question="{}",answer="{}"  WHERE email="{}"'.format(nm,em,nu,qs,aw,uid))
            mysql.connection.commit()
            cur.close()

            session['name'] = nm
            session['email'] = em
            session['phone'] = nu
            session['question'] = qs
            session['answer'] = aw
            
            flash('profile update successful')
            return redirect(url_for('.customer_index'))
        else:
            return redirect(url_for('.customer_index'))
    except:
        flash('Email already exist')
        return redirect(url_for('.customer_index'))

# customer registration----------------------------------------------------------------------------------------
@customer.route('/register', methods=["GET", "POST"]) 
def register():
    # try:
        if request.method == 'GET':
            return render_template("customer/register.html")
        elif request.method == 'POST':
            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM users")
            user = curl.fetchall()
            curl.close()
            if request.form['email'] == user:
                flash('Mail already exist')
                return redirect(url_for('customer.register'))
            else:
                name = request.form['name']
                email = request.form['email']
                phone = request.form['phone']
                password = request.form['password']
                question = request.form['question']
                answer = request.form['answer']

                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO users (name,email,phone,password,question,answer) VALUES (%s,%s,%s,%s,%s,%s)",(name,email,phone,password,question,answer))
                mysql.connection.commit()
                cur.close()

                session['name'] = request.form['name']
                session['email'] = request.form['email']
                session['phone'] = request.form['phone']
                session['question'] = request.form['question']
                session['answer'] = request.form['answer']
                flash('register successful')
                return redirect(url_for('customer.customer_index'))
    # except:
        flash('Mail already exist')  
        return redirect(url_for('customer.register'))

# customer login---------------------------------------------------------------------------------------------------------
@customer.route('/cu_login',methods=["GET","POST"])
def cu_login():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            curl.execute("SELECT * FROM users WHERE email=%s",(email,))
            user = curl.fetchone()
            curl.close()

            if (user):
                if  password == user["password"]:
                    session['name'] = user['name']
                    session['email'] = user['email']
                    session['phone'] = user['phone']
                    session['question'] = user['question']
                    session['answer'] = user['answer']
                    return redirect(url_for('.customer_index'))
                    
                else:
                    flash('Error password and email not match')
                    return redirect(url_for('customer.cu_login'))
            else:
                flash('user not found! please register.')
                return redirect(url_for('customer.cu_login'))

        else:
            return redirect(url_for('.customer_index'))
    except:
        flash("server busy, try again later...")
        return redirect(url_for('.customer_index'))
        

#reset password---------------------------------------------------------------------------------------------------
@customer.route('/reset_request',methods=["GET","POST"])
def reset_request():
    if request.method == 'GET' :
        return render_template("customer/reset_request.html")
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
                    curl.execute('UPDATE users SET password="{}" where email="{}"'.format(password,email))
                    mysql.connection.commit()
                    curl.close()
                    
                    flash('password updated')
                    return redirect(url_for('.customer_index'))
                else:
                    flash('invalid answer')
                    return redirect(url_for('.reset_request'))
            else:
                flash('invalid question')
                return redirect(url_for('.reset_request'))
        else:
            flash('email not found')
            return redirect(url_for('.reset_request'))


#courier transaction---------------------------------------------------------------------------------------------
@customer.route('/transaction')
def transaction():
    phone = session['phone']
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM courier where s_num="{}"'.format(phone))
    data = cur.fetchall()
    cur.close()
    return render_template("customer/transaction.html",contacts=data)

# customer logout-----------------------------------------------------------------------------------------------
@customer.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.customer_index'))
    

#customer_feedback---------------------------------------------------------------------------------------------------
@customer.route('/feedback', methods=["POST"])
def feedback():
    if request.method == 'POST':
        cid = ""
        email = request.form['email']
        message  = request.form['message']
        operation = 'feedback'
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO com_feed (cid, email, message, operation) VALUES (%s,%s,%s,%s)",(cid,email,message,operation,))
        mysql.connection.commit()
        cur.close()

        flash('feedback sucessful')
        return redirect(url_for('.customer_index'))

#customer_complaint---------------------------------------------------------------------------------------------------
@customer.route('/complaint', methods=["POST"])
def complaint():
    if request.method == 'POST':   

        cid = request.form['cid']
        email = session['email']
        message  = request.form['message']
        operation = 'complaint'
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO com_feed (cid, email, message, operation) VALUES (%s,%s,%s,%s)",(cid,email,message,operation,))
        mysql.connection.commit()
        cur.close()

        flash('compalint sucssusfull')
        return redirect(url_for('.customer_index'))

@customer.route('change_password',methods=['POST'])
def change_password():
    if request.method == 'POST':
        email = session['email']
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        password = request.form['old_password']

        if (user):
            if password == user["password"]:
                new_password = request.form['new_password']
            
                cur = mysql.connection.cursor()
                cur.execute('UPDATE users SET password="{}" WHERE email="{}"'.format(new_password,email))
                mysql.connection.commit()
                cur.close()
                flash('password updated')
                return redirect(url_for('.customer_index'))
            else:
                flash('password not match, try again.')    
                return redirect(url_for('.customer_index'))

    return redirect(url_for('.customer_index'))
        
# end of code===================================================================================================

