class Message {
  static SEND_DATA = "sd";
  static SEND_SESSIONS = "ss";
  static SEND_RESIZE = "sr";
  static SEND_CLOSE = "sc";
  static SEND_LOAD = "sl";

  static GET_DATA = "gd";
  static GET_SESSIONS = "gs";
  static GET_RESIZE = "gr";
  static GET_CLOSE = "gc";
  static GET_LOAD = "gl";

  constructor(data, sid, action) {
    this.data = data;
    this.sid = sid;
    this.action = action;
  }

  toJSON() {
    return {
      data: this.data,
      sid: this.sid,
      action: this.action,
    };
  }

  equals(other) {
    if (!(other instanceof this.constructor)) {
      return false;
    }
    return JSON.stringify(this) === JSON.stringify(other);
  }

  static create(data, sid, action) {
    const msg = new Message(data, sid, action);

    return msg.toJSON();
  }

  static data(...args) {
    return Message.create(args[0], args[1], Message.SEND_DATA);
  }
  static session = Message.create(
    "get_all_sessions",
    null,
    Message.SEND_SESSIONS
  );

  static resize(...args) {
    return Message.create(args[0], args[1], Message.SEND_RESIZE);
  }
  static close(sid) {
    return Message.create("close_session", sid, Message.SEND_CLOSE);
  }
  static load(sids) {
    return Message.create("get_session_content", sids, Message.SEND_LOAD);
  }
}

function displayNotification(msg) {
  alert(msg);
}
