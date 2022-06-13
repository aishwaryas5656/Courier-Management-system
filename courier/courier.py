# imports--------------------------------------------------------------------------------------------
from flask import Blueprint,render_template,request,Response,redirect,flash,url_for
from database import mysql
# creating of courier blueprint---------------------------------------------------------------------
courier = Blueprint('courier', __name__, url_prefix='/courier', template_folder='templates')

# courier deatil-----------------------------------------------------------------------------------
@courier.route('/courier_details',methods=["GET","POST"])
@courier.route('/courier/courier_details',methods=["GET","POST"])
def courier_details():
    if request.method == 'GET':
        return render_template("courier/courier_details.html")
    else:
        tid = 'suj2216'

        Qty = request.form['Qty']
        del_type = request.form['del_type']
        ship_type = request.form['ship_type']
        weight = request.form['weight']
        
        s_name = request.form['s_name']
        s_num = request.form['s_num']
        s_add = request.form['s_add']
        s_city = request.form['s_city']
        s_state = request.form['s_state']
        s_zip = request.form['s_zip']
        
        r_name = request.form['r_name']
        r_num = request.form['r_num']
        r_add = request.form['r_add']
        r_city = request.form['r_city']
        r_state = request.form['r_state']
        r_zip = request.form['r_zip']

        
        price =  150 + int(weight) * 10
        status = 'delevary placed'


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO courier (tid,Qty,del_type,ship_type,weight,s_name,s_num,s_add,s_city,s_state,s_zip,r_name,r_num,r_add,r_city,r_state,r_zip,price,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(tid,Qty,del_type,ship_type,weight,s_name,s_num,s_add,s_city,s_state,s_zip,r_name,r_num,r_add,r_city,r_state,r_zip,price,status))
        mysql.connection.commit()
        return redirect(url_for('courier.courier_details'))

# end of code=======================================================================================================================================