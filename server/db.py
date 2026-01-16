import sqlite3
from message import Message

class Database:
    def __init__(self, db_path: str = "cpbechat.db"):
        self.db_path = db_path

        self.connection = None
        self.cursor = None

        self.tables_sql = """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content VARCHAR(1000) NOT NULL,
            author VARCHAR(255) NOT NULL,
            authorIP VARCHAR(255) NOT NULL,
            authorNameTag INTEGER NOT NULL,
            time INTEGER NOT NULL
        )
        """

    def init_db(self):
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.tables_sql)
        self.connection.commit()

    def new_message(self, message: Message):
        insert_sql = """
        INSERT INTO messages (content, author, authorIP, authorNameTag, time)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(insert_sql, (message.content, message.author, message.authorIP, message.authorNameTag, message.time))
        self.connection.commit()

    def get_messages(self) -> list[Message]:
        select_sql = "SELECT content, author, authorIP, authorNameTag, time FROM messages ORDER BY time ASC"
        self.cursor.execute(select_sql)
        rows = self.cursor.fetchall()
        messages = []
        
        for row in rows:
            messages.append(Message(row[0], row[1], row[2], row[3], row[4]))

        return messages
    
    def get_messages_from_authorIP(self, authorIP: str) -> list[Message]:
        select_sql = "SELECT content, author, authorIP, authorNameTag, time FROM messages WHERE authorIP = ? ORDER BY time ASC"
        self.cursor.execute(select_sql, (authorIP,))
        rows = self.cursor.fetchall()
        messages = []
        
        for row in rows:
            messages.append(Message(row[0], row[1], row[2], row[3], row[4]))

        return messages

    def close_db(self):
        if self.connection:
            self.connection.close()