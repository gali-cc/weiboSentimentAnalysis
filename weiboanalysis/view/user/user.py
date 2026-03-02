from flask import Blueprint, jsonify, redirect, render_template, request, session
from weiboanalysis.dao import userDao
from weiboanalysis.util.md5Util import MD5Utility


ub = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')


@ub.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # 1. 获取并清洗参数 (视图层职责) 
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if not username or not password:
        return jsonify(error=True, info='用户名或密码不能为空')

    # 2. 调用 DAO 获取数据 (DAO层职责)
    user = userDao.get_user_by_username(username)

    # 3. 业务逻辑判断 (属于 Service 或 View 职责)
    if not user:
        return jsonify(error=True, info='用户不存在')

    if not MD5Utility.verify(password, user.password):
        return jsonify(error=True, info='密码错误')
    
    # 4. 登录成功，设置 session 或 token (视图层职责)
    session['user_id'] = user.id
    session['username'] = user.username
    
    return jsonify(success=True, info='登录成功')

@ub.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册用户
    """
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('password2', '').strip()
        
        if not username or not password or not confirm_password:
            return jsonify(error=True, info='用户名、密码或确认密码不能为空')
        
        if password != confirm_password:
            return jsonify(error=True, info='两次输入密码不一致')
        
        if userDao.get_user_by_name(username):
            return jsonify(error=True, info='用户名已存在')
        
        userDao.add_user(username, MD5Utility.encrypt(password))
        return jsonify(success=True, info='注册成功')
    

@ub.route('/logout', methods=['GET'])
def logout():
    """
    退出登录
    """
    session.clear()
    return redirect('/user/login')