from dataclasses import dataclass


class Message:
    SEND_DATA = "sd"
    SEND_SESSIONS = "ss"
    # SEND_RESIZE = "sr"
    # SEND_CLOSE = "sc"
    SEND_LOAD = "sl"

    GET_SESSIONS = "gs"
    # GET_RESIZE = "gr"
    # GET_CLOSE = "gc"
    GET_LOAD = "gl"

    def __init__(self, data, sid, action) -> None:
        self.data = data
        self.sid = sid
        self.action = action

    def toPy(self):
        return {
            "data": self.data,
            "sid": self.sid,
            "action": self.action
        }

    @classmethod
    def create(cls, data, sid, action):
        msg = cls(data, sid, action)
        return msg.toPy()
    
    @staticmethod
    def data(data, sid):
        return Message.create(data, sid, Message.SEND_DATA)
    
    # @staticmethod
    # def resize(data, sid):
    #     return Message.create(data, sid, Message.SEND_RESIZE)
    
    # @staticmethod
    # def close(sid):
    #     return Message.create('session_close', sid, Message.SEND_CLOSE)
    
    @staticmethod
    def session(sids):
        return Message.create(sids, None, Message.SEND_SESSIONS)
    

    @staticmethod
    def load(data, sid):
        return Message.create(data, sid, Message.SEND_LOAD)