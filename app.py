from flask import Flask, redirect, render_template, session, request
from flask_mongoengine import MongoEngine
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField, SelectMultipleField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired
from wtforms import Label
from mongoengine.queryset import Q
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = [
    {
        "db": "sANDs",
        "host": "localhost",
        "port": 27017,
        "alias": "default",
    }
]
db = MongoEngine(app)
app.secret_key = 'KEY'
# salon -> [roles] ->

TYPES = [('Male', 'Male'), ('Female', 'Female'), ('Both', 'Both')]

# class EmployeeForm(FlaskForm):
#     name=StringField(label='Shop Name',validators=[DataRequired(message='EMPTY'),Length(min=3,max=20,message='Min 3 and Max 20')])
#     gender=
#     phone_number=
#     address=
#     email=
#     roles=


"""------------------------------------------------------------------------------------------FORM-----------------------------------------------------------------------------"""
ROLES=[('Artist','Artist'),('Senior Artist','Senior Artist'),('Hair stylist','Hair stylist'),('Assistant','Assistant'),('Manager','Manager'),('Receptionist','Receptionist')]

class EmployeeForm(FlaskForm):
    name=StringField(label='Name',validators=[DataRequired(message='EMPTY'),Length(min=3,max=20,message='Min 3 and Max 20')])
    gender = SelectField(label='Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    phone_number=IntegerField('Phone Number',validators=[Length(min=11,max=11,message='Phone Number Length Must Be 11'),InputRequired()])
    email=EmailField(label='Valid Email',validators=[DataRequired(message='EMPTY')])
    password1=PasswordField(label='Password',validators=[DataRequired(message='EMPTY'),Length(min=7,max=12,message='Min 7 and Max 12')])
    password2=PasswordField(label='Confirm Password',validators=[DataRequired(message='EMPTY'),Length(min=7,max=12,message='Min 7 and Max 12')])
    location=StringField(label='Location',validators=[DataRequired(message='EMPTY'),Length(min=3,max=20,message='Min 3 and Max 20')])
    roles=SelectField(label='Roless',choices=ROLES)
    submit = SubmitField()
    
    

class SalonForm(FlaskForm):
    shop_name = StringField(label='Shop Name', validators=[DataRequired(
        message='EMPTY'), Length(min=3, max=50, message='Min 3 and Max 20')])
    type_of_shop = SelectField(label='Type of shop', choices=TYPES)
    email = EmailField(label='Valid Email', validators=[
                       DataRequired(message='EMPTY')])
    password1 = PasswordField(label='Password', validators=[DataRequired(
        message='EMPTY'), Length(min=7, max=12, message='Min 7 and Max 12')])
    password2 = PasswordField(label='Confirm Password', validators=[DataRequired(
        message='EMPTY'), Length(min=7, max=12, message='Min 7 and Max 12')])
    location = StringField(label='Location', validators=[DataRequired(
        message='EMPTY'), Length(min=3, max=20, message='Min 3 and Max 20')])
    phone_number = IntegerField('Phone Number', validators=[Length(
        min=11, max=11, message='Phone Number Length Must Be 11'), InputRequired()])
    submit = SubmitField()


class OwnerForm(FlaskForm):
    owner_name = StringField('Owner Name', validators=[DataRequired(
        message='EMPTY'), Length(min=3, max=20, message='Min 3 and Max 20')])
    email = EmailField(label='Valid Email', validators=[
                       DataRequired(message='EMPTY')])
    password1 = PasswordField(label='Password', validators=[DataRequired(
        message='EMPTY'), Length(min=7, max=12, message='Min 7 and Max 12')])
    password2 = PasswordField(label='Confirm Password', validators=[DataRequired(
        message='EMPTY'), Length(min=7, max=12, message='Min 7 and Max 12')])
    submit = SubmitField()


class SalonLoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(
        'Its Empty!'), Length(min=3, max=30, message='Either Too SMALL Or To LARGE')])
    password1 = PasswordField(label="Password", validators=[DataRequired(
        'Its Emty!'), Length(min=5, max=12, message='Either Too SMALL Or To LARGE')])
    remember = BooleanField('remember me')
    submit = SubmitField()


