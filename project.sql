--------------------------------------------------------
--  DDL for Table Member
--------------------------------------------------------

CREATE TABLE MEMBER (	
   mId         NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
   username    VARCHAR2(38  BYTE),
   mail        VARCHAR2(256 BYTE),
   account     VARCHAR2(128 BYTE), 
   passwd      VARCHAR2(128 BYTE), 
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
   content        CLOB,      
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
   cartTime       date,
   pNo            NUMBER,
   amount         NUMBER(38,0),
   PRIMARY KEY (mId, cartTime),
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
--  DDL for Table Record
--------------------------------------------------------

CREATE TABLE MESSAGE (	
   senderId          NUMBER,
   receiverId        NUMBER,
   messageTime       date,
   content           CLOB,
   PRIMARY KEY (senderId, receiverId, messageTime),
   FOREIGN KEY (senderId) REFERENCES MEMBER(mId),
   FOREIGN KEY (receiverId) REFERENCES MEMBER(mId)
);


-- DROP TABLE BROWSE;
-- DROP TABLE COMMENTS;
-- DROP TABLE ORDERS;
-- DROP TABLE RECORD;
-- DROP TABLE MESSAGE;
-- DROP TABLE CART;
-- DROP TABLE TRANSACTION;
-- DROP TABLE PRODUCT;
-- DROP TABLE MEMBER;


-- INSERT INTO MEMBER (USERNAME, MAIL, ACCOUNT, PASSWD) values ('test', 'test@gmail.com', 'test', 'test')

-- INSERT INTO PRODUCT (PNAME, PRICE, PDESC, LAUNCHBY) values ('product1', 10, 'product desc', 1)
