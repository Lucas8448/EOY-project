import os
from flask import *
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3 as sql
from uuid7 import generate_uuid

sessions = {}

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
  print('connected')
  sessions[request.sid] = None
  emit('connected')

@socketio.on('disconnect')
def handle_disconnect():
  print('disconnected')
  # delete session
  del sessions[request.sid]
  emit('disconnected')
  
@socketio.on('login')
def handle_login(data):
  print('login')
  username = data['username']
  password = data['password']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username, ))
    user_rows = cur.fetchall()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE password=?", (password, ))
    pass_rows = cur.fetchall()
    if len(user_rows) == 0:
      # return error in login emit
      print('login failed')
      emit('login', {'error': 'Invalid username'})
    if len(pass_rows) == 0:
      # return error in login emit
      print('login failed')
      emit('login', {'error': 'Invalid password'})
    else:
      print('login success')
      user = pass_rows[0]
      user_data = {
          "id": user[0],
          "username": user[1],
          "email": user[2],
          "discriminator": user[4]
      }
      sessions[request.sid] = user[0]
      emit('login', {'success':True, 'user':user_data})

@socketio.on('register')
def handle_register(data):
  print('register')
  username = data['username']
  password = data['password']
  email = data['email']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username, ))
    user_rows = cur.fetchall()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email, ))
    email_rows = cur.fetchall()
    if len(email_rows) > 0:
      print('register failed')
      emit('register', {'error': 'Email already in use'})
    if len(user_rows) > 0:
      print('register failed')
      emit('register', {'error': 'Username already in use'})
    else:
      cur.execute("INSERT INTO users (id, username, password, email) VALUES (?, ?, ?, ?)",(generate_uuid(), username, password, email))
      con.commit()
      cur = con.cursor()
      cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
      rows = cur.fetchall()
      user = rows[0]
      user_data = {
          "id": user[0],
          "username": user[1],
          "email": user[2],
          "discriminator": user[4]
      }
      print('register success')
      sessions[request.sid] = user[0]
      emit('register', {'success':True, "user":user_data})


@socketio.on('add_server')
def handle_addServer(data):
    print('add_server')
    name = data['name']
    user_id = sessions[request.sid]
    print(name, user_id)
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO servers (id, name, owner_id) VALUES (?, ?, ?)",
                        (generate_uuid(), name, user_id))
            con.commit()
            cur.execute(
                "SELECT * FROM servers WHERE name=? AND owner_id=?", (name, user_id))
            server = cur.fetchone()
            if server is not None:
                # add user as member of server
                cur.execute("INSERT INTO server_members (server_id, user_id) VALUES (?, ?)",
                            (server[0], user_id))
                con.commit()
                emit('addServer', {'success': True, 'server': {
                    "id": server[0],
                    "name": server[1],
                    "owner_id": server[2]
                }})
            else:
                print("Error: Server not found in the database")
                emit('addServer', {'success': False})
    except Exception as e:
        print("Error creating server:", e)
        emit('addServer', {'success': False})


@socketio.on('get_servers')
def handle_get_servers():
    user_id = sessions[request.sid]
    print(user_id)
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute(
                "SELECT server_id FROM server_members WHERE user_id=?", (user_id,))
            server_ids = [row[0] for row in cur.fetchall()]
            servers = []
            for server_id in server_ids:
                cur.execute("SELECT * FROM servers WHERE id=?", (server_id,))
                server = cur.fetchone()
                if server:
                    servers.append(dict(server))
            emit('get_servers', {"success": True, "servers": servers})
    except Exception as e:
        print("Error fetching servers:", e)
        emit('get_servers', {"success": False})

@socketio.on('get_channels')
def handle_get_channels(data):
    server_id = data['server_id']
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM channels WHERE server_id=?", (server_id,))
        rows = cur.fetchall()
        channels = [{"id": row[0], "name": row[1]} for row in rows]
        emit('get_channels', {"success": True, "channels": channels})

@socketio.on('get_messages')
def handle_get_messages(data):
    channel_id = data['channel_id']
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM messages WHERE channel_id=?", (channel_id,))
        rows = cur.fetchall()
        messages = [{"id": row[0], "content": row[1], "author_id": row[2], "timestamp": row[4]} for row in rows]
        emit('get_messages', {"success": True, "messages": messages})


@socketio.on('send_message')
def handle_send_message(data):
    channel_id = data['channel_id']
    author_id = data['author_id']
    content = data['content']
    with sql.connect("database.db") as con:
        cur = con.cursor()
        message_id = generate_uuid()
        cur.execute("INSERT INTO messages (id, content, author_id, channel_id) VALUES (?, ?, ?, ?)",
                    (message_id, content, author_id, channel_id))
        con.commit()
        message = {
            "id": message_id,
            "content": content,
            "author_id": author_id,
            "timestamp": None  # You may want to add a timestamp field to your messages table
        }
        emit('send_message', {"success": True, "message": message})
        # send to all users
        emit('message', {"success": True, "message": message}, broadcast=True)


#run app
if __name__ == '__main__':
    socketio.run(app, port=3055)