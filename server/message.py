

class Message:
    def __init__(self, content: str, author: str, authorIP: str, authorNameTag: int, time: int):
        self.content = content
        self.author = author
        self.authorIP = authorIP
        self.authorNameTag = authorNameTag
        self.time = time

    def to_dict(self, includes: list[str]) -> dict:
        message_dict = {"content": self.content,
                        "author": self.author,
                        "authorIP": self.authorIP,
                        "authorNameTag": self.authorNameTag,
                        "time": self.time}
        return {key: message_dict[key] for key in includes if key in message_dict}