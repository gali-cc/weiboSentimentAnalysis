from flask import Flask, redirect, render_template, request, session

from weiboanalysis.view.page import page
from weiboanalysis.view.user import user

app = Flask(__name__)
app.secret_key = 'asdasdasd'

app.register_blueprint(page.pb)
app.register_blueprint(user.ub)

@app.before_request
def before_request():
    """
    鉴权
    检查用户是否登录， 如果未登录， 则跳转到登录页面
    """
    # 1. 获取当前请求的端点 (Endpoint)
    endpoint = request.endpoint
    
    # 2. 如果请求的是不存在的路由（404），endpoint 会是 None
    if not endpoint:
        return None
    
    # 检查是否是公开的端点
    public_endpoints = {'user.login', 'user.register', 'user.logout', 'static'}
    if request.endpoint in public_endpoints:
        return None
    # 检查是否是静态文件
    if request.path.startswith('/static/'):
        return None
    # 检查用户是否登录
    if 'user_id' not in session or 'username' not in session:
        return redirect('/user/login')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
