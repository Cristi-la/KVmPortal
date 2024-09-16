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

    def __init__(self, data, sid, action, vis) -> None:
        self.data = data
        self.sid = sid
        self.action = action
        self.vis = vis

    def toPy(self):
        data = {
            "data": self.data,
            "sid": self.sid,
            "action": self.action
        }

        if self.vis:
            data['vis'] = self.vis

        return data

    @classmethod
    def create(cls, data, sid, action, vis=None):
        msg = cls(data, sid, action, vis=vis)
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
    def load(data, sid, vis=None):
        return Message.create(data, sid, Message.SEND_LOAD, vis)