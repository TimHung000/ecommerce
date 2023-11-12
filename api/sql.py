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
        sql = "SELECT MID, ACCOUNT, USERNAME FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_member_by_account(account):
        sql = 'SELECT MID, ACCOUNT, PASSWD, USERNAME FROM MEMBER WHERE ACCOUNT = :account'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'account': account}))

    def get_member_by_Id(userId):
        sql = "SELECT MID, ACCOUNT, USERNAME FROM MEMBER WHERE MID = :userId"
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

    def count_all(mId):
        sql = 'SELECT COUNT(*) FROM PRODUCT WHERE LAUNCHBY != :mId AND ISAVAILABLE = 1'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'mId': mId}))

        # return DB.fetchone(DB.execute(DB.connect(), sql))
    
    def count_by_launcher(mId):
        sql = 'SELECT COUNT(*) WHERE mId = :mId FROM PRODUCT WHERE ISAVAILABLE = 1'
        return DB.fetchone(DB.execute(sql, {'mId': mId}))
    
    def get_all_product(mId):
        sql = 'SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY, USERNAME FROM PRODUCT JOIN MEMBER ON PRODUCT.LAUNCHBY = MEMBER.MID WHERE LAUNCHBY != :mId AND ISAVAILABLE = 1'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))
    
    def get_product_by_pNo(pNo):
        sql ='SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY, USERNAME FROM PRODUCT JOIN MEMBER ON PRODUCT.LAUNCHBY = MEMBER.MID WHERE PNO = :pNo'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'pNo': pNo}))
    
    def get_product_by_launcher(mId):
        sql = 'SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY, USERNAME FROM PRODUCT JOIN MEMBER ON PRODUCT.LAUNCHBY = MEMBER.MID WHERE LAUNCHBY = :mId AND ISAVAILABLE = 1'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))
    
    def get_product_by_keyword(keyword, mId):
        sql = 'SELECT PNO, PNAME, PRICE, PDESC, LAUNCHBY, USERNAME FROM PRODUCT JOIN MEMBER ON PRODUCT.LAUNCHBY = MEMBER.MID WHERE PRODUCT.LAUNCHBY != :mId AND PNAME LIKE :keyword AND ISAVAILABLE = 1'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId, 'keyword': f'%{keyword}%'}))
    
    def update_product(input):
        sql = 'UPDATE PRODUCT SET PNAME = :pName, PRICE = :price, PDESC = :description WHERE PNO = :pNo'    
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def discontinue_product(pNo):
        sql = 'UPDATE PRODUCT SET ISAVAILABLE = 0 WHERE PNO = :pNo'
        DB.execute_input(DB.prepare(sql), {'pNo': pNo})
        DB.commit()


class Comments():
    def get_product_comments(pNo):
        sql = 'SELECT MID, USERNAME, COMMENTTIME, CONTENT FROM COMMENTS NATURAL JOIN MEMBER WHERE PNO = :pNo ORDER BY COMMENTTIME DESC'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'pNo': pNo}))
    
    def add_product_comment(mId, pNo, commentTime, format, content):
        sql = 'INSERT INTO COMMENTS(MID, PNO, COMMENTTIME, CONTENT) VALUES (:mId, :pNo, TO_DATE(:commentTime, :format), :content)'
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'pNo': pNo, 'commentTime': commentTime, 'format': format, 'content': content})
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
    def add_transaction(mId, transTime, format, paymentMethod, deliveryMethod, deliveryPrice):
        sql = 'INSERT INTO TRANSACTION(BUYERID, TRANSTIME, PAYMENTMETHOD, DELIVERMETHOD, DELIVERPRICE) VALUES(:mId, TO_DATE(:transTime, :format), :paymentMethod, :deliveryMethod, :deliveryPrice) RETURNING TNO INTO :out_tNo'
        cursor = DB.prepare(sql)
        out_tNo = cursor.var(oracledb.DB_TYPE_NUMBER)
        DB.execute_input(DB.prepare(sql), {'mId': mId, 'TRANSTIME': transTime, 'format': format, 'out_tNo': out_tNo, 'paymentMethod': paymentMethod, 'deliveryMethod': deliveryMethod, 'deliveryPrice': deliveryPrice})
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

class Chat():
    def get_chatroom(mId1, mId2):
        sql = 'SELECT CHATROOMID FROM CHATMEM WHERE MID IN (:mId1, :mId2) GROUP BY CHATROOMID HAVING COUNT(DISTINCT mId) >= 2'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'mId1': mId1, 'mId2': mId2}))
    
    def create_chatroom(mId1, mId2, createTime, format):
        out_id = cursor.var(oracledb.DB_TYPE_NUMBER)
        sql = 'INSERT INTO CHATROOM(CREATETIME) VALUES(TO_DATE(:createTime, :format)) RETURNING CHATROOMID INTO :out_id'
        DB.execute_input(DB.prepare(sql), {'createTime': createTime, 'format': format, 'out_id': out_id})
        print('test-------------------------------------------')
        print(int(out_id.getvalue()[0]))
        print(mId1)

        sql = 'INSERT INTO CHATMEM(CHATROOMID, MID) VALUES (:out_id, :mId1)'
        DB.execute_input(DB.prepare(sql), {'out_id': int(out_id.getvalue()[0]), 'mId1': mId1})
        sql = 'INSERT INTO CHATMEM(CHATROOMID, MID) VALUES (:out_id, :mId2)'
        DB.execute_input(DB.prepare(sql), {'out_id': int(out_id.getvalue()[0]), 'mId2': mId2})
        DB.commit()
        return out_id
    
    def get_chatroom_messages(chatroomId):
        sql = 'SELECT CHATROOMID, SENDERID, CONTENT, MESSAGETIME FROM CHATROOM NATURAL JOIN MESSAGE WHERE CHATROOMID = :chatroomId ORDER BY MESSAGETIME'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'chatroomId': chatroomId}))    

    def select_user_all_chatroom(mId):
        sql = 'SELECT CHATROOMID, MID RECEIVERID, USERNAME FROM CHATMEM NATURAL JOIN MEMBER WHERE MID != :mId AND CHATROOMID IN (SELECT CHATROOMID FROM CHATROOM NATURAL JOIN CHATMEM WHERE MID = :mId)'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'mId': mId}))
    
    def add_message_to_chatroom(chatroomId, mId, message, time):
        sql = 'INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (:chatroomId, :mId, :message, :time)'
        DB.execute_input(DB.prepare(sql), {'chatroomId': chatroomId, 'mId': mId, 'message': message, 'time': time})
        DB.commit()

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