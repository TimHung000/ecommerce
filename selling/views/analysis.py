from flask import render_template, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import Analysis
import datetime


analysis = Blueprint('analysis', __name__, template_folder='../templates')

@analysis.route('/dashboard')
@login_required
def dashboard():
    revenue_list = []
    transaction_count_list = []
    for month in range(1,13):
        monthly_revenue = Analysis.monthly_revenue(current_user.id, datetime.date.today().strftime("%Y"), month)

        if not monthly_revenue:
            revenue_list.append(0)
        else:
            revenue_list.append(monthly_revenue[0])
        
        monthly_transaction_count = Analysis.monthly_transaction_count(current_user.id, datetime.date.today().strftime("%Y"), month)
        if not monthly_transaction_count:
            transaction_count_list.append(0)
        else:
            transaction_count_list.append(monthly_transaction_count[0])
    


    username_list = []
    member_sale_list = []
    member_sale_count_list = []
    member_sales = Analysis.member_sale(current_user.id, datetime.date.today().strftime("%Y"))
    for member_sale in member_sales:
        username_list.append(member_sale[1])
        member_sale_list.append(member_sale[2])
        member_sale_count_list.append(member_sale[3])
    
    print(username_list)
    print(member_sale_list)
    print(member_sale_count_list)

    return render_template('dashboard.html', revenue_list = revenue_list, transaction_count = transaction_count_list, member_sale_list = member_sale_list, username_list = username_list, member_sale_count_list = member_sale_count_list, user=current_user.name)