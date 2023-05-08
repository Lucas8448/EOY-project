import os
from flask import *
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3 as sql
from uuid7 import generate_uuid


app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/image/<name>')
def get_image(name):
  if os.path.isfile(f'assets/images/{name}'):
    return send_file(f'assets/images/{name}', mimetype='image/png')
  else:
    return send_file(f'assets/images/default_user.png', mimetype='image/png')

@app.route('/icon/<name>')
def get_icon(name):
  if os.path.isfile(f'assets/icon/{name}'):
    return send_file(f'assets/icon/{name}', mimetype='image/png')
  else:
    return 404

@socketio.on('connect')
def handle_connect():
  print('connected')
  emit('connected')

@socketio.on('disconnect')
def handle_disconnect():
  print('disconnected')
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
          "avatar": user[4],
          "discriminator": user[5]
      }
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
      cur.execute("INSERT INTO users (id, username, password, email, avatar) VALUES (?, ?, ?, ?, ?)",(generate_uuid(), username, password, email, 'default_user.png'))
      con.commit()
      cur = con.cursor()
      cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
      rows = cur.fetchall()
      user = rows[0]
      user_data = {
          "id": user[0],
          "username": user[1],
          "email": user[2],
          "avatar": user[4],
          "discriminator": user[5]
      }
      print('register success')
      emit('register', {'success':True, "user":user_data})
      
@socketio.on('get_self')
def handle_get_user(data):
  print('get_self')
  token = data['token']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (token))
    rows = cur.fetchall()
    if len(rows) == 0:
      print('get_self failed')
      emit('get_self_failed')
    else:
      print('get_self success')
      user = rows[0]
      user_data = {
          "id": user[0],
          "username": user[1],
          "email": user[2],
          "avatar": user[4],
          "discriminator": user[5]
      }
      cur.execute("SELECT * FROM server_members WHERE user_id=?", (user[0],))
      rows = cur.fetchall()
      servers = []
      for row in rows:
        cur.execute("SELECT * FROM servers WHERE id=?", (row[1],))
        server = cur.fetchall()[0]
        servers.append({
            "id": server[0],
            "name": server[1],
            "owner_id": server[2],
            "icon": server[3]
        })
      emit('get_self_success', user_data, servers)
      

@socketio.on('get_servers')
def handle_get_servers(data):
  print('get_servers')
  token = data['Id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (token))
    rows = cur.fetchall()
    if len(rows) == 0:
      print('get_servers failed')
      emit('get_servers', {'error': 'Username already in use'})
    else:
      print('get_servers success')
      user = rows[0]
      cur.execute("SELECT * FROM server_members WHERE user_id=?", (user[0],))
      rows = cur.fetchall()
      servers = []
      for row in rows:
        cur.execute("SELECT * FROM servers WHERE id=?", (row[1],))
        server = cur.fetchall()[0]
        servers.append({
            "id": server[0],
            "name": server[1],
            "owner_id": server[2],
            "icon": server[3]
        })
      emit('get_servers', {'success': True, "servers": servers})


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


#run app
if __name__ == '__main__':
    socketio.run(app, port=3055)