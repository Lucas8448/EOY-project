from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3 as sql
from uuid7 import generate_uuid

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")

#c.execute('''CREATE TABLE users (
#                id TEXT PRIMARY KEY,
#                username TEXT UNIQUE,
#                email TEXT,
#                password TEXT,
#                avatar BLOB,
#                discriminator TEXT
#            )''')
#
#c.execute('''CREATE TABLE servers (
#                id TEXT PRIMARY KEY,
#                name TEXT,
#                owner_id TEXT,
#                icon BLOB,
#                FOREIGN KEY(owner_id) REFERENCES users(id)
#            )''')
#
#c.execute('''CREATE TABLE channels (
#                id TEXT PRIMARY KEY,
#                name TEXT,
#                server_id TEXT,
#                FOREIGN KEY(server_id) REFERENCES servers(id)
#            )''')
#
#c.execute('''CREATE TABLE server_members (
#                id TEXT PRIMARY KEY,
#                server_id TEXT,
#                user_id TEXT,
#                FOREIGN KEY(server_id) REFERENCES servers(id),
#                FOREIGN KEY(user_id) REFERENCES users(id)
#            )''')
#
#c.execute('''CREATE TABLE messages (
#                id TEXT PRIMARY KEY,
#                content TEXT,
#                author_id TEXT,
#                channel_id TEXT,
#                timestamp TEXT,
#                FOREIGN KEY(author_id) REFERENCES users(id),
#                FOREIGN KEY(channel_id) REFERENCES channels(id)
#            )''')

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
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    rows = cur.fetchall()
    if len(rows) == 0:
      # return error in login emit
      print('login failed')
      emit('login', {'error': 'Invalid username or password'})
    else:
      print('login success')
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
      emit('login', user_data, servers)

@socketio.on('register')
def handle_register(data):
  print('register')
  username = data['username']
  password = data['password']
  email = data['email']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
    rows = cur.fetchall()
    if len(rows) > 0:
      print('register failed')
      emit('register', {'error': 'Username or email already in use'})
    else:
      cur.execute("INSERT INTO users (id, username, password, email) VALUES (?, ?, ?, ?)",(generate_uuid(), username, password, email))
      con.commit()
      print('register success')
      emit('register')
      
@socketio.on('get_self')
def handle_get_user(data):
  print('get_self')
  username = data['username']
  password = data['password']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
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
      
