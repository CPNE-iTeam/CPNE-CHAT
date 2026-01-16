from db import Database
from message import Message

class UserActions:
    def __init__(self, db: Database):
        self.db = db

    def execute_action(self, message: Message) -> bool:
        message_content = message.content

        match message_content:
            case "/delete":
                self.user_delete_last_message(message.authorIP)
                return False
            case _:
                return True

    def user_delete_last_message(self, authorIP: str):
        author_messages = self.db.get_messages_from_authorIP(authorIP)
        if len(author_messages) == 0:
            return
        
        last_message = author_messages[-1]
        self.db.delete_message(last_message.id)
 
        
    