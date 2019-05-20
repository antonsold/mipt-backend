import os

from flask import Flask, redirect, url_for, request, render_template, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse

from db import User
from config import SECRET_KEY
from mailer import send_mail
from activation import get_user_by_activation_token

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    us = User.objects(id=user_id)
    if us.count() == 0:
        return None
    else:
        return us.next()


app.config['SECRET_KEY'] = SECRET_KEY

cnt = 0

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get(username=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def send_activation_link(user):
    send_mail(user.email, 'Activate your email',
        'Your activation link: ' + url_for('activate', token=user.get_activation_token(),
                                            _external=True))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        send_activation_link(user)
        flash('Activation link was sent to your email. Please activate your account')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/activate')
def activate():
    user = get_user_by_activation_token(request.args.get('token'))
    if user.is_active:
        flash('Error: your account was already activated')
    else:
        user.is_active = True
        user.save()
        flash('Your account was successfully activated')
    return redirect(url_for('index'))


@app.route('/private_page')
@login_required
def private_page():
    return render_template('private_page.html', title='Nice hat, kiddo')


if __name__ == '__main__':
    app.run(
        host=os.getenv('LISTEN_HOST', '127.0.0.1'),
        port=os.getenv('LISTEN_PORT', '8080'),
        debug=True
    )
