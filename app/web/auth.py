from app.forms.auth import RegisterForm
from app.forms.auth import LoginForm

from app.models.user import User
from app.models.base import db


from flask import request, jsonify

from . import web

from app.lib.http import login_required, create_token, verify_token


@web.route('/api/user/logout', methods=['GET'])
def logout():
    try:
        token = request.headers['Authorization']
        user = verify_token(token)
        if user:
            with db.auto_commit():
                result = User.query.filter_by(id=user.id).first()
                result.launched = False
        return jsonify({
            'code': 200,
            'message': '退出成功'
        })
    except:
        return jsonify({
            'code': 200,
            'message': '退出失败'
        })


@web.route('/api/user/info/get', methods=['GET'])
def getuserinfo():
    token = request.headers['Authorization']
    user = verify_token(token)
    id = user.id
    name = user.name
    roles = user.roles.split(',')


    return jsonify({
        'code': 200,
        'message': '请求用户信息成功',
        'data': {
            'userList': {
                'roles': roles,
                'name': name,
                'id': id
            }
        }
    })



@web.route('/api/user/register', methods=['POST'])
def register():
    form = request.form
    form = RegisterForm(request.form)
    if request.method  == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return jsonify({
            'code': 200,
            'message': '注册成功'
        })
    return jsonify({
            'code': 201,
            'message': '注册失败'
        })

@web.route('/api/user/login', methods=['POST'])
def login():

    form = request.form
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(name=form.name.data).first()
        if user and user.check_password(form.password.data):
            with db.auto_commit():

                user.launched = True

            token = create_token(user.id)
            return jsonify({
                'code': 200,
                'message': '登录成功',
                'token': token,
                'username': user.name,
                'roles': user.roles.split(',')
            })
        return jsonify({
            'code': 201,
            'message': '用户名或密码有误,请在仔细检查一下重新输入'
        })
    else:
        return jsonify({
            'code': 201,
            'message': '登录失败'
        })