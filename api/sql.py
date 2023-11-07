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
        sql = 'SELECT * FROM MEMBER WHERE ACCOUNT = :account'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'account': account}))

    def get_member_by_Id(userId):
        sql = "SELECT USERNAME FROM MEMBER WHERE MID = :userId"
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'userId': userId}))

    def create_member(username, account, password):
        sql = "INSERT INTO MEMBER (USERNAME, ACCOUNT, PASSWD) VALUES (:username, :account, :password)"
        DB.execute_input(DB.prepare(sql), {'username': username, 'account': account, 'password': password})
        DB.commit()
    
    def delete_product(tno, pNo):
        sql = 'DELETE FROM RECORD WHERE TNO=:tno and pNo=:pNo'
        DB.execute_input(DB.prepare(sql), {'tno': tno, 'pNo':pNo})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():        
    def get_current_cart(mId):
        sql = 'SELECT * FROM CART WHERE MID = :mId AND TNO IS NULL'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'mId': mId}))

    def add_cart(mId, cartTime, format):
        sql = 'INSERT INTO CART(MID, CARTTIME) VALUES (:mId, TO_DATE(:cartTime, :format))'
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'cartTime': cartTime, 'format': format})
        DB.commit()

    def get_all_product_in_cart(mId, cartTime):
        sql = 'SELECT PNO, PNAME, AMOUNT, PRICE, LAUNCHBY  FROM CART NATURAL JOIN ORDERS NATURAL JOIN PRODUCT WHERE MID = :mId AND CARTTIME = :cartTime'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId, 'cartTime': cartTime}))
    
    def get_total_price(mId, cartTime):
        sql = 'SELECT SUM(AMOUNT * PRICE) FROM CART NATURAL JOIN ORDERS NATURAL JOIN PRODUCT WHERE MID = :mId AND CARTTIME = :cartTime'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'mId': mId, 'cartTime': cartTime}))[0]
    
    def complete_cart(mId, cartTime, tNo):
        sql = 'UPDATE CART SET TNO = :tNo WHERE MID = :mId AND CARTTIME = :cartTime'
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'cartTime': cartTime, 'tNo': tNo})
        DB.commit()
       
class Product():
    def add_product(input):
        sql = 'INSERT INTO PRODUCT(PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) VALUES (:pName, :price, :description, :launchBy, 1)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def count_all():
        sql = 'SELECT COUNT(*) FROM PRODUCT WHERE ISAVAILABLE = 1'
        return DB.fetchone(DB.execute(DB.connect(), sql))
    
    def count_by_launcher(mId):
        sql = 'SELECT COUNT(*) WHERE mId = :mId FROM PRODUCT WHERE ISAVAILABLE = 1'
        return DB.fetchone(DB.execute(sql, {'mId': mId}))
    
    def get_all_product():
        sql = 'SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY FROM PRODUCT WHERE ISAVAILABLE = 1'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_product_by_pNo(pNo):
        sql ='SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY FROM PRODUCT WHERE PNO = :pNo'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'pNo': pNo}))
    
    def get_product_by_launcher(mId):
        sql = 'SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY FROM PRODUCT WHERE LAUNCHBY = :mId AND ISAVAILABLE = 1'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))
    
    def get_product_by_keyword(keyword):
        sql = 'SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY FROM PRODUCT WHERE PNAME LIKE :keyword'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'keyword': f'%{keyword}%'}))
    
    def update_product(input):
        sql = 'UPDATE PRODUCT SET PNAME = :pName, PRICE = :price, PDESC = :description WHERE PNO = :pNo'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def discontinue_product(pNo):
        sql = 'UPDATE PRODUCT SET ISAVAILABLE = 0 WHERE PNO = :pNo'
        DB.execute_input(DB.prepare(sql), {'pNo': pNo})
        DB.commit()
    
class Record():
    def add_record(tNo, pNo, amount, salePrice):
        sql = 'INSERT INTO RECORD(TNO, PNO, AMOUNT, SALEPRICE) VALUES (:tNo, :pNo, :amount, :salePrice)'
        DB.execute_input(DB.prepare(sql), {'tNo': tNo, 'pNo': pNo, 'amount': amount, 'salePrice': salePrice})
        DB.commit()
    

