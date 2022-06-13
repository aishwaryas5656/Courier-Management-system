# imports----------------------------------------------------------------------------------------------------------------------
from branch.branch import courierBoys
from flask import Blueprint,session,render_template,request,flash,redirect,url_for
from database import mysql
from flask_mysqldb import MySQLdb
import bcrypt

# create blueprint of courier_boy----------------------------------------------------------------------------------------------
courier_boy = Blueprint('courier_boy', __name__, url_prefix='/courier_boy', template_folder='templates',static_folder='static')

# courier boy main page-------------------------------------------------------------------------------------------------------
@courier_boy.route('/')
def courier_boy_index():
    return render_template('courier_boy/index.html')

# courier boy login------------------------------------------------------------------------------------------------------------
@courier_boy.route('/courier_boy/courier_boy_login',methods=["GET","POST"])
@courier_boy.route('/courier_boy_login',methods=["GET","POST"])
def courier_boy_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM courierboydb WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if (user):
            if password == user["password"]:
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                session['email'] = user['email']
                session['phone'] = user['phone']
                session['password'] = user['password']
                session['address'] = user['address']
                session['city'] = user['city']
                session['question'] = user['question']
                session['answer'] = user['answer']
                session['status'] = user['status']
                session['random_num'] = user['random']

                return render_template("courier_boy/index.html")
            else:
                flash('email and password not match')
            return redirect(url_for('courier_boy.courier_boy_login'))
        else:
            flash('wrong email id')
            return redirect(url_for('courier_boy.courier_boy_login'))
    else:
        return render_template("courier_boy/courier_boy_login.html")

# courier boy application ------------------------------------------------------------------------------------------------------
@courier_boy.route('courier_boy/courierBoyApplication',methods=["GET","POST"])
@courier_boy.route('/courierBoyApplication',methods=["GET","POST"])
def courierBoyApplication():
    if request.method == 'GET':
            return render_template("courier_boy/courierBoyApplication.html")
    else:
        first_name = request.form['first_name'] 
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        address = request.form['address']
        city = request.form['city']
        question = request.form['question']
        answer = request.form['answer']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO courierboydb (first_name,last_name,email,phone,password,address,city,question,answer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(first_name,last_name,email,phone,password,address,city,question,answer))
        mysql.connection.commit()
        flash('register successful')
        return redirect(url_for('courier_boy.courier_boy_login'))


# courier boy forget password----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@courier_boy.route('courier_boy/forget_password')
def forget_password():

    if request.method == 'GET' :
        return render_template('courier_boy/forget_password.html')
        
    else:
        email = request.form['email']
        question = request.form['question']
        answer = request.form['answer']
        password = request.form['password']

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM courierboydb WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()


        if (user):
            if (question == user['question']):
                if answer == user['answer']:
                    curl = mysql.connection.cursor()
                    curl.execute('UPDATE courierboydb SET password="{}" where email="{}"'.format(password,email))
                    mysql.connection.commit()
                    curl.close()
                    
                    flash('password updated')
                    return redirect(url_for('courier_boy.courier_boy_login'))
                else:
                    flash('invalid answer')
                    return redirect(url_for('courier_boy.forget_password'))
            else:
                flash('invalid question')
                return redirect(url_for('courier_boy.forget_password'))
        else:
            flash('email not found')
            return redirect(url_for('courier_boy.forget_password'))


# courier details----------------------------------------------------------------------------------------------------------------------------------------
@courier_boy.route('/couriers')
def couriers():
    city = session['city']
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute('SELECT * FROM courier where r_city="{}"'.format(city))
    user = curl.fetchall()
    curl.close()
    return render_template('courier_boy/couriers.html',contacts=user)

# profile----------------------------------------------------------------
@courier_boy.route('courier_boy/profile', methods=["GET", "POST"])
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
            cur.execute('UPDATE courierboydb SET name="{}",email="{}",phone="{}",question="{}",answer="{}"  WHERE email="{}"'.format(nm,em,nu,qs,aw,uid))
            mysql.connection.commit()
            cur.close()

            session['name'] = nm
            session['email'] = em
            session['phone'] = nu
            session['question'] = qs
            session['answer'] = aw
            
            flash('profile update successful')
            return redirect(url_for('courier_boy.courier_boy_index'))
        else:
            return redirect(url_for('courier_boy.courier_boy_index'))
    except:
        flash('Email already exist')
        return redirect(url_for('courier_boy.courier_boy_index'))
# ----------------------------------------------------------------------
@courier_boy.route('courier_boy/courier_boy/resubmit', methods=["GET", "POST"])
def resubmit():
    try:
        if request.method == 'POST':
            id = session['email']
            nm = request.form['first_name']
            ls = request.form['last_name']
            em = request.form['email']
            pn = request.form['phone']
            ps = request.form['password']
            ct = request.form['city']
            addr = request.form['address']
            st = ""
            cur = mysql.connection.cursor()
            cur.execute('UPDATE courierboydb SET first_name="{}",last_name="{}",email="{}",phone="{}",password="{}",city="{}",address="{}",status="{}"  WHERE email="{}"'.format(nm,ls,em,pn,ps,ct,addr,st,id))
            mysql.connection.commit()
            cur.close()
            session['first_name'] = nm
            session['last_name'] = ls
            session['email'] = em
            session['phone'] = pn
            session['password'] = ps
            session['address'] = addr
            session['city'] = ct
            session['status'] = st

            flash('profile update successful')
            return redirect(url_for('courier_boy.resubmit'))
        else:
            return render_template('courier_boy/index.html')
    except:
        flash('Mail already exist')
        return redirect(url_for('courier_boy.profile'))

# verification--------------------------------------------------------------------------------------------------------------------------
@courier_boy.route('courier_boy/courier_boy/verification', methods=["GET", "POST"])
def verification():

    if request.method == 'POST':
        code = session['random_num']
        id = session['email']
        if request.form['random_num'] == code:
            cur = mysql.connection.cursor()
            cur.execute('UPDATE courierboydb SET random="" WHERE email="{}"'.format(id))
            mysql.connection.commit()
            cur.close()
            flash('verification successfull')
            return redirect(url_for('courier_boy.courier_boy_login'))
        else:
            flash('not match, try again...')
            return redirect(url_for('courier_boy.verification'))
    else:
        return redirect(url_for('courier_boy.courier_boy_index'))





# end of code===========================================================================================================================================