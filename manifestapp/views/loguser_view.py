"""User logining routes"""
from flask import Blueprint, request, flash, url_for
from flask import render_template, redirect
from flask_login import login_required, logout_user, login_user
from manifestapp.logger import logger_setup
from manifestapp.models import User, policy
from manifestapp.extensions import db

loguser_bp = Blueprint('log', __name__, static_folder='static', url_prefix='/log')

logger = logger_setup(__name__, '%(levelname)s::%(name)s::%(asctime)s'
                                '::%(message)s', 'webapp.log', 'DEBUG')


@loguser_bp.route('/in', methods=['GET', 'POST'])
def login():
    """login route"""

    if request.method == 'POST':
        trying_user = User.query.filter(User.username == request.form.get('username')).first()
        if trying_user and trying_user.check_pwd(attempted_pwd=request.form.get('password')):
            login_user(trying_user, remember=True)
            logger.debug('User %s was logged in.', trying_user.username)
            return redirect(url_for('events.main'))

        flash('Username and/or password are incorrect. Please, try again', 'info')
        logger.error('Username and/or password are incorrect. Please, try again')

    return render_template('login.html')


@loguser_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register route"""

    if request.method == 'POST':
        if request.form.get('password') == request.form.get('password2'):
            pwd_test = policy.test(request.form.get('password'))
            if not pwd_test:
                new_user = User(username=request.form.get('username'),
                                password=request.form.get('password'))

                check_user = User.query.filter(User.username == new_user.username).first()
                if check_user:
                    msg = f'User <{check_user.username}> already exists. Please, use another username or go to login page'
                else:
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    logger.debug('User successfully registered and logged in')
                    return redirect(url_for('events.main'))
            else:
                msg = f'Password is not strong enough. Errors: {pwd_test}'

        else:
            msg = 'Passwords do not match.'

        flash(msg, 'info')
        logger.debug(msg)

    return render_template('register.html')


@loguser_bp.route('/out')
@login_required
def logout():
    """Logout route"""

    logout_user()
    logger.debug('Current user is logged out')
    return redirect(url_for('log.login'))