@socketio.on('get_server')
def handle_get_server(data):
  print('get_server')
  server_id = data['server_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM servers WHERE id=?", (server_id,))
    rows = cur.fetchall()
    if len(rows) == 0:
      print('get_server failed')
      emit('get_server_failed')
    else:
      print('get_server success')
      server = rows[0]
      server_data = {
          "id": server[0],
          "name": server[1],
          "owner_id": server[2],
          "icon": server[3]
      }
      cur.execute("SELECT * FROM channels WHERE server_id=?", (server[0],))
      rows = cur.fetchall()
      channels = []
      for row in rows:
        channels.append({
            "id": row[0],
            "name": row[1],
            "server_id": row[2]
        })
      emit('get_server_success', server_data, channels)

@socketio.on('get_channel')
def handle_get_channel(data):
  print('get_channel')
  channel_id = data['channel_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM channels WHERE id=?", (channel_id,))
    rows = cur.fetchall()
    if len(rows) == 0:
      print('get_channel failed')
      emit('get_channel_failed')
    else:
      print('get_channel success')
      channel = rows[0]
      channel_data = {
          "id": channel[0],
          "name": channel[1],
          "server_id": channel[2]
      }
      cur.execute("SELECT * FROM messages WHERE channel_id=?", (channel[0],))
      rows = cur.fetchall()
      messages = []
      for row in rows:
        cur.execute("SELECT * FROM users WHERE id=?", (row[2],))
        author = cur.fetchall()[0]
        messages.append({
            "id": row[0],
            "content": row[1],
            "author": {
                "id": author[0],
                "username": author[1],
                "avatar": author[4],
                "discriminator": author[5]
            },
            "channel_id": row[3],
            "timestamp": row[4]
        })
      emit('get_channel_success', channel_data, messages)

@socketio.on('get_user')
def handle_get_user(data):
  print('get_user')
  user_id = data['user_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    rows = cur.fetchall()
    if len(rows) == 0:
      print('get_user failed')
      emit('get_user_failed')
    else:
      print('get_user success')
      user = rows[0]
      user_data = {
          "username": user[1],
          "avatar": user[4],
          "discriminator": user[5]
      }
      emit('get_user_success', user_data)

@socketio.on('get_users')
def handle_get_users(data):
  print('get_users')
  server_id = data['server_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM server_members WHERE server_id=?", (server_id,))
    rows = cur.fetchall()
    users = []
    for row in rows:
      cur.execute("SELECT * FROM users WHERE id=?", (row[0],))
      user = cur.fetchall()[0]
      users.append({
          "username": user[1],
          "avatar": user[4],
          "discriminator": user[5]
      })
    emit('get_users_success', users)

@socketio.on('create_server')
def handle_create_server(data):
  print('create_server')
  name = data['name']
  owner_id = data['owner_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO servers (id, name, owner_id) VALUES (?, ?, ?)",(generate_uuid(), name, owner_id))
    con.commit()
    cur.execute("SELECT * FROM servers WHERE name=? AND owner_id=?", (name, owner_id))
    server = cur.fetchall()[0]
    print('create_server success')
    emit('create_server_success', server[0])

@socketio.on('create_channel')
def handle_create_channel(data):
  print('create_channel')
  name = data['name']
  server_id = data['server_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO channels (id, name, server_id) VALUES (?, ?, ?)", (generate_uuid(), name, server_id))
    con.commit()
    cur.execute("SELECT * FROM channels WHERE name=? AND server_id=?", (name, server_id))
    channel = cur.fetchall()[0]
    print('create_channel success')
    emit('create_channel_success', channel[0])

@socketio.on('send_message')
# send message only to clients where the logged in user is in the channel
def handle_send_message(data):
  print('send_message')
  content = data['content']
  author_id = data['author_id']
  channel_id = data['channel_id']
  timestamp = data['timestamp']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO messages (id, content, author_id, channel_id, timestamp) VALUES (?, ?, ?, ?, ?)", (generate_uuid(), content, author_id, channel_id, timestamp))
    con.commit()
    cur.execute("SELECT * FROM messages WHERE content=? AND author_id=? AND channel_id=? AND timestamp=?", (content, author_id, channel_id, timestamp))
    message = cur.fetchall()[0]
    print('send_message success')
    emit('send_message_success', message[0], room=channel_id)

@socketio.on('add_member')
def handle_add_member(data):
  print('add_member')
  user_id = data['user_id']
  server_id = data['server_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("INSERT INTO server_members (user_id, server_id) VALUES (?, ?)", (user_id, server_id))
    con.commit()
    print('add_member success')
    emit('add_member_success', room=server_id)

@socketio.on('remove_member')
def handle_remove_member(data):
  print('remove_member')
  user_id = data['user_id']
  server_id = data['server_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("DELETE FROM server_members WHERE user_id=? AND server_id=?", (user_id, server_id))
    con.commit()
    print('remove_member success')
    emit('remove_member_success', room=server_id)

@socketio.on('delete_server')
def handle_delete_server(data):
  print('delete_server')
  server_id = data['server_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("DELETE FROM servers WHERE id=?", (server_id,))
    con.commit()
    cur.execute("DELETE FROM channels WHERE server_id=?", (server_id,))
    con.commit()
    cur.execute("DELETE FROM server_members WHERE server_id=?", (server_id,))
    con.commit()
    cur.execute("DELETE FROM messages WHERE channel_id IN (SELECT id FROM channels WHERE server_id=?)", (server_id,))
    con.commit()
    print('delete_server success')
    emit('delete_server_success', room=server_id)

@socketio.on('delete_channel')
def handle_delete_channel(data):
  print('delete_channel')
  channel_id = data['channel_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("DELETE FROM channels WHERE id=?", (channel_id,))
    con.commit()
    cur.execute("DELETE FROM messages WHERE channel_id=?", (channel_id,))
    con.commit()
    print('delete_channel success')
    emit('delete_channel_success', room=channel_id)

@socketio.on('delete_message')
def handle_delete_message(data):
  print('delete_message')
  message_id = data['message_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("DELETE FROM messages WHERE id=?", (message_id,))
    con.commit()
    print('delete_message success')
    emit('delete_message_success', room=message_id)

@socketio.on('logout')
def handle_logout(data):
  print('logout')
  user_id = data['user_id']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
    con.commit()
    print('logout success')
    emit('logout_success', room=user_id)

#run app
if __name__ == '__main__':
    socketio.run(app, port=3001)