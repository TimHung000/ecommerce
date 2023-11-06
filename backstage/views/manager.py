from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():        
    if 'delete' in request.values:
        pNo = request.values.get('delete')
        product = Product.get_product_by_pNo(pNo)
        print(type(current_user.id))
        print(current_user.id)
        print(type(product[4]))
        print(product[4])
        print(pNo == product[4])
        if(product == None or str(product[4]) != current_user.id):
            flash('failed')
        else:
            Product.discontinue_product(pNo)
            flash(f'successfully discontinue product {product[1]}')
    
    elif 'edit' in request.values:
        pNo = request.values.get('edit')
        return redirect(url_for('manager.edit', pNo=pNo))
    
    product_data = get_product_by_memberId(current_user.id)
    return render_template('productManager.html', product_data = product_data, user=current_user.name)

def get_product_by_memberId(mId):
    products = Product.get_product_by_launcher(mId)
    product_data = []
    for i in products:
        product = {
            'pNo': i[0],
            'pName': i[1],
            'price': i[2],
        }
        product_data.append(product)
    return product_data

@manager.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.values.get('name')
        price = request.values.get('price')
        description = request.values.get('description')
        launchBy = current_user.id

        if (len(name) < 1 or len(price) < 1):
            return redirect(url_for('manager.productManager'))
        
        Product.add_product(
            {
                'pName' : name,
                'price' : price,
                'description': description,
                'launchBy' : launchBy
            }
        )

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        Product.update_product(
            {
                'pNo': request.values.get('pNo'),
                'pName': request.values.get('pName'),
                'price': request.values.get('price'),
                'description': request.values.get('description'),
            }
        )
        
        return redirect(url_for('manager.productManager'))
    else:
        product = show_info()
        return render_template('edit.html', data=product)


def show_info():
    pNo = request.args['pNo']
    data = Product.get_product_by_pNo(pNo)
    pName = data[1]
    price = data[2]
    description = data[3]
    isAvailable = data[4]
    product = {
        'pNo': pNo,
        'pName': pName,
        'price': price,
        'description': description,
        'isAvailable': isAvailable
    }
    return product


@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'POST':
        pass
    else:
        order_row = Orders.get_order_by_mId(current_user.id)
        order_data = []
        order_detail = []
        for i in order_row:
            order = {
                'mId': i[1],
                'cartTime': i[2],
                'pNo': i[3],
                'amount': i[4]
            }
            order_data.append(order)
            order_detail.append(order)
            
        # orderdetail_row = Order_List.get_orderdetail()
        # order_detail = []

        # for j in orderdetail_row:
        #     orderdetail = {
        #         '訂單編號': j[0],
        #         '商品名稱': j[1],
        #         '商品單價': j[2],
        #         '訂購數量': j[3]
        #     }
        #     order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)