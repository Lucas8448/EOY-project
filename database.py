import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE users (
                id TEXT PRIMARY KEY,
                username TEXT,
                email TEXT,
                password TEXT,
                discriminator INTEGER
            )''')

c.execute('''CREATE TABLE servers (
                id TEXT PRIMARY KEY,
                name TEXT,
                owner_id TEXT,
                FOREIGN KEY(owner_id) REFERENCES users(id)
            )''')

c.execute('''CREATE TABLE channels (
                id TEXT PRIMARY KEY,
                name TEXT,
                server_id TEXT,
                FOREIGN KEY(server_id) REFERENCES servers(id)
            )''')

c.execute('''CREATE TABLE server_members (
                id TEXT PRIMARY KEY,
                server_id TEXT,
                user_id TEXT,
                FOREIGN KEY(server_id) REFERENCES servers(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )''')

c.execute('''CREATE TABLE messages (
                id TEXT PRIMARY KEY,
                content TEXT,
                author_id TEXT,
                channel_id TEXT,
                timestamp TEXT,
                FOREIGN KEY(author_id) REFERENCES users(id),
                FOREIGN KEY(channel_id) REFERENCES channels(id)
            )''')

conn.commit()
conn.close()