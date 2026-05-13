from flask import Flask, render_template, request, url_for, flash, redirect
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ameerscoffee123'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'amirtj2007@gmail.com'
app.config['MAIL_PASSWORD'] = 'cfzwhnxzvxbdgwif'
app.config['MAIL_DEBUG'] = True

mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.String(15))
    image = db.Column(db.String(200))
    category = db.Column(db.String(50))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100))
    price = db.Column(db.String(20))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    items = MenuItem.query.all()    
    return render_template('menu.html', items=items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    success = False
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        msg = Message(
            subject=f'New message from {name}',
            sender=email,
            recipients=['amirtj2007@gmail.com'],
            body=f'Name: {name}\nEmail: {email}\nMessage: {message}'
        )
        mail.send(msg)
        success = True
    
    return render_template('contact.html', success=success)
@app.route('/add-item', methods=['GET', 'POST'])
@login_required
def add_item():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.form['image']
        category = request.form['category']
        
        new_item = MenuItem(name=name, description=description, price=price, image=image, category=category)
        db.session.add(new_item)
        db.session.commit()
        
        flash('Menu item added!')
        return redirect(url_for('menu'))
    
    return render_template('add_item.html')

@app.route('/edit-item/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('home'))
    item = MenuItem.query.get(id)
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.image = request.form['image']
        item.category = request.form['category']
        db.session.commit()
        flash('Item updated!')
        return redirect(url_for('menu'))
    
    return render_template('edit_item.html', item=item)

@app.route('/checkout/<item>/<price>', methods=['GET', 'POST'])
def checkout(item, price):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']

        new_order = Order(item=item, price=price, name=name, phone=phone, address=address)
        db.session.add(new_order)
        db.session.commit()

        msg = Message(
            subject=f'New Order - {item}',
            sender=app.config['MAIL_USERNAME'],
            recipients=['amirtj2007@gmail.com'],
            body=f'Item: {item}\nPrice: ${price}\nName: {name}\nPhone: {phone}\nAddress: {address}'
        )
        mail.send(msg)

        flash('Order placed successfully!')
        return redirect(url_for('home'))

    return render_template('checkout.html', item=item, price=price)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Wrong username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('login'))
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)