class ServiceForm(FlaskForm):
    service_name = StringField(label='Service Name', validators=[DataRequired(
        message='EMPTY'), Length(min=3, max=100, message='min_lenth 3 and max_lenth 200')])
    about = StringField(label='About_service', validators=[DataRequired(
        message='EMPTY'), Length(min=2, max=200, message='min_lenth 3 and max_lenth 20')])
    price = IntegerField('prices')
    submit = SubmitField()



"""------------------------------------------------------------------------------------------DATABASEs-----------------------------------------------------------------------------"""


class Owner(db.Document):
    owner_name = db.StringField()
    email = db.EmailField(unique=True)
    password = db.StringField()


class Salon(db.Document):
    shop_name = db.StringField()
    type_of_shop = db.StringField()
    email = db.EmailField(unique=True)
    password = db.StringField()
    location = db.StringField()
    phone_number = db.IntField()
    owner = db.ReferenceField('Owner', reverse_delete_rule=db.CASCADE)

class Employee(db.Document):
    name=db.StringField()
    gender=db.StringField()
    email=db.EmailField(unique=True)
    password=db.StringField()
    location=db.StringField()
    roles=db.StringField()
    phone_number=db.IntField()
    salon = db.ReferenceField('Salon', reverse_delete_rule=db.CASCADE)

class Service(db.Document):
    name = db.StringField(unique=True)
    about = db.StringField()
    price = db.IntField()
    salon = db.ReferenceField('Salon', reverse_delete_rule=db.CASCADE)


@app.route('/salon_sign_up/', methods=['GET', 'POST'])
def salon_sign_up():
    employee_name=''
    owner_name=''
    salon_name=''
    if 'owner_id' in session:
        owner_name=Owner.objects(id=session['owner_id']).first().owner_name
    if 'employee_id' in session:
        employee_name=Employee.objects(id=session['employee_id']).first().name
    if 'salon_id' in session:
        salon_name=Salon.objects(id=session['salon_id']).first().shop_name
    if 'owner_id' in session:
        
        shop_name = ""
        type_of_shop = ""
        email = ""
        password1 = ""
        password2 = ""
        location = ""
        phone_number = ""
        error = ""
        form = SalonForm()
        if request.method == 'POST':
            if form.validate_on_submit:
                shop_name = form.data['shop_name']
                type_of_shop = form.data['type_of_shop']
                email = form.data['email']
                password1 = form.data['password1']
                password2 = form.data['password2']
                location = form.data['location']
                phone_number = form.data['phone_number']
                print(password1)
                if password1 == password2:
                    cipher = generate_password_hash(password1)
                    salon = Salon(shop_name=shop_name, type_of_shop=type_of_shop, email=email, password=cipher,
                                  location=location, phone_number=phone_number, owner=session['owner_id'])
                    salon.save()
                    if 'salon_id' in session:
                        session.pop('salon_id')
                    return redirect('/salon_list/')
                else:
                    error = 'Password Didnt Match'
    else:
        return redirect('/login/')

    return render_template('salon_signup.html', owner_name=owner_name,salon_name=salon_name,employee_name=employee_name,form=form)


@app.route('/owner_sign_up/', methods=['GET', 'POST'])
def owner_sign_up():
    form = OwnerForm()
    owner_name = ""
    email = ""
    password1 = ""
    password2 = ""
    error = ""
    if request.method == 'POST':
        if form.validate_on_submit:
            owner_name = form.data['owner_name']
            email = form.data['email']
            password1 = form.data['password1']
            password2 = form.data['password2']
            if password1 == password2:
                cipher = generate_password_hash(password1)
                owner = Owner(owner_name=owner_name,
                              email=email, password=cipher)
                owner.save()
                session.clear()
                return redirect('/login/')
        else:
            error = 'Password Didnt Match'
    return render_template('owner_sign.html', **locals())


