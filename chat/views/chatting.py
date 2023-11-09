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
from api.sql import Member, Orders, Product, Record, Cart, Transaction, Comments, Chat

chat = Blueprint('chat', __name__, template_folder='../templates')

@chat.route('/', methods=['GET', 'POST'])
@login_required
def chatroom():
    chatroom_list = []
    
    current_chatroomId = None
    message_list = []
    receiver = None
    sender = None

    if request.method == 'POST':
        current_chatroomId = request.values.get('chatroomId')
        Chat.add_message_to_chatroom(current_chatroomId, current_user.id, request.values.get('message'), datetime.now())

    
    if request.values.get('mId') != None:
        receiverId = request.values.get('mId')
        current_chatroom = Chat.get_chatroom(current_user.id, receiverId)
        if not current_chatroom:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            format = 'yyyy-mm-dd hh24:mi:ss'
            current_chatroomId = Chat.create_chatroom(current_user.id, receiverId, time, format)
        else:
            current_chatroomId = current_chatroom[0]


        messages = Chat.get_chatroom_messages(current_chatroomId)
        for message in messages:
            curr_message = {
                'senderId': message[1],
                'content': message[2],
                'messageTime': message[3]
            }
            message_list.append(curr_message)


        receiver_items = Member.get_member_by_Id(receiverId)
        receiver = {
            'receiverId': receiver_items[0],
            'account': receiver_items[1],
            'username': receiver_items[2]
        }

        sender_items = Member.get_member_by_Id(current_user.id)
        sender = {
            'senderId': sender_items[0],
            'account': sender_items[1],
            'username': sender_items[2]
        }


    chatrooms = Chat.select_user_all_chatroom(current_user.id)
    for chatroom in chatrooms:
        curr_chatroom = {
            'chatroomId': chatroom[0],
            'receiverId': chatroom[1],
            'receiverName': chatroom[2]
        }
        chatroom_list.append(curr_chatroom)


    return render_template('chatroom.html', current_chatroomId = current_chatroomId, receiver = receiver, sender = sender, chatroom_list=chatroom_list, message_list = message_list)
