DROP TABLE BROWSE;
DROP TABLE COMMENTS;
DROP TABLE ORDERS;
DROP TABLE RECORD;
DROP TABLE CART;
DROP TABLE TRANSACTION;
DROP TABLE PRODUCT;
DROP TABLE CHATMEM;
DROP TABLE MESSAGE;
DROP TABLE CHATROOM;
DROP TABLE MEMBER;

--------------------------------------------------------
--  DDL for Table Member
--------------------------------------------------------

CREATE TABLE MEMBER (	
   MID         NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
   ACCOUNT     VARCHAR2(128 BYTE) UNIQUE, 
   PASSWD      VARCHAR2(128 BYTE), 
   USERNAME    VARCHAR2(38  BYTE),
   PRIMARY KEY (mId)
);

--------------------------------------------------------
--  DDL for Table Product
--------------------------------------------------------

CREATE TABLE PRODUCT (	
   pNo         NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1), 
	pName       VARCHAR2(128 BYTE), 
	price       NUMBER(38,0), 
	pDesc       CLOB,
   launchBy    NUMBER,
   isAvailable NUMBER(1),
   PRIMARY KEY (pNo),
   FOREIGN KEY (launchBy) REFERENCES MEMBER(mId)
);

--------------------------------------------------------
--  DDL for Table Browse
--------------------------------------------------------

CREATE TABLE BROWSE (	
   mId         NUMBER,
   pNo         NUMBER,
   browseTime  date,
   PRIMARY KEY (mId, pNo, browseTime),
   FOREIGN KEY (mId) REFERENCES MEMBER(mId),
   FOREIGN KEY (pNo) REFERENCES PRODUCT(pNo)
);

--------------------------------------------------------
--  DDL for Table Comment
--------------------------------------------------------

CREATE TABLE COMMENTS (	
   mId            NUMBER,
   pNo            NUMBER,
   commentTime    date,
   content        VARCHAR2(1024 BYTE),      
   PRIMARY KEY (mId, pNo, commentTime),
   FOREIGN KEY (mId) REFERENCES MEMBER(mid),
   FOREIGN KEY (pNo) REFERENCES PRODUCT(pNo)
);

--------------------------------------------------------
--  DDL for Table Transaction
--------------------------------------------------------

CREATE TABLE TRANSACTION (	
   tNo            NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
   buyerId        NUMBER,
   transTime      date,
   paymentMethod  VARCHAR2(32 BYTE),
   deliverMethod  VARCHAR2(32 BYTE),
   deliverPrice   NUMBER(38,0), 
   PRIMARY KEY (tNo),
   FOREIGN KEY (buyerId) REFERENCES MEMBER(mid)
);

--------------------------------------------------------
--  DDL for Table Cart
--------------------------------------------------------

CREATE TABLE CART (	
   mId            NUMBER,
   cartTime       date,
   tNo            NUMBER,      
   PRIMARY KEY (mId, cartTime),
   FOREIGN KEY (mId) REFERENCES MEMBER(mid),
   FOREIGN KEY (tNo) REFERENCES TRANSACTION(tNo)
);

--------------------------------------------------------
--  DDL for Table Order
--------------------------------------------------------

CREATE TABLE ORDERS (	
   mId            NUMBER,
   cartTime       DATE,
   pNo            NUMBER,
   amount         NUMBER(38,0),
   PRIMARY KEY (mId, cartTime, pNo),
   FOREIGN KEY (mId, cartTime) REFERENCES CART(mId, cartTime),
   FOREIGN KEY (pNo) REFERENCES PRODUCT(pNo)
);

--------------------------------------------------------
--  DDL for Table Record
--------------------------------------------------------

CREATE TABLE RECORD (	
   tNo         NUMBER,
   pNo         NUMBER,
   amount      NUMBER(38,0),
   salePrice   NUMBER(38,0),   
   PRIMARY KEY (tNo, pNo),
   FOREIGN KEY (tNo) REFERENCES TRANSACTION(tNo),
   FOREIGN KEY (pNo) REFERENCES PRODUCT(pNo)
);

--------------------------------------------------------
--  DDL for Table Chatroom
--------------------------------------------------------