@app.route('/salon_login/', methods=['GET', 'POST'])
def salon_login():
    employee_name=''
    owner_name=''
    salon_name=''
    if 'owner_id' in session:
        owner_name=Owner.objects(id=session['owner_id']).first().owner_name
    if 'employee_id' in session:
        employee_name=Employee.objects(id=session['employee_id']).first().name
    if 'salon_id' in session:
        salon_name=Salon.objects(id=session['salon_id']).first().shop_name
    salon=True
    form=SalonLoginForm()
    return render_template('login.html', salon=salon,form=form,owner_name=owner_name,salon_name=salon_name,employee_name=employee_name)


@app.route('/', methods=['GET', 'POST'])
def home():
    employee_name=''
    owner_name=''
    salon_name=''
    emp=''
    if 'owner_id' in session:
        owner_name=Owner.objects(id=session['owner_id']).first().owner_name
    if 'employee_id' in session:
        employee_name=Employee.objects(id=session['employee_id']).first().name
    if 'salon_id' in session:
        salon_name=Salon.objects(id=session['salon_id']).first().shop_name
    salon = ''
    services = ''
    roles=0
    if 'salon_id' in session:
        salon = session['salon_id']
    if'salon_id' in session:
        salon = Salon.objects(id=salon).first()
        services = Service.objects(salon=salon)
        if 'employee_id' in session:
            emp=Employee.objects(id=session['employee_id']).first()
            if emp.roles =='Manager':
                roles=2
            elif emp.roles== 'Receptionist':
                roles=3
            else:
                roles=0
        if 'owner_id' in session:
            roles=1
            emp=Employee.objects(salon=salon)
            print(len(emp))
            

    else:
        if 'owner_id' in session:
            return redirect('/salon_list/')
        return redirect('/login/')

    return render_template('home.html', salon=salon,employees=emp ,services=services,roles=roles,owner_name=owner_name,salon_name=salon_name,employee_name=employee_name)


@app.route('/create_service/', methods=['GET', 'POST'])
def create_service():
    service_name = ""
    about = ""
    price = ""
    form = ServiceForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            service_name = request.form['service_name']
            about = request.form['about']
            price = request.form['price']
            service = Service(name=service_name, about=about,
                              price=price, salon=session['salon_id'])
            service.save()
            return redirect('/')

    return render_template('create_service.html', **locals())


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = SalonLoginForm()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password1']
        type = request.form['type']
        if type=='owner':
            session.clear()
            logger=Owner.objects(email=email).first()
            if logger:
                if check_password_hash(logger.password,password):
                    session['owner_id']=str(logger.id)
                    return redirect('/salon_list/')
        elif type=='salon':
            logger=Salon.objects(email=email).first()
            if logger:
                if check_password_hash(logger.password,password):
                    session['salon_id']=str(logger.id)
                    return redirect('/')
        else:
            logger=Employee.objects(email=email).first()
            if logger:
                if check_password_hash(logger.password,password):
                    session['employee_id']=str(logger.id)
                    session['salon_id']=str(logger.salon.id)
                    return redirect('/')
        

    return render_template('login.html', form=form)


@app.route('/salon_list/')
def salon_list():
    employee_name=''
    owner_name=''
    salon_name=''
    if 'owner_id' in session:
        owner_name=Owner.objects(id=session['owner_id']).first().owner_name
    if 'employee_id' in session:
        employee_name=Employee.objects(id=session['employee_id']).first().name
    if 'salon_id' in session:
        salon_name=Salon.objects(id=session['salon_id']).first().shop_name
    if 'owner_id' in session:
        salons = Salon.objects(owner=session['owner_id'])
    else:
        return redirect('/login/')
    return render_template('salon_list.html', salons=salons,owner_name=owner_name,salon_name=salon_name,employee_name=employee_name)

