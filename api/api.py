import imp
from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *

api = Blueprint('api', __name__, template_folder='./templates')

login_manager = LoginManager(api)
login_manager.login_view = 'api.login'
login_manager.login_message = "請先登入"

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(userid):  
    user = User()
    user.id = userid
    data = Member.get_member_by_Id(userid)
    try:
        user.name = data[0]
    except:
        pass
    return user

@api.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        account = request.form['account']
        password = request.form['password']
        member = Member.get_member_by_account(account) 

        try:
            user_id = member[0]
            DB_password = member[3]
        except:
            flash('*沒有此帳號')
            return redirect(url_for('api.login'))

        if(DB_password == password ):
            user = User()
            user.id = user_id
            login_user(user)

            # return redirect(url_for('bookstore.bookstore'))
            # return redirect(url_for('manager.productManager'))
            return redirect(url_for('manager.home'))
        
        else:
            flash('*密碼錯誤，請再試一次')
            return redirect(url_for('api.login'))

    
    return render_template('login.html')

@api.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_account = request.form['account']
        all_member = Member.get_all_member()
        account_list = []
        for i in all_member:
            print(i)
            account_list.append(i[0])

        if(user_account in account_list):
            flash('Falied!')
            return redirect(url_for('api.register'))
        else:
            input = { 
                'username': request.form['username'], 
                'account' : user_account, 
                'password': request.form['password'], 
            }
            Member.create_member(input)
            return redirect(url_for('api.login'))

    return render_template('register.html')

@api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))