class Orders():
    def add_order(mId, cartTime, pNo, amount):
        sql = 'INSERT INTO ORDERS(MID, CARTTIME, PNO, AMOUNT) VALUES(:mId, :cartTime, :pNo, :amount)'
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'cartTime': cartTime, 'pNo': pNo, 'amount': amount})
        DB.commit()
    
    def update_order_increment_pNo(mId, cartTime, pNo):
        sql = 'UPDATE ORDERS SET AMOUNT = AMOUNT + 1 WHERE MID = :mId AND cartTime = :cartTime AND PNO = :pNo'
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'cartTime': cartTime, 'pNo': pNo})
        DB.commit()

    def update_amount(mId, cartTime, pNo, amount):
        sql = 'UPDATE ORDERS SET AMOUNT = :amount WHERE MID = :mId AND cartTime = :cartTime AND PNO = :pNo'
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'cartTime': cartTime, 'pNo': pNo, 'amount': amount})
        DB.commit()

    def delete_order(mId, cartTime, pNo):
        sql = 'DELETE FROM ORDERS WHERE MID = :mId AND CARTTIME = :cartTime AND PNO = :pNo'
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'cartTime': cartTime, 'pNo': pNo})
        DB.commit()

class Transaction():
    def add_transaction(mId, transTime, format):
        sql = 'INSERT INTO TRANSACTION(BUYERID, TRANSTIME) VALUES(:mId, TO_DATE(:transTime, :format)) RETURNING TNO INTO :out_tNo'
        cursor = DB.prepare(sql)
        out_tNo = cursor.var(oracledb.DB_TYPE_NUMBER)
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'TRANSTIME': transTime, 'format': format, 'out_tNo': out_tNo})
        DB.commit()
        return int(out_tNo.getvalue()[0])
    
    def get_transact_list_by_buyer(mId):
        sql = 'SELECT TRANSACTION.TNO, SUM(AMOUNT * SALEPRICE), TRANSTIME FROM TRANSACTION LEFT JOIN RECORD ON TRANSACTION.TNO = RECORD.TNO WHERE BUYERID = :mId GROUP BY (TRANSACTION.TNO, TRANSTIME) ORDER BY TRANSTIME DESC'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))

    def get_transact_detail_by_buyer(mId):
        sql = 'SELECT TNO, PNO, PNAME, AMOUNT, SALEPRICE FROM TRANSACTION NATURAL JOIN RECORD NATURAL JOIN PRODUCT WHERE BUYERID = :mId ORDER BY TRANSTIME DESC'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))

    def get_transact_list_by_seller(mId):
        sql = 'SELECT TNO, BUYERID, SUM(AMOUNT * SALEPRICE), TRANSTIME FROM TRANSACTION NATURAL JOIN RECORD NATURAL JOIN PRODUCT WHERE LAUNCHBY = :mId GROUP BY (TNO, TRANSTIME, BUYERID) ORDER BY TRANSTIME DESC'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))

    def get_transact_detail_by_seller(mId):
        sql = 'SELECT TNO, PNO, PNAME, AMOUNT, SALEPRICE FROM TRANSACTION NATURAL JOIN RECORD NATURAL JOIN PRODUCT WHERE LAUNCHBY = :mId ORDER BY TRANSTIME DESC'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))    
    

class Analysis():
    def monthly_revenue(mId, year, month):
        sql = 'SELECT SUM(AMOUNT * SALEPRICE) FROM TRANSACTION NATURAL JOIN RECORD NATURAL JOIN PRODUCT WHERE LAUNCHBY = :mId AND EXTRACT(MONTH FROM TRANSTIME) = :month AND EXTRACT(YEAR FROM TRANSTIME) = :year'
        return DB.fetchone(DB.execute_input(DB.prepare(sql) , {"mId": mId, "year": year, "month": month}))

    def monthly_transaction_count(mId, year, month):
        sql = 'SELECT COUNT(UNIQUE TNO) FROM TRANSACTION NATURAL JOIN RECORD NATURAL JOIN PRODUCT WHERE LAUNCHBY = :mId AND EXTRACT(MONTH FROM TRANSTIME) = :month AND EXTRACT(YEAR FROM TRANSTIME) = :year'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {"mId": mId, "year": year, "month": month}))

    def member_sale(mId, year):
        sql = 'SELECT BUYERID, USERNAME, SUM(AMOUNT * SALEPRICE), COUNT(DISTINCT TNO) FROM TRANSACTION NATURAL JOIN RECORD NATURAL JOIN PRODUCT JOIN MEMBER ON BUYERID = MID WHERE LAUNCHBY = :mId AND EXTRACT(YEAR FROM TRANSTIME) = :year GROUP BY (BUYERID, USERNAME) ORDER BY SUM(AMOUNT * SALEPRICE) DESC'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {"mId": mId, "year": year}))

    def member_sale_count(mId, year):
        sql = 'SELECT BUYERID, USERNAME, COUNT(DISTINCT TNO) FROM TRANSACTION NATURAL JOIN RECORD NATURAL JOIN PRODUCT JOIN MEMBER ON BUYERID = MID WHERE LAUNCHBY = :mId AND EXTRACT(YEAR FROM TRANSTIME) = :year GROUP BY (BUYERID, USERNAME) ORDER BY COUNT(DISTINCT TNO) DESC'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {"mId": mId, "year": year}))