from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def recipe():
    return render_template('recipe.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('No such user')
        elif check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Wrong password')
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('registration.html')


@app.route('/spaghetti', methods=['GET'])
def spaghetti():
    return render_template('spaghetti.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        return render_template('profile.html', user=current_user)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        user = User.query.get(current_user.get_id())
        if user is None:
            abort(404)
        user.email = email
        user.username = username
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash('Username already taken')
        except sqlalchemy.exc.SQLAlchemyError:
            db.session.rollback()
            flash('Unable to save changes')
        else:
            return redirect(url_for('profile'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))





@app.route('/pancakes')
def pancakes():
    return render_template('pancakes.html')


if __name__ == '__main__':
    app.run()