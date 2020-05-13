from flask import Flask,render_template, request,session
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail

with open("C:\\Users\\Admin\\PycharmProjects\\website\\config.json","r") as c:
    params= json.load(c)["params"]
local_server=True

app = Flask(__name__)
app.secret_key = 'The-secret-key'
app.config.update(
    MAIL_SERVER='smtp.gmail.com', MAIL_PORT='465', MAIL_USE_SSL=True,MAIL_USERNAME= params['gmail-user'],MAIL_PASSWORD=params['gmail-password']

)
mail=Mail(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)





class Db_orders(db.Model):
    order_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    contact = db.Column(db.String(15), unique=True, nullable=False)
    order_cake = db.Column(db.String(10),  nullable=True)
    qty_cake = db.Column(db.String(250),  nullable=True)
    order_biscuits = db.Column(db.String(10),  nullable=True)
    qty_biscuits = db.Column(db.String(250),  nullable=True)
    order_bread = db.Column(db.String(10),  nullable=True)
    qty_bread = db.Column(db.String(250) , nullable=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.route('/')
def home():
    return render_template("MyBakery.html",params=params)
@app.route('/about')
def about():
    return render_template("about.html",params=params)

@app.route('/signin', methods = ['GET','POST'])
def signin():


    if request.method == 'POST':
        uname= request.form.get('uname')
        password= request.form.get('pass')
        if uname==params['user-name'] and password==params['user-pass']:
            session['user']=uname
            return render_template("orderNow.html")
        else:
            return render_template("MyBakery.html")
    return render_template('signin.html')


@app.route('/orderNow', methods = ['GET','POST'])
def orderNow():
    if(request.method== 'POST'):
        '''Add entry to the database'''
        name= request.form.get("name")
        email = request.form.get("email")
        contact = request.form.get("contact")
        order_cake= request.form.get("order_cake")
        order_biscuits= request.form.get("order_biscuits")
        order_bread= request.form.get("order_bread")
        qty_cake= request.form.get("qty_cake")
        qty_biscuits= request.form.get("qty_biscuits")
        qty_bread= request.form.get("qty_bread")
        entry=Db_orders(name=name,email=email,contact=contact,order_cake=order_cake,qty_cake=qty_cake,order_biscuits=order_biscuits,qty_biscuits=qty_biscuits,order_bread=order_bread,qty_bread=qty_bread)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New order', sender=email, recipients=[params['gmail-user']]
                          ,body=qty_cake+" " +qty_biscuits+ " "+qty_bread+ "\n" + contact)
    return render_template("orderNow.html",params=params)

if __name__ == '__main__':
    app.run(debug=True)