CREATE TABLE CHATROOM (	
   chatroomId        NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
   createTime        DATE,
   PRIMARY KEY (chatroomId)
);

--------------------------------------------------------
--  DDL for Table ChatMEM
--------------------------------------------------------

CREATE TABLE CHATMEM (	
   chatroomId       NUMBER,
   mId              NUMBER,
   PRIMARY KEY (chatroomId, mId),
   FOREIGN KEY (chatroomId) REFERENCES CHATROOM(chatroomId),
   FOREIGN KEY (mId) REFERENCES MEMBER(mId)
);

--------------------------------------------------------
--  DDL for Table Message
--------------------------------------------------------

CREATE TABLE MESSAGE (	
   chatroomId        NUMBER,
   senderId          NUMBER,
   content           VARCHAR2(1024 BYTE),
   messageTime       DATE,
   PRIMARY KEY (chatroomId, senderId, messageTime),
   FOREIGN KEY (chatroomId) REFERENCES CHATROOM(chatroomId),
   FOREIGN KEY (senderId) REFERENCES MEMBER(mId)
);



INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user1', 'user1', 'user1');
INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user2', 'user2', 'user2');
INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user3', 'user3', 'user3');
INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user4', 'user4', 'user4');
INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user5', 'user5', 'user5');
INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user6', 'user6', 'user6');
INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user7', 'user7', 'user7');
INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user8', 'user8', 'user8');
INSERT INTO MEMBER (ACCOUNT, PASSWD, USERNAME) values ('user9', 'user9', 'user9');

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product1', 10, 'product description', 1, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product2', 20, 'product description', 1, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product3', 30, 'product description', 1, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product4', 40, 'product description', 1, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product5', 50, 'product description', 1, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product6', 60, 'product description', 1, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product7', 70, 'product description', 1, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product8', 80, 'product description', 1, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user1-product9', 90, 'product description', 1, 1);

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product1', 10, 'product description', 2, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product2', 20, 'product description', 2, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product3', 30, 'product description', 2, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product4', 40, 'product description', 2, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product5', 50, 'product description', 2, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product6', 60, 'product description', 2, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product7', 70, 'product description', 2, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product8', 80, 'product description', 2, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user2-product9', 90, 'product description', 2, 1);

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product1', 10, 'product description', 3, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product2', 20, 'product description', 3, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product3', 30, 'product description', 3, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product4', 40, 'product description', 3, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product5', 50, 'product description', 3, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product6', 60, 'product description', 3, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product7', 70, 'product description', 3, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product8', 80, 'product description', 3, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user3-product9', 90, 'product description', 3, 1);

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product1', 10, 'product description', 4, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product2', 20, 'product description', 4, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product3', 30, 'product description', 4, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product4', 40, 'product description', 4, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product5', 50, 'product description', 4, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product6', 60, 'product description', 4, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product7', 70, 'product description', 4, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product8', 80, 'product description', 4, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user4-product9', 90, 'product description', 4, 1);

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product1', 10, 'product description', 5, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product2', 20, 'product description', 5, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product3', 30, 'product description', 5, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product4', 40, 'product description', 5, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product5', 50, 'product description', 5, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product6', 60, 'product description', 5, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product7', 70, 'product description', 5, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product8', 80, 'product description', 5, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user5-product9', 90, 'product description', 5, 1);

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product1', 10, 'product description', 6, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product2', 20, 'product description', 6, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product3', 30, 'product description', 6, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product4', 40, 'product description', 6, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product5', 50, 'product description', 6, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product6', 60, 'product description', 6, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product7', 70, 'product description', 6, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product8', 80, 'product description', 6, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user6-product9', 90, 'product description', 6, 1);

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product1', 10, 'product description', 7, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product2', 20, 'product description', 7, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product3', 30, 'product description', 7, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product4', 40, 'product description', 7, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product5', 50, 'product description', 7, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product6', 60, 'product description', 7, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product7', 70, 'product description', 7, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product8', 80, 'product description', 7, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user7-product9', 90, 'product description', 7, 1);

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product1', 10, 'product description', 8, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product2', 20, 'product description', 8, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product3', 30, 'product description', 8, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product4', 40, 'product description', 8, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product5', 50, 'product description', 8, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product6', 60, 'product description', 8, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product7', 70, 'product description', 8, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product8', 80, 'product description', 8, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user8-product9', 90, 'product description', 8, 1);

INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product1', 10, 'product description', 9, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product2', 20, 'product description', 9, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product3', 30, 'product description', 9, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product4', 40, 'product description', 9, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product5', 50, 'product description', 9, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product6', 60, 'product description', 9, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product7', 70, 'product description', 9, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product8', 80, 'product description', 9, 1);
INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY, ISAVAILABLE) values ('user9-product9', 90, 'product description', 9, 1);

DECLARE
   room_id CHATROOM.CHATROOMID%TYPE;
BEGIN
   INSERT INTO CHATROOM (CREATETIME) VALUES (sysdate) RETURNING CHATROOMID INTO room_id;
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 1);
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 2);
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there1\nHi', sysdate - 1 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 2, 'Hi there2\nHi', sysdate - 2 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 2, 'Hi there3\nHi', sysdate - 3 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there4\nHi', sysdate - 4 * (1/1440 * 5));

   INSERT INTO CHATROOM (CREATETIME) VALUES (sysdate) RETURNING CHATROOMID INTO room_id;
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 1);
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 3);
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 3, 'Hi there1\nHi', sysdate - 1 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there2\nHi', sysdate - 2 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 3, 'Hi there3\nHi', sysdate - 3 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there4\nHi', sysdate - 4 * (1/1440 * 5));

   INSERT INTO CHATROOM (CREATETIME) VALUES (sysdate) RETURNING CHATROOMID INTO room_id;
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 1);
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 4);
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 4, 'Hi there1\nHi', sysdate - 1 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 4, 'Hi there2\nHi', sysdate - 2 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there3\nHi', sysdate - 3 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there4\nHi', sysdate - 4 * (1/1440 * 5));

   INSERT INTO CHATROOM (CREATETIME) VALUES (sysdate) RETURNING CHATROOMID INTO room_id;
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 1);
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 5);
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 5, 'Hi there1\nHi', sysdate - 1 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there2\nHi', sysdate - 2 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there3\nHi', sysdate - 3 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 5, 'Hi there4\nHi', sysdate - 4 * (1/1440 * 5));

   INSERT INTO CHATROOM (CREATETIME) VALUES (sysdate) RETURNING CHATROOMID INTO room_id;
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 1);
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 6);
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 6, 'Hi there1\nHi', sysdate - 1 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there2\nHi', sysdate - 2 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there3\nHi', sysdate - 3 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 6, 'Hi there4\nHi', sysdate - 4 * (1/1440 * 5));

   INSERT INTO CHATROOM (CREATETIME) VALUES (sysdate) RETURNING CHATROOMID INTO room_id;
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 1);
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 7);
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there1\nHi', sysdate - 1 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 7, 'Hi there2\nHi', sysdate - 2 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 7, 'Hi there3\nHi', sysdate - 3 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there4\nHi', sysdate - 4 * (1/1440 * 5));

   INSERT INTO CHATROOM (CREATETIME) VALUES (sysdate) RETURNING CHATROOMID INTO room_id;
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 1);
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 8);
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 8, 'Hi there1\nHi', sysdate - 1 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 8, 'Hi there2\nHi', sysdate - 2 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 8, 'Hi there3\nHi', sysdate - 3 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there4\nHi', sysdate - 4 * (1/1440 * 5));

   INSERT INTO CHATROOM (CREATETIME) VALUES (sysdate) RETURNING CHATROOMID INTO room_id;
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 1);
   INSERT INTO CHATMEM (CHATROOMID, MID) VALUES (room_id, 8);
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there1\nHi', sysdate - 1 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 1, 'Hi there2\nHi', sysdate - 2 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 9, 'Hi there3\nHi', sysdate - 3 * (1/1440 * 5));
   INSERT INTO MESSAGE (CHATROOMID, SENDERID, CONTENT, MESSAGETIME) VALUES (room_id, 9, 'Hi there4\nHi', sysdate - 4 * (1/1440 * 5));
END;
