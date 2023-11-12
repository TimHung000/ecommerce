import re
from typing_extensions import Self
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
import random, string
from sqlalchemy import null
from link import *
import math
from base64 import b64encode
from api.sql import Member, Orders, Product, Record, Cart, Transaction, Comments

productStore = Blueprint('productStore', __name__, template_folder='../templates')

@productStore.route('/', methods=['GET', 'POST'])
@login_required
def product():
    result = Product.count_all(current_user.id)
    count = math.ceil(result[0]/9)
    flag = 0
    
    if 'keyword' in request.args and 'page' in request.args:
        total = 0
        single = 1
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        keyword = request.values.get('keyword')
        
        products = Product.get_product_by_keyword(keyword, current_user.id)
        product_list = []
        final_data = []
        
        for product in products:
            curr_product = {
                'pNo': product[0],
                'pName': product[1],
                'price': product[2],
                'launcherId': product[4],
                'username': product[5]
            }
            product_list.append(curr_product)
            total = total + 1

        
        if(len(product_list) < end):
            end = len(product_list)
            flag = 1
            
        for j in range(start, end):
            final_data.append(product_list[j])
            
        count = math.ceil(total/9)
        
        return render_template('productStore.html', single=single, keyword=keyword, product_data=product_list, user=current_user.name, page=page, flag=flag, count=count)    

    
    elif 'pNo' in request.args:
        pNo = request.args['pNo']
        product = Product.get_product_by_pNo(pNo)
        image = 'sdg.jpg'
        
        product = {
            'pNo': product[0],
            'pName': product[1],
            'price': product[2],
            'description': product[3],
            'launcherId': product[4],
            'username': product[5],
            'image': image
        }

        comment_list = []
        comments = Comments.get_product_comments(pNo)
        for comment in comments:
            curr_comment = {
                'username': comment[1],
                'commentTime' : comment[2],
                'comment' : comment[3]
            }
            comment_list.append(curr_comment)

        return render_template('product.html', product_data = product, comment_list = comment_list, user=current_user.name)
    
    elif 'page' in request.args:
        total = 0
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        
        products = Product.get_all_product(current_user.id)
        product_list = []
        final_data = []
        
        for product in products:
            product = {
                'pNo': product[0],
                'pName': product[1],
                'price': product[2],
                'launcherId': product[4],
                'username': product[5]
            }
            product_list.append(product)
            total += 1
            
        if(len(product_list) < end):
            end = len(product_list)
            flag = 1
            
        for j in range(start, end):
            final_data.append(product_list[j])
        count = math.ceil(total/9)    

        return render_template('productStore.html', product_data=final_data, user=current_user.name, page=page, flag=flag, count=count)    
    
    elif 'keyword' in request.args:
        single = 1
        keyword = request.values.get('keyword')
        Product.get_product_by_keyword(keyword, current_user.id)
        products = cursor.fetchall()
        product_list = []
        total = 0
        
        for product in products:
            curr_product = {
                'pNo': product[0],
                'pName': product[1],
                'price': product[2],
                'launcherId': product[4],
                'username': product[5]
            }
            product_list.append(curr_product)
            total = total + 1
            
        if(len(product_list) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('productStore.html', keyword=keyword, single=single, product_data=product_list, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        products = Product.get_all_product(current_user.id)
        product_list = []
        total = 0
        for product in products:
            curr_product = {
                'pNo': product[0],
                'pName': product[1],
                'price': product[2],
                'launcherId': product[4],
                'username': product[5]
            }
            total += 1
            if len(product_list) < 9:
                product_list.append(curr_product)
        count = math.ceil(total/9)
        
        return render_template('productStore.html', product_data=product_list, user=current_user.name, page=1, flag=flag, count=count)

@productStore.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'POST':
        if "pNo" in request.form :
            cart = Cart.get_current_cart(current_user.id)
            if(cart == None):
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                format = 'yyyy-mm-dd hh24:mi:ss'
                Cart.add_cart(current_user.id, time, format)
                cart = Cart.get_current_cart(current_user.id) 

            products = Cart.get_all_product_in_cart(cart[0], cart[1])
            pNo = request.values.get('pNo')

            exist = False
            for product in products:
                if str(product[0]) == pNo:
                    Orders.update_order_increment_pNo(cart[0], cart[1], pNo)
                    exist = True
                    break
            
            if not exist:
                Orders.add_order(cart[0], cart[1], pNo, 1)

        elif "delete" in request.form :
            pNo = request.values.get('delete')
            cart = Cart.get_current_cart(current_user.id)
            Orders.delete_order(cart[0], cart[1], pNo)
        
        elif "user_edit" in request.form:
            change_order()  
            return redirect(url_for('productStore.product'))
        
        elif "buy" in request.form:
            change_order()
            if request.values.get('paymentMethod') == 0 or request.values.get('deliveryType') == 0:
                return redirect(url_for('productStore.cart'))
            
            return redirect(url_for('productStore.transacting', paymentMethod=request.values.get('paymentMethod'), deliveryType = request.values.get('deliveryType')))

        elif "order" in request.form:
            cart = Cart.get_current_cart(current_user.id)
            products = Cart.get_all_product_in_cart(cart[0], cart[1])

            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            format = 'yyyy-mm-dd hh24:mi:ss'

            deliveryFee = int(request.values.get('deliveryFee'))
            deliveryType = request.values.get('deliveryType')
            paymentMethod = request.values.get('paymentMethod')


            tNo = Transaction.add_transaction(cart[0], time, format, paymentMethod, deliveryType, deliveryFee)
            for product in products:
                Record.add_record(tNo, product[0], product[2], product[3])
            
            Cart.complete_cart(cart[0], cart[1], tNo)

            return render_template('complete.html', user=current_user.name)

    cart = Cart.get_current_cart(current_user.id)
    if cart == None:
        return render_template('empty.html', user=current_user.name)

    products = Cart.get_all_product_in_cart(cart[0], cart[1])
    product_list = []
    for product in products:
        pNo = product[0]
        pName = product[1]
        amount = product[2]
        price = product[3]
        
        curr_product = {
            'pNo': pNo,
            'pName': pName,
            'amount': amount,
            'price': price
        }
        product_list.append(curr_product)
    
    if len(product_list) == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('cart.html', product_data=product_list, user=current_user.name)

@productStore.route('/transacting')
@login_required
def transacting():
    cart = Cart.get_current_cart(current_user.id)
    products = Cart.get_all_product_in_cart(cart[0], cart[1])
    product_list = []

    for product in products:
        curr_product = {
            'pNo': product[0],
            'pName': product[1],
            'amount': product[2],
            'price': product[3]
        }
        product_list.append(curr_product)
    

    deliveryType = request.values.get('deliveryType')
    paymentMethod = request.values.get('paymentMethod')

    paymentMethod = "信用卡" if paymentMethod == "1" else "貨到付款"
    deliveryType = "宅配" if deliveryType == "1" else "超商取貨"
    deliveryFee = 100 if deliveryType == '1' else 50
    product_price = Cart.get_total_price(cart[0], cart[1])
    total_price = product_price + deliveryFee
    return render_template('transacting.html', product_data=product_list,product_price=product_price, total_price=total_price, user=current_user.name, deliveryFee=deliveryFee, deliveryType=deliveryType, paymentMethod=paymentMethod)

@productStore.route('/transactionlist')
@login_required
def transactionList():
    transactions = Transaction.get_transact_list_by_buyer(current_user.id)
    transaction_list = []

    for transaction in transactions:
        curr_transac = {
            'tNo': transaction[0],
            'total_price': transaction[1],
            'transTime': transaction[2]
        }
        transaction_list.append(curr_transac)
    
    transactDetails = Transaction.get_transact_detail_by_buyer(current_user.id)
    detail_list = []

    for detail in transactDetails:
        curr_detial = {
            'tNo': detail[0],
            'pName': detail[2],
            'amount': detail[3],
            'salePrice': detail[4]
        }
        detail_list.append(curr_detial)


    return render_template('transactionList.html', transaction_data=transaction_list, detail_data=detail_list, user=current_user.name)

def change_order():
    cart = Cart.get_current_cart(current_user.id)
    products = Cart.get_all_product_in_cart(cart[0], cart[1])

    for product in products:
        # change the amount ordered
        if request.form[str(product[0])] != str(product[2]):
            Orders.update_amount(cart[0], cart[1], product[0], request.form[str(product[0])])

@productStore.route('/comment', methods=['POST'])
@login_required
def comment():
    if request.method == 'POST':
        comment = request.form.get("comment").strip()
        pNo = request.form.get("pNo")
        if comment != "":
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            format = 'yyyy-mm-dd hh24:mi:ss'
            Comments.add_product_comment(current_user.id, pNo, time, format, comment)

    return redirect(url_for('productStore.product', pNo = pNo))

