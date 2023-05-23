import os
from flask import *
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3 as sql
from uuid7 import generate_uuid
from moderator import moderate

sessions = {}
user_channels = {}
user_servers = {}

app = Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/ping')
def hello():
    return 'Pong!!'

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
  email = data['email']
  password = data['password']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password, ))
    rows = cur.fetchall()
    if len(rows) == 0:
      print('login failed')
      emit('login', {'error': 'Invalid email or password'})
    else:
      user = rows[0]
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
    elif len(user_rows) > 0:
      cur.execute("SELECT MAX(discriminator) FROM users WHERE username=?", (username, ))
      max_discriminator = cur.fetchone()[0]
      if max_discriminator is None:
          max_discriminator = 999  # Set to 999 so that the first user gets 1000
      discriminator = max_discriminator + 1
      cur.execute("INSERT INTO users (id, username, password, email, discriminator) VALUES (?, ?, ?, ?, ?)",(generate_uuid(), username, password, email, discriminator))
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
    else:
      discriminator = 1000  # The first user with this username
      cur.execute("INSERT INTO users (id, username, password, email, discriminator) VALUES (?, ?, ?, ?, ?)",(generate_uuid(), username, password, email, discriminator))
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
            columns = [column[0] for column in cur.description]
            server = cur.fetchone()
            if server is not None:
                # add user as member of server
                cur.execute("INSERT INTO server_members (server_id, user_id) VALUES (?, ?)",
                            (server[0], user_id))
                con.commit()
                # return all servers
                cur.execute(
                    "SELECT server_id FROM server_members WHERE user_id=?", (user_id,))
                server_ids = [row[0] for row in cur.fetchall()]
                servers = []
                for server_id in server_ids:
                    cur.execute(
                        "SELECT * FROM servers WHERE id=?", (server_id,))
                    server = cur.fetchone()
                    if server:
                        servers.append(dict(zip(columns, server)))
                emit('add_server', {'success': True, 'servers': servers})
            else:
                print("Error: Server not found in the database")
                emit('add_server', {'success': False})
    except Exception as e:
        print("Error creating server:", e)
        emit('add_server', {'success': False})


@socketio.on('get_servers')
def handle_get_servers():
    user_id = sessions[request.sid]
    print("userId", user_id)
    try:
      with sql.connect("database.db") as con:
          cur = con.cursor()
          cur.execute("SELECT server_id FROM server_members WHERE user_id=?", (user_id,))
          member_server_ids = [id[0] for id in cur.fetchall()]
          cur.execute("SELECT id FROM servers WHERE owner_id=?", (user_id,))
          owner_server_ids = [id[0] for id in cur.fetchall()]
          server_ids = list(set(member_server_ids + owner_server_ids))
          cur.execute("SELECT * FROM servers LIMIT 0")
          columns = [column[0] for column in cur.description]
          servers = []
          for server_id in server_ids:
              cur.execute("SELECT * FROM servers WHERE id=?", (server_id,))
              server = cur.fetchone()
              if server:
                  servers.append(dict(zip(columns, server)))
          emit('get_servers', {"success": True, "servers": servers})
    except Exception as e:
      print("Error loading servers:", e)
      emit('get_servers', {'success': False})

@socketio.on('add_channel')
def handle_addChannel(data):
    server_id = data['server_id']
    name = data['name']
    user_id = sessions[request.sid]
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM server_members WHERE server_id=? AND user_id=?", (server_id, user_id))
            rows = cur.fetchall()
            if len(rows) > 0:
                channel_id = generate_uuid()
                cur.execute("INSERT INTO channels (id, name, server_id) VALUES (?, ?, ?)",
                            (channel_id, name, server_id))
                con.commit()
                cur.execute(
                    "SELECT * FROM channels WHERE name=? AND server_id=?", (name, server_id))
                columns = [column[0] for column in cur.description]
                channel = cur.fetchone()
                if channel is not None:
                    # return all channels
                    cur.execute(
                        "SELECT * FROM channels WHERE server_id=?", (server_id,))
                    channels = []
                    for channel in cur.fetchall():
                        channels.append(dict(zip(columns, channel)))
                    user_servers[request.sid] = server_id
                    user_channels[request.sid] = channel_id
                    emit('add_channel', {'success': True, 'channels': channels})
                else:
                    print("Error: Channel not found in the database")
                    emit('add_channel', {'success': False})
            else:
                print("Error: User is not a member of the server")
                emit('add_channel', {'success': False})
    except Exception as e:
        print("Error creating channel:", e)
        emit('add_channel', {'success': False})

@socketio.on('get_channels')
def handle_get_channels(data):
    server_id = data['server_id']
    user_id = sessions[request.sid]
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM server_members WHERE server_id=? AND user_id=?", (server_id, user_id))
            rows = cur.fetchall()
            if len(rows) > 0:
                cur.execute(
                    "SELECT * FROM channels WHERE server_id=?", (server_id,))
                columns = [column[0] for column in cur.description]
                channels = []
                for channel in cur.fetchall():
                    channels.append(dict(zip(columns, channel)))
                user_servers[request.sid] = server_id
                emit('get_channels', {'success': True, 'channels': channels})
            else:
                print("Error: User is not a member of the server")
                emit('get_channels', {'success': False})
    except Exception as e:
        print("Error loading channels:", e)
        emit('get_channels', {'success': False})


@socketio.on('get_messages')
def handle_get_messages(data):
    channel_id = data['channel_id']
    user_channels[request.sid] = channel_id  # Update user's current channel
    print("Getting messages for channel", channel_id)
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM messages WHERE channel_id=?", (channel_id,))
        rows = cur.fetchall()
        messages = [{"id": row[0], "content": row[1],
                     "author_id": row[2], "timestamp": row[4]} for row in rows]
        emit('get_messages', {"success": True, "messages": messages})


@socketio.on('send_message')
def handle_send_message(data):
    channel_id = data['channel_id']
    author_id = sessions[request.sid]
    content = data['content']

    # Moderate the content
    if moderate(content):
        print("Message from user", author_id, "flagged by the moderation model.")
        # Emit only to the sender
        emit('send_message', {"success": False, "error": "Content violates policies"}, room=request.sid)
    else:
        print("Sending message to channel", channel_id, "from user", author_id, ":", content)
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
            # Emit only to the sender
            emit('send_message', {"success": True, "message": message}, room=request.sid)
            # send to all users in list user_channels except the sender
            for sid, channel in user_channels.items():
                if channel == channel_id and sid != request.sid:
                    emit('message', {"success": True, "message": message}, room=sid)


@socketio.on('search_user')
def handle_search_user(data):
  searchText = data['searchText']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username LIKE ?",
                (f"%{searchText}%", ))
    rows = cur.fetchall()
    users = [{"id": row[0], "username": row[1], "discriminator": row[4]} for row in rows]
    emit('search_user', {'success': True, 'users': users})


@socketio.on('add_member')
def handle_add_member(data):
  server_id = data['serverId']
  user_id = data['userId']
  with sql.connect("database.db") as con:
    cur = con.cursor()
    cur.execute(
        "INSERT INTO server_members (server_id, user_id) VALUES (?, ?)", (server_id, user_id))
    con.commit()
    emit('add_member', {'success': True})

# get username
@socketio.on('get_username')
def handle_get_username(data):
    user_id = data["userId"]
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        rows = cur.fetchall()
        if len(rows) > 0:
            emit('get_username', {'success': True, 'username': rows[0][1]})
        else:
            emit('get_username', {'success': False})

#run app
if __name__ == '__main__':
    socketio.run(app, port=3055)