@app.route('/create_appointment/',methods=['GET','POST'])
def create_appointment():
    employee_name=''
    owner_name=''
    salon_name=''
    if 'owner_id' in session:
        owner_name=Owner.objects(id=session['owner_id']).first().owner_name
    if 'employee_id' in session:
        employee_name=Employee.objects(id=session['employee_id']).first().name
    if 'salon_id' in session:
        salon_name=Salon.objects(id=session['salon_id']).first().shop_name
    if 'salon_id' in session:
            services=Service.objects(salon=session['salon_id'])
            employees=Employee.objects(Q(salon=session['salon_id'])&Q(roles__ne ='Manager'))
            if request.method=='POST':
                customer=request.form['name']
                emp=request.form.getlist('emp')
                print("➡ emp :", emp)
                serv=request.form.getlist('service')
                print("➡ serv :", serv)
                tp=0
                s=list()
                e=list()
                for i in serv:
                    s.append( Service.objects(id=i).first())
                    tp+=Service.objects(id=i).first().price
                for j in emp:
                    e.append(Employee.objects(id=j).first())
                print(tp)
                return render_template('appointment.html',customer_name=customer,services=s,employees=e,totalPrice=tp,owner_name=owner_name,salon_name=salon_name,employee_name=employee_name)
                
    return render_template('create_appointment.html',employees=employees,services=services,owner_name=owner_name,salon_name=salon_name,employee_name=employee_name)

@app.route('/logout/')
def loguut():
    session.clear()
    return redirect('/login/')


@app.route('/add_employee/',methods=['GET','POST'])
def add_employee():
    employee_name=''
    owner_name=''
    salon_name=''
    if 'owner_id' in session:
        owner_name=Owner.objects(id=session['owner_id']).first().owner_name
    if 'employee_id' in session:
        employee_name=Employee.objects(id=session['employee_id']).first().name
    if 'salon_id' in session:
        salon_name=Salon.objects(id=session['salon_id']).first().shop_name
    if 'salon_id' in session:
        print(session['salon_id'])
        form=EmployeeForm()
        if request.method=='POST':
            if form.validate_on_submit:
                if request.form['password1']==request.form['password2']:
                    cipher=generate_password_hash(request.form['password1'])
                    emp=Employee(name=request.form['name'],gender=request.form['gender'],email=request.form['email'],password=cipher,location=request.form['location'],roles=request.form['roles'],phone_number=request.form['phone_number'],salon=session['salon_id'])
                    print(emp)
                    emp.save()
                    return redirect('/')
    else:
        return redirect('/salon_login/')
    return render_template('add_employee.html',form=form,owner_name=owner_name,salon_name=salon_name,employee_name=employee_name)

@app.route('/login_employee/',methods=['GET','POST'])
def login_employee():
    employee_name=''
    owner_name=''
    salon_name=''
    if 'owner_id' in session:
        owner_name=Owner.objects(id=session['owner_id']).first().owner_name
    if 'employee_id' in session:
        employee_name=Employee.objects(id=session['employee_id']).first().name
    if 'salon_id' in session:
        salon_name=Salon.objects(id=session['salon_id']).first().shop_name
    employee=True
    form = SalonLoginForm()
    return render_template('login.html',employee=employee,form=form,owner_name=owner_name,salon_name=salon_name,employee_name=employee_name)

@app.route('/logout_employee/',methods=['GET','POST'])
def logout_employee():
    session.pop('employee_id')
    return redirect('/')

@app.route('/delete/<string:id>/<string:table>/',methods=['GET','POST'])
def delete(id,table):
    if(table=='service'):
        Service.objects(id=id).first().delete()
    if(table=='salon'):
        Salon.objects(id=id).first().delete()
    if(table=='employee'):
        Employee.objects(id=id).first().delete()
    else:
       e="table didnot found"
   
    return redirect('/')
@app.route('/salon_logout/')
def salon_logout():
    session.pop('salon_id')
    if 'owner_id' in session:
        return redirect('/salon_list/')
    return redirect('/login/')



if __name__ == ('__main__'):
    app.run(debug=True)
