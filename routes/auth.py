from flask import Blueprint, render_template, request, jsonify, session, redirect
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')


# 3.1. Основна адреса
@auth_bp.route('/')
def login():
    return render_template('login.html')
# ---------------------------------------------------------------------------------------------

# 3.2. Авторизація користувача (API)
@auth_bp.route('/api/login', methods=['POST'])
def login_page():
        data = request.get_json()

        user_name = data.get('userName')
        user_password = data.get('userPassword')

        if not user_name or not user_password:
            return jsonify({'success': False, 'message': 'Логін та пароль обов’язкові'}), 400

        found_user = User.query.filter_by(user_name_db=user_name).first()

        if found_user and found_user.user_password_db == user_password:
            session['user_in_session'] = found_user.user_name_db
            return jsonify({'success': True, 'message': 'Успішний вхід!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Невірний логін або пароль!'}), 401
# ---------------------------------------------------------------------------------------------

# 3.3. Вихід із системи
@auth_bp.route('/logout')
def logout():
     session.pop('user_in_session', None)
     return redirect('/')
# ---------------------------------------------------------------------------------------------

# 3.4. Головна панель управління (HTML)
@auth_bp.route('/dashboard')
def dashboard():
     get_user_name = session.get('user_in_session')
     return render_template('dashboard.html', user_name_with_session = get_user_name )
# ---------------------------------------------------------------------------------------------
