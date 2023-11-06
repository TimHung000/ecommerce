from typing import Optional
from link import *

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class Member():
    def get_all_member():
        sql = "SELECT ACCOUNT FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_member_by_account(account):
        sql = "SELECT MID, USERNAME, ACCOUNT, PASSWD FROM MEMBER WHERE ACCOUNT = :account"
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'account' : account}))

    def get_member_by_Id(userId):
        sql = "SELECT USERNAME FROM MEMBER WHERE MID = :userId"
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'userId': userId}))

    def create_member(input):
        sql = "INSERT INTO MEMBER (USERNAME, ACCOUNT, PASSWD) VALUES (:username, :account, :password)"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(tno, pNo):
        sql = 'DELETE FROM RECORD WHERE TNO=:tno and pNo=:pNo '
        DB.execute_input(DB.prepare(sql), {'tno': tno, 'pNo':pNo})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()
       
class Product():
    def count_all():
        sql = 'SELECT COUNT(*) FROM PRODUCT WHERE ISAVAILABLE = 1'
        return DB.fetchone(DB.execute(DB.connect(), sql))
    
    def count_by_launcher(mId):
        sql = 'SELECT COUNT(*) WHERE mId = :mId FROM PRODUCT WHERE ISAVAILABLE = 1'
        return DB.fetchone(DB.execute(sql, {'mId': mId}))
    
    def get_all_product():
        sql = 'SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE FROM PRODUCT WHERE ISAVAILABLE = 1'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_product_by_pNo(pNo):
        sql ='SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE FROM PRODUCT WHERE PNO = :pNo'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'pNo': pNo}))
    
    def get_product_by_launcher(mId):
        sql = 'SELECT pNo, PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE FROM PRODUCT WHERE LAUNCHBY = :mId AND ISAVAILABLE = 1'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))
    
    def get_name(pNo):
        sql = 'SELECT PNAME FROM PRODUCT WHERE pNo = :pNo'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pNo': pNo}))[0]

    def add_product(input):
        sql = 'INSERT INTO PRODUCT(PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) VALUES (:pName, :price, :description, :launchBy, 1)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def discontinue_product(pNo):
        sql = 'UPDATE PRODUCT SET ISAVAILABLE = 0 WHERE PNO = :pNo'
        DB.execute_input(DB.prepare(sql), {'pNo': pNo})
        DB.commit()

    def update_product(input):
        sql = 'UPDATE PRODUCT SET PNAME = :pName, PRICE = :price, PDESC = :description WHERE PNO = :pNo'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_product(pNo, tno):
        sql = 'SELECT * FROM RECORD WHERE pNo = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pNo, 'tno':tno}))

    def get_price(pNo):
        sql = 'SELECT PRICE FROM PRODUCT WHERE pNo = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pNo}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pNo):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and pNo=:pNo'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pNo':pNo}) )[0]
    
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE pNo=:pNo and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    

class Orders():
    def add_order(input):
        sql = 'INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_order_by_mId(mId):
        sql = 'SELECT MID, CARTTIME, PNO, AMOUNT FROM ORDERS WHERE MID = :mId ORDER BY CARTTIME DESC'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.pNo = P.pNo'
        return DB.fetchall(DB.execute(DB.connect(), sql))


class Analysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), SUM(PRICE) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i}))

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), COUNT(OID) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))
    
    def category_sale():
        sql = 'SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.pNo = RECORD.pNo) GROUP BY CATEGORY'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT SUM(PRICE), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(PRICE